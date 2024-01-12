from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import uvicorn
import sqlite_helpers as helpers
from fastapi.testclient import TestClient
from hash import create_alias
from args import get_args
from enums import HttpStatus

app = FastAPI()

args = get_args()
DATABASE = args.database_file
helpers.create_table(DATABASE)


@app.post('/create_url')
async def create_url(request: Request):
    try:
        data = await request.json()
        url = data.get("url", None)
        alias = data.get("alias", None)
        if (url is None):  # url not provided
            raise HTTPException(
                status_code=HttpStatus.BAD_REQUEST.value, detail="Url not provided.")
        if (helpers.alias_exists(DATABASE, alias)):  # alias exists
            raise HTTPException(
                status_code=HttpStatus.INVALID.value, detail="Alias already exists.")
        if (alias is None):  # creates random alias if not given.
            alias = create_alias(url)
        helpers.insert_url(DATABASE, url, alias)
        return {"url": url, "alias": alias}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.value, detail=str(e))


@app.get('/list_all')
def list_all():
    try:
        url_list = helpers.list_alias_url(DATABASE)
        return {"url_list": url_list}
    except Exception as e:
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.value, detail=str(e))


@app.get('/find/{alias}')
def find_alias(alias: str):
    try:
        target_url = helpers.alias_to_url(DATABASE, alias)
        return RedirectResponse(url=target_url)
    except ValueError as e:
        raise HTTPException(
            status_code=HttpStatus.NOT_FOUND.value, detail="Alias not found.")
    except Exception as e:
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.value, detail=str(e))


@app.post('/delete/{alias}')
def delete_alias(alias: str):
    try:
        if (helpers.delete_alias(DATABASE, alias)):
            return {f"Alias {alias} was deleted successfully."}
        else:
            raise HTTPException(
                status_code=HttpStatus.NOT_FOUND.value, detail="Alias not found")
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(
            status_code=HttpStatus.INTERNAL_SERVER_ERROR.value, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
