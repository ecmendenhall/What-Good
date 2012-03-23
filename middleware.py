import os

class LastVisitedMiddleware(object):
    """This middleware sets the last visited url as session field"""

    def process_request(self, request):
        """Intercept the request and add the current path to it"""
        #request_path = request.get_full_path()
        #try:
        #    request.session['last_visited'] = request.session['currently_visiting']
        #except KeyError:
        #    # silence the exception - this is the users first request
        #    pass
        #
    	#request.session['currently_visiting'] = request_path
    	
    	current_request = request.get_full_path()
        if '.' not in os.path.split(current_request)[1]:
            last = request.session.get("currently_visiting", None)
            request.session['last_visited'] = last
        request.session['currently_visiting'] = request.get_full_path()

    