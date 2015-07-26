# Toontown World Launcher (Windows/Linux python version)

"""
TODO LIST:

    - Get mirai python built with _ssl and bz2
    - Fix up patcher.
    - Graphical User Interface (inb4 python needs m0ar)
"""

from fsm.FSM import FSM
import settings
import localizer
import messagetypes
import urllib, urllib2 # Heh...
import httplib
import json
import sys
import os
import subprocess
import threading
import time

# Temporary Modules
import getpass

class TTWLauncher(FSM):
    """
    This is the "main" class that powers the toontown world launcher. It manages
    everything the launcher needs to do, including manage all the "sub-threads" that
    carry out tasks such as patching.

    As of right now, the launcher consists of 3 threads:

        - "main-thread": This is the thread which holds this class, and keeps everything
        running properly. This also manages state transitions as well as submitting
        data to and from the web server.

        - "graphical": This thread will hold the GUI side of the launcher, such as abs
        wyPython interface. Usually, this is what the end user will see when running the
        launcher.

        - "patcher": Since the majority of the patching process is locking, it has to be
        run on a separate thread to keep the main thread alive. This thread will deal with
        all the files it needs to download, as well as update/patch. During the download
        process, the patcher will also report back the current download percentage of the
        current file it is downloading.

    ERR001: This occurs when the website returns broken JSON.
    ERR002: This occurs when the website returns a Non-OK response when authenticating.
    ERR003: We got a response, but the data received was invalid.
    ERR004: The response said our login was invalid (failed).
    ERR005: User tried to submit TFA code without entering anything.
    ERR006: Account server is temporarily unavailable (HTTP 503).
    """

    def __init__(self, input, output):
        # We have to create an instance our FSM class.
        FSM.__init__(self)

        # input is a Queue of stuff coming from the gui to us
        self.input = input
        # output is a Queue of stuff we're sending to the gui
        self.output = output

        # This is a dict of the FSM itself. It describes what state can transition to
        # another state, for example, Off can go to CheckForUpdates or Off.
        self.transitions = {
            'Off' : ['CheckForUpdates', 'Off', 'LaunchGame'],
            'CheckForUpdates' : ['Patch', 'Off'],
            'GetCredentials' : ['SubmitCredentials', 'Off'],
            'SubmitCredentials' : ['LoginResponse', 'Off'],
            'LoginResponse' : ['GetCredentials',  'GetTFACode', 'Delayed', 'LaunchGame', 'Off'],
            'GetTFACode' : ['SubmitTFACode', 'Off'],
            'SubmitTFACode' : ['LoginResponse', 'Off'],
            'Delayed' : ['CheckQueue', 'Off'],
            'CheckQueue' : ['LoginResponse', 'Off'],
            'Patch' : ['GetCredentials', 'Off'],
            'LaunchGame' : ['GetCredentials', 'Off'],
        }

        # This probably wasn't needed, but since I had used self.version prior to
        # introducing the settings module, the configuration for version is set here.
        self.version = settings.Version

        # Create a secured connection (to be used for logins) to the endpoint specified
        # in the settings configuration. Note that this should be a tuple of:
        # (domain, port) (do not include "https://"!)
        self.connection = None

        # These are place holder attributes that the launcher uses during its login
        # process. If these are set to None, and it attempts to do something with these
        # attributes, then the Launcher FSM will come to a Halt and transition to the
        # "Off" state.
        self.gameserver = None
        self.cookie = None
        self.authToken = None
        self.authBanner = None
        self.appToken = None
        self.queueToken = None

        # These are place holder attributes for the separate threads that the launcher
        # will be running. In this case, we will have a patcher thread to handle all
        # the patching we have to do, and an interface thread to display a pretty GUI
        # to the end-user.
        self.patcher = None
        self.interface = None

        # If the user ever crashes, we can automatically log them back in without any
        # credential input. Sort of like a "remember me".
        self.credentials = None

        self.dontClearMessage = False

    # Send output to the GUI, blocking for no more than half a second
    def sendOutput(self, data):
        self.output.put(data, block=True, timeout=0.5)

    def start(self):
        # Open the GUI just to show the user that the process is active.
        self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))
        # Begin by checking for any updates to the launcher itself.
        self.request('CheckForUpdates')

    def enterCheckForUpdates(self):
        def versionCmp(v1, v2):
            v1b = v1.split('.')
            v2b = v2.split('.')
            if len(v1b) != len(v2b):
                return None # rip
            for i in xrange(len(v1b)):
                v1bb = int(v1b[i])
                v2bb = int(v2b[i])
                if v1bb == v2bb:
                    pass
                elif v1bb < v2bb:
                    # v1 version portion is larger than v2's, so no need to check rest of range
                    return False
                elif v1bb > v2bb:
                    # v1 version portion (remote) is bigger than a v2, we're out of date
                    return True
            return False

        # We only need to check for updates if we're actually setting a version string.
        if self.version is not None:
            # Download the JSON file containing the Launcher versions.
            # An example of this launcher JSON file can be found here:
            # download.toontownworldonline.com/launcher/windows/ttw_launcher.json
            # N.B.: This is blocking and will block the main thread until it downloads
            # the file in to memory!
            try:
                data = urllib2.urlopen(settings.JSONLauncherInfo)
            except:
                # If we weren't able to get the data, that's fine, just launch anyway
                self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.UnableToCheckForUpdates))
                self.dontClearMessage = True
                self.request('Patch')
                return

            try:
                # Try to load the data we got back in to a Pythonic dict from JSON.
                data = json.load(data)
            except:
                # An exception was raised during the JSON -> Pythonic dict process.
                # Perhaps the website returned invalid data?
                self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR001: %s" % localizer.ERR_JSONParseError))
                self.request('Patch')
                return

            if versionCmp(data[0].get('version', '0.0.0'), self.version):
                # There is a version mismatch between the launcher's version and
                # the version described in the JSON manifest. Alert the user that
                # there is an update available, open up to the download page and
                # then exit.
                self.sendOutput(
                    (messagetypes.LAUNCHER_VERSION_UPDATE,
                        data[0].get('version'),
                        data[0].get('rnotes'),
                        data[0].get('update', settings.DefaultDownloadLocation)
                    )
                )
                self.request('Off')

        # Alright, all seems well. We have no updates available (either because
        # version is None or there was no version mismatch). Continue our login
        # journey!
        self.request('Patch')

    def enterGetCredentials(self):
        # Clear out the status label
        if self.dontClearMessage:
            self.dontClearMessage = False
        else:
            self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))

        if self.credentials is None:
            username, password = self.input.get(block=True, timeout=None) # block until GUI sends input
            self.credentials = username, password
        else:
            username, password = self.credentials
        self.request('SubmitCredentials', username, password)

    def enterSubmitCredentials(self, username, password):
        # Notify the GUI
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Authing))

        # Create the connection to the SSL secured server to get our cookie and gameserver
        # IP address.
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)

        # This is the data we will be sending to the web server to submit our credentials.
        # Though the dict names should make it obvious as to what each one is, the first
        # is for all the Headers we will be sending to the web server (this can include
        # security-level headers) and the second is simply a POST of our username and
        # password.
        headers = {
            # Tell the webserver that we're submitting a urlencoded form.
            'Content-type': 'application/x-www-form-urlencoded',
        }
        # N.B.: The data should always be encoded/encrypted some way or another, as it
        # has a *raw* password! We don't want any man-in-the-middle attacks to steal our
        # users passwords. :(
        params = urllib.urlencode({
            'username': username,
            'password': password,
        })
        # Submit our headers/data through the secured connection we created at the start.
        self.connection.request('POST', settings.LoginPostLocation, params, headers)

        # Venture forth to see what the web server returns.
        self.request('LoginResponse')

    def enterLoginResponse(self):
        try:
            # Lets attempt to read the response that the web server gave us when we submitted
            # our authentication data.
            response = self.connection.getresponse()
        except httplib.BadStatusLine:
            # Something went wrong... The website returned a bad status. Lets just start over
            # and ask the user to enter their credentials again.
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR006: %s" % localizer.ERR_AccServerDown))
            self.credentials = None
            self.request('GetCredentials')

        if response.status == httplib.SERVICE_UNAVAILABLE:
            # The web server we tried to contact returned a 503, meaning the service is
            # currently unavailable. This means we are unable to login, exit the launcher.
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR006: %s" % localizer.ERR_AccServerDown))
            self.credentials = None
            self.request('GetCredentials')

        if response.status != httplib.OK:
            # The web server returned a Non-OK (200) response status. Alert the user and
            # exit the launcher.
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR002: %s" % localizer.ERR_Non200Resp % {'response':str(response.status)}))
            self.credentials = None
            self.request('GetCredentials')

        try:
            # We got an OK status from the website, meaning that we received something.
            # Lets find out if it's really what we're looking for.
            data = json.loads(response.read())
        except:
            # Uh-oh. This isn't JSON. The web server is doing something stupid.
            # Lets exit for now.
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR001: %s" % localizer.ERR_JSONParseError))
            self.request('Off')

        # Attempt to get the success status from the JSON we received. If there's no
        # success key, default to false, meaning we failed.
        success = data.get('success', 'false')

        # Clean up our connection that we no longer need.
        self.connection.close()
        self.connection = None

        if success == 'true':
            # Woo-hoo! We finally logged in successfully.

            # Store our cookie and gameserver as attributes on the launcher so we
            # can use them to login properly.
            self.cookie = data.get('cookie', 'NoCookieGiven')
            self.gameserver = data.get('gameserver', 'NoServerGiven')

            # Now we need to make sure our files aren't out of date (or if we even have
            # the files).
            self.request('LaunchGame')

        elif success == 'false':
            self.sendOutput((messagetypes.LAUNCHER_ERROR, data.get('banner', localizer.ERR_InvalidLogin)))

            # Lets go back to getting the credentials, but first clear out the stored ones so we don't just spam web
            self.credentials = None
            self.request('GetCredentials')
            self.sendOutput((messagetypes.LAUNCHER_CLEAR_PASSWORD))

        elif success == 'partial':
            # TFA has kicked in, RIP us.
            self.authToken = data.get('responseToken', None)
            self.authBanner = data.get('banner', '')
            self.request('GetTFACode')

        elif success == 'delayed':
            # RIP, the queue system has kicked in.
            #position = int(data.get('position', 0))
            eta = int(data.get('eta', 5))
            self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Queue % (eta))) #(position, eta) - disabled position for simplicity as it was mostly meaningless to a player
            self.queueToken = data.get('queueToken', None)
            self.request('Delayed', eta)

    def enterGetTFACode(self):
        if self.authToken is None:
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR005: %s" % localizer.ERR_TFAWithoutToken))
            self.request('Off')
        self.sendOutput((messagetypes.LAUNCHER_STATUS, ''))
        self.sendOutput((messagetypes.LAUNCHER_REQUEST_TFA, self.authBanner))
        self.appToken = self.input.get(block=True, timeout=None) # block until GUI sends input
        if self.appToken is None:
            # User cancelled trying to login with tfa, clear out
            self.credentials = None
            self.request('GetCredentials')
        self.request('SubmitTFACode')

    def enterSubmitTFACode(self):
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_Authing))
        # Create the connection to the SSL secured server to get our cookie and gameserver
        # IP address.
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
        }
        params = urllib.urlencode({
            'appToken': self.appToken,
            'authToken': self.authToken,
        })
        self.connection.request('POST', settings.LoginPostLocation, params, headers)
        self.request('LoginResponse')

    def enterDelayed(self, timeDelay):
        if self.queueToken is None:
            self.sendOutput((messagetypes.LAUNCHER_ERROR, "ERR007: %s" % localizer.ERR_DelayWithoutToken))
            self.request('Off')
        time.sleep(max(timeDelay, 1)) # Sleep for at least 1 second
        self.request('CheckQueue')

    def enterCheckQueue(self):
        # Create the connection to the SSL secured server to get our cookie and gameserver
        # IP address.
        self.connection = httplib.HTTPSConnection(*settings.SSLConnection)

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
        }
        params = urllib.urlencode({
            'queueToken': self.queueToken,
        })
        self.connection.request('POST', settings.LoginPostLocation, params, headers)
        self.request('LoginResponse')

    def enterPatch(self):
        from patcher import Patcher
        self.patcher = threading.Thread(target=Patcher.Patch, name="Patcher-Thread", args=(self.__updateProgress, self.__updateFile))
        self.patcher.daemon = True
        self.patcher.start()

        # Loop main thread until patcher is complete.
        while self.patcher.isAlive():
            time.sleep(0.2)

        self.request('GetCredentials')

    def __updateProgress(self, percentage):
        if self.output.empty(): # Only send an update after other updates have been consumed
            self.sendOutput((messagetypes.LAUNCHER_PROGRESS, percentage))

    def __updateFile(self, fileCount):
        # Updates the 'file n of 30' message
        if self.output.empty(): # Only send an update after other updates have been consumed
            self.sendOutput((messagetypes.LAUNCHER_STATUS, fileCount))

    def enterLaunchGame(self):
        os.environ['TTR_PLAYCOOKIE'] = self.cookie
        os.environ['TTR_GAMESERVER'] = self.gameserver
        if sys.platform == 'win32': # creationflags is only supported on Windows
            game = subprocess.Popen('TTWEngine', creationflags=0x08000000)
        else:
            game = subprocess.Popen('TTWEngine')
        self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_PlayGameFarewell))
        time.sleep(1) # Sleep so the "Have Fun!" can be read
        self.sendOutput((messagetypes.LAUNCHER_HIDE))
        # Check game health every second
        while game.poll() is None:
            # Game hasn't died yet
            time.sleep(1.5)
        # Game is rip?
        if game.returncode == 0:
            # Clean exit, just bring ourselves back up to play again
            self.sendOutput((messagetypes.LAUNCHER_CLEAR_PASSWORD))
            self.sendOutput((messagetypes.LAUNCHER_SHOW))
            self.sendOutput((messagetypes.LAUNCHER_ENABLE_CONTROLS))
            self.credentials = None # We set this to none so that we don't immediately boot again, and end up waiting on the GUI
            self.dontClearMessage = True
            self.sendOutput((messagetypes.LAUNCHER_STATUS, localizer.GUI_PlayAgain))
            time.sleep(1.5)
            self.request('GetCredentials')
            return
        # Ask the user if they want us to try again.
        self.sendOutput((messagetypes.LAUNCHER_SHOW))
        self.sendOutput((messagetypes.LAUNCHER_PLAY_RETRY))
        # If they say no, the app terminates, so the else block isn't super useful
        if self.input.get(block=True, timeout=None):
            self.request('GetCredentials')
        else:
            self.request('Off')

    def enterOff(self):
        if self.connection is not None:
            self.connection.close()
        self.sendOutput((messagetypes.LAUNCHER_EXIT))
