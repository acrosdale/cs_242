import lucene


class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        # lucene.initVM()

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            # ge the vm context and use it for this thread
            lucene.getVMEnv().attachCurrentThread()
        except:
            lucene.initVM()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
