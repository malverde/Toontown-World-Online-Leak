from direct.directnotify.DirectNotifyGlobal import directNotify


class ToontownRPCDispatcher:
    notify = directNotify.newCategory('ToontownRPCDispatcher')

    def __init__(self, handler):
        self.handler = handler

    def dispatch(self, request):
        """
        Handle a JSON-RPC 2.0 request.
        """
        if (not isinstance(request.method, basestring)) or \
           (not isinstance(request.params, (tuple, list, dict))):
            request.error(-32600, 'Invalid Request')
            return

        # Grab the method from the handler:
        method = getattr(self.handler, 'rpc_' + request.method, None)
        if method is None:
            request.error(-32601, 'Method not found')
            return

        # Find the token in the params, authenticate it, and then remove it
        # from the params:
        token = None
        if isinstance(request.params, dict):
            token = request.params.get('token')
            del request.params['token']
        elif len(request.params) > 0:
            token = request.params[0]
            params = request.params[1:]
        if not isinstance(token, basestring):
            request.error(-32000, 'No token provided')
            return
        error = self.handler.authenticate(token, method)
        if error is not None:
            # Authentication wasn't successful. Send the error:
            request.error(*error)
            return

        # Finally, attempt to call the method:
        try:
            if isinstance(params, dict):
                request.result(method(**params))
            else:
                request.result(method(*params))
        except:
            request.error(-32603, describeException())
