class LastVisitedMiddleware(object):
    """This middleware sets the last visited url as session field"""

    def process_request(self, request):
        """Intercept the request and add the current path to it"""
        request_path = request.get_full_path()
        try:
            request.session['last_visited'] = request.session['currently_visiting']
        except KeyError:
            # silence the exception - this is the users first request
            pass
        
    	request.session['currently_visiting'] = request_path
    	
    	
    