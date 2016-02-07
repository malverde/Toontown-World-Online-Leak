from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.stdpy import threading
from direct.stdpy import threading2
import httplib
import json
import socket
import time

from toontown.rpc.ToontownRPCDispatcher import ToontownRPCDispatcher


class ToontownRPCConnection:
    notify = directNotify.newCategory('ToontownRPCConnection')

    def __init__(self, socket, handler):
        self.socket = socket

        self.dispatcher = ToontownRPCDispatcher(handler)

        self.socketLock = threading.Lock()
        self.readLock = threading.RLock()
        self.writeLock = threading.RLock()

        self.readBuffer = ''

        self.writeQueue = []
        self.writeSemaphore = threading.Semaphore(0)
        self.writeThread = threading.Thread(target=self.__writeThread)
        self.writeThread.start()

    def __readHeaders(self):
        # Acquire a read lock so that nothing intervenes:
        self.readLock.acquire()

        # Read data until we find the '\r\n\r\n' terminator:
        while '\r\n\r\n' not in self.readBuffer:
            try:
                self.readBuffer += self.socket.recv(2048)
            except:
                self.readLock.release()
                return {}

            if not self.readBuffer:
                # It looks like we have nothing to read.
                self.readLock.release()
                return {}

        # Collect the data before the terminator:
        terminatorIndex = self.readBuffer.find('\r\n\r\n')
        data = self.readBuffer[:terminatorIndex]

        # Truncate the remaining data:
        self.readBuffer = self.readBuffer[terminatorIndex + 4:]

        # We're done working with the read buffer, so:
        self.readLock.release()

        # Return the parsed headers in the form of a dictionary:
        return self.__parseHeaders(data)

    def __parseHeaders(self, data):
        headers = {}

        for i, line in enumerate(data.split('\n')):
            line = line.rstrip('\r')

            if i == 0:
                # This is the HTTP request.
                words = line.split(' ')
                if len(words) != 3:
                    self.writeHTTPError(400)
                    return {}

                command, _, version = words

                if command != 'POST':
                    self.writeHTTPError(501)
                    return {}

                if version not in ('HTTP/1.0', 'HTTP/1.1'):
                    self.writeHTTPError(505)
                    return {}
            else:
                # This is an HTTP header.
                words = line.split(': ', 1)
                if len(words) != 2:
                    self.writeHTTPError(400)
                    return {}

                headers[words[0].lower()] = words[1]

        return headers

    def read(self, timeout=None):
        """
        Read an HTTP POST request from the socket, and return the body.
        """
        self.socketLock.acquire()
        self.socket.settimeout(timeout)

        # Read our HTTP headers:
        headers = self.__readHeaders()

        if not headers:
            # It looks like we have nothing to read.
            self.socketLock.release()
            return ''

        # We need a content-length in order to read POST data:
        contentLength = headers.get('content-length', '')
        if (not contentLength) or (not contentLength.isdigit()):
            self.socketLock.release()
            self.writeHTTPError(400)
            return ''

        # Acquire a read lock so nothing touches the read buffer while we work:
        self.readLock.acquire()

        contentLength = int(contentLength)

        # Ensure we have all of our content:
        while len(self.readBuffer) < contentLength:
            try:
                self.readBuffer += self.socket.recv(2048)
            except:
                self.readLock.release()
                self.socketLock.release()
                return ''

            if not self.readBuffer:
                # It looks like we have nothing to read.
                self.readLock.release()
                self.socketLock.release()
                return ''

        # Collect the content:
        data = self.readBuffer[:contentLength]

        # Truncate the remaining data:
        self.readBuffer = self.readBuffer[contentLength + 1:]

        # Release our thread locks:
        self.readLock.release()
        self.socketLock.release()

        try:
            return data.decode('utf-8')
        except UnicodeDecodeError:
            return ''

    def __writeNow(self, data, timeout=None):
        # Acquire a write lock so nothing intervenes:
        self.writeLock.acquire()

        self.socket.settimeout(timeout)

        # Ensure the data ends with a new line:
        if not data.endswith('\n'):
            data += '\n'

        while data:
            try:
                sent = self.socket.send(data)
            except:
                break
            if sent == 0:
                break
            data = data[sent:]

        # Release our write lock:
        self.writeLock.release()

    def __writeThread(self):
        while True:
            self.writeSemaphore.acquire()

            # Ensure we have a request in the write queue:
            if not self.writeQueue:
                continue

            request = self.writeQueue.pop(0)

            terminate = request.get('terminate')
            if terminate is not None:
                # Clear the write queue, and stop:
                self.writeQueue = []
                terminate.set()
                break

            # Write the data to the socket:
            data = request.get('data')
            if data:
                self.__writeNow(data, timeout=request.get('timeout'))

    def write(self, data, timeout=None):
        """
        Add data to the write queue.
        """
        self.writeQueue.append({'data': data, 'timeout': timeout})
        self.writeSemaphore.release()

    def writeHTTPResponse(self, body, contentType=None, code=200):
        """
        Write an HTTP response to the socket.
        """
        response = 'HTTP/1.1 %d %s\r\n' % (code, httplib.responses.get(code))

        # Add the standard headers:
        response += 'Date: %s\r\n' % time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime())
        response += 'Server: TTS-RPCServer/0.1\r\n'

        # Add the content headers:
        response += 'Content-Length: %d\r\n' % len(body)
        if contentType is not None:
            response += 'Content-Type: %s\r\n' % contentType

        # Add the body:
        response += '\r\n' + body

        # Finally, send it out:
        self.write(response, timeout=5)

    def writeHTTPError(self, code):
        """
        Write an HTTP error response to the socket.
        """
        self.notify.warning('Received a bad HTTP request: ' + str(code))
        body = '%d %s' % (code, httplib.responses.get(code))
        self.writeHTTPResponse(body, contentType='text/plain', code=code)

    def writeJSONResponse(self, response, id=None):
        """
        Write a JSON response object to the socket.
        """
        response.update({'jsonrpc': '2.0', 'id': id})
        try:
            body = json.dumps(response, encoding='latin-1')
        except TypeError:
            self.writeJSONError(-32603, 'Internal error')
            return
        self.writeHTTPResponse(body, contentType='application/json')

    def writeJSONError(self, code, message, id=None):
        """
        Write a JSON error response object to the socket.
        """
        self.notify.warning('Received a bad JSON request: %d %s' % (code, message))
        response = {'error': {'code': code, 'message': message}}
        self.writeJSONResponse(response, id=id)

    def close(self):
        """
        Wait until the write queue is empty, then shutdown and close our
        socket.
        """
        terminate = threading2.Event()
        self.writeQueue.append({'terminate': terminate})
        self.writeSemaphore.release()
        terminate.wait()

        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except socket.error:
            pass
        self.socket.close()

    def dispatchUntilEmpty(self):
        """
        Read and dispatch until there is nothing left.
        """
        while True:
            data = self.read(timeout=5)

            if not data:
                # We have nothing left to read.
                break

            try:
                request = json.loads(data)
            except ValueError:
                self.writeJSONError(-32700, 'Parse error')
                continue

            request = ToontownRPCRequest(
                self, request.get('method'), params=request.get('params') or (),
                id=request.get('id'), notification=('id' not in request))
            self.dispatcher.dispatch(request)


class ToontownRPCRequest:
    def __init__(self, connection, method, params=(), id=None, notification=False):
        self.connection = connection
        self.method = method
        self.params = params
        self.id = id
        self.notification = notification

    def result(self, result):
        """
        Write a result response object to the connection as long as this isn't
        a notification.
        """
        if not self.notification:
            self.connection.writeJSONResponse({'result': result}, id=self.id)

    def error(self, code, message):
        """
        Write an error response object to the connection as long as this isn't
        a notification.
        """
        if not self.notification:
            self.connection.writeJSONError(code, message, id=self.id)
