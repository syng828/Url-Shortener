from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import sqlite_helpers as helpers
from fastapi.testclient import TestClient

app = FastAPI()

DATABASE = "urls.db"
helpers.create_table(DATABASE)


@app.post('/create_url')
async def create_url(request: Request):
    try:
        data = await request.json()
        url = data["url"]
        alias = data["alias"]
        helpers.insert_url(DATABASE, url, alias)
        return {"url": url, "alias": alias}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/list_all')
def list_all():
    try:
        url_list = helpers.list_alias_url(DATABASE)
        return {"url_list": url_list}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/find/{alias}')
def find_alias(alias: str):
    try:
        url = helpers.alias_to_url(DATABASE, alias)
        return {"url": url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post('/delete/{alias}')
def delete_alias(alias: str):
    try:
        helpers.delete_alias(alias)
        return {f"Alias {alias} was deleted successfully."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
