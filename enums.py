from enum import Enum, auto


class HttpStatus(Enum):
    OK = (200, "<h1>200 Ok</h1>")
    NOT_FOUND = (404, "<h1> 404 Not found</h1>")
    INVALID = (422, "<h1>422 Invalid</h1>")
    BAD_REQUEST = (400, "<h1>400 Bad request</h1>")
    CONFLICT = (409, "<h1>409 Conflict</h1>")
    INTERNAL_SERVER_ERROR = (500, "<h1>500 Internal server error</h1>")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    def get_http_codes(code):
        code_to_enum_dict = {
            200: HttpStatus.OK,
            404: HttpStatus.NOT_FOUND,
            422: HttpStatus.INVALID,
            400: HttpStatus.BAD_REQUEST,
            409: HttpStatus.CONFLICT,
            500: HttpStatus.INTERNAL_SERVER_ERROR
        }
        return (code_to_enum_dict.get(code))
