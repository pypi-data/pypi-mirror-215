import http

# Error types return from dingman
DEFAULT_ERR_CODE = 100  # unknown
DEFAULT_ERR_TYPE = 'Unknown'
BAD_REQUEST = 'Bad Request'
NOT_FOUND = 'Not Found'
UNAUTHORIZED = 'Unauthorized'
BAD_GATEWAY = 'Bad Gateway'
CONFLICT = 'Conflict'
UNPROCESSABLE_ENTITY = 'Unable to Reach gRPC Server'


class DingmanGRPCError(Exception):
    """DingmanGRPCError returned the base Error Model for Dingman gRPC related error.
    """
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg
        self.err_type = DEFAULT_ERR_TYPE
        self.err_code = DEFAULT_ERR_CODE
        self.http_status_code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    def __str__(self):
        return self.err_type + ' - ' + self.msg


class InvalidGRPCResponseError(DingmanGRPCError):
    """InvalidGRPCResponseError returned when upstream gRPC returns an 
    invalid/unexpected response.
    """
    def __init__(self, msg):
        super().__init__(msg)
        self.err_type = BAD_GATEWAY
        self.err_code = 900
        self.http_status_code = http.HTTPStatus.BAD_GATEWAY


# class GRPCResponseError(DingmanGRPCError):
#     """GRPCResponseError returned when upstream gRPC returns a valid response,
#     but the operation was not successful (i.e business layer error).
#     """
#     pass


class GRPCUpstreamError(DingmanGRPCError):
    """GRPCUpstreamError returned when failing to connect to upstream gRPC server.
    """
    def __init__(self, msg):
        super().__init__(msg)
        self.err_type = UNPROCESSABLE_ENTITY
        self.err_code = 901
        self.http_status_code = http.HTTPStatus.UNPROCESSABLE_ENTITY
