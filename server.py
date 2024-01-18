from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import uvicorn
import sqlite_helpers as helpers
from fastapi.testclient import TestClient
from hash import create_alias
from args import get_args
from enums import HttpStatus, code_to_enum
import logging
import time
from metrics import MetricsHandler

app = FastAPI()

args = get_args()
DATABASE = args.database_file
helpers.create_table(DATABASE)


@app.post('/create_url')
async def create_url(request: Request):
    try:
        with MetricsHandler.query_time.labels("create").time():
            data = await request.json()
            logging.debug(f"Received data for creating url: {data}")
            url = data.get("url", None)
            alias = data.get("alias", None)

            if (url is None):  # url not provided
                raise ValueError("Url not provided.")

            if (args.disable_random_alias):  # if random alias is disabled
                if (alias is None):
                    raise ValueError("Alias is required.")

            if (helpers.alias_exists(DATABASE, alias)):  # alias exists
                raise HTTPException(
                    status_code=HttpStatus.INVALID.code, detail="Alias already exists.")

            if (alias is None):  # creates random alias if not given.
                logging.debug("Generating random alias.")
                alias = create_alias(url)

            helpers.insert_url(DATABASE, url, alias)
            MetricsHandler.url_count.inc()
            logging.info(f"URL created successfully: {url}, Alias: {alias}")
            return {"url": url, "alias": alias}

    except ValueError as e:
        logging.exception(f"ValueError: {str(e)}")
        MetricsHandler.http_code.labels("BAD REQUEST").inc()
        raise HTTPException(
            status_code=HttpStatus.BAD_REQUEST.code, detail=str(e))
    except HTTPException as e:
        logging.exception(f"HTTPException: {str(e.detail)}")
        MetricsHandler.http_code.labels("INVALID").inc()
        raise e
    except Exception as e:
        logging.exception(f"Internal server error: {str(e)}")
        MetricsHandler.http_code.labels(
            "INTERNAL_SERVER_ERROR").inc()
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.code, detail=str(e))


@app.get('/list_all')
def list_all():
    try:
        with MetricsHandler.query_time.labels("list").time():
            logging.debug("Listing the alias and urls.. ")
            url_list = helpers.list_alias_url(DATABASE)
            return {"url_list": url_list}
    except Exception as e:
        logging.exception("Unable to list the urls and aliases")
        MetricsHandler.http_code.labels(
            "INTERNAL_SERVER_ERROR").inc()
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.code, detail=str(e))


@app.get('/find/{alias}')
def find_alias(alias: str):
    try:
        with MetricsHandler.query_time.labels("find").time():
            logging.debug(f"Finding alias: {alias}")
            target_url = helpers.alias_to_url(DATABASE, alias)
            return RedirectResponse(url=target_url)
    except ValueError as e:
        logging.exception("Alias not found in find alias")
        MetricsHandler.http_code.labels("NOT_FOUND").inc()
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.code, detail="Alias not found.")
    except Exception as e:
        logging.exception(f"Internal server error while finding alias")
        MetricsHandler.http_code.labels(
            "INTERNAL_SERVER_ERROR").inc()
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.code, detail=str(e))


@app.post('/delete/{alias}')
def delete_alias(alias: str):
    try:
        with MetricsHandler.query_time.labels("delete").time():
            logging.debug(f"Deleting alias: {alias}")
            if (helpers.delete_alias(DATABASE, alias)):
                return {f"Alias {alias} was deleted successfully."}
            else:
                raise KeyError("Alias not found")
    except KeyError as e:
        logging.exception("Alias not found in delete alias")
        MetricsHandler.http_code.labels("NOT_FOUND").inc()
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.code, detail=str(e))
    except Exception as e:
        logging.exception(f"Internal server error while deleting alias")
        MetricsHandler.http_code.labels(
            "INTERNAL_SERVER_ERROR").inc()
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.code, detail=str(e))


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception):
    status_code = exception.status_code
    status_enum = code_to_enum.get(status_code)
    status_description = status_enum.description

    return HTMLResponse(content=status_description, status_code=status_code)

logging.Formatter.converter = time.gmtime

logging.basicConfig(
    format="%(asctime)s.%(msecs)03dZ %(levelname)s:%(name)s:%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.ERROR - (args.verbose*10),
)

if __name__ == "__main__":
    logging.info(f"Server started on {args.host} {args.port}")
    uvicorn.run("server:app", host=args.host, port=args.port, reload=True)

# we have a separate __name__ check here due to how FastAPI starts
# a server. the file is first ran (where __name__ == "__main__")
# and then calls `uvicorn.run`. the call to run() reruns the file,
# this time __name__ == "server". the separate __name__ if statement
# is so the thread references the same instance as the global
# metrics_handler referenced by the rest of the file. otherwise,
# the thread interacts with an instance different than the one the
# server uses

if __name__ == "server":
    initial_url_count = helpers.get_number_of_entries(DATABASE)
    MetricsHandler.url_count.inc(initial_url_count)
