from enum import Enum, auto


class HttpStatus(Enum):
    OK = 200
    NOT_FOUND = 404
    INVALID = 422
    BAD_REQUEST = 400
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500
