from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request
from starlette.types import ASGIApp
from libs.utils.logger.log_manager import request_id_var, request_path_var
import uuid

class RequestDataMiddleware(BaseHTTPMiddleware):

    """
    Middleware to capture request data such as request ID and path.
    
    This middleware generates a unique request ID for each incoming request
    and stores it in a thread-local variable. It also captures the request path
    and stores it in a thread-local variable for logging purposes.
    The request ID and path can be accessed later in the application using
    
    """


    def __init__(self,app:ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        """
        Dispatch method to handle the request and response cycle.
        It generates a unique request ID and captures the request path.
        Args:
            request (Request): The incoming request object.
            call_next (RequestResponseEndpoint): The next middleware or endpoint to call.

        Returns:
            Response: The response object returned by the next middleware or endpoint.

        """

        request_id_var.set(str(uuid.uuid4()))
        request_path_var.set(request.url.path)
        try:
            response = await call_next(request)
            return response
        except Exception as e:
           
            raise e
