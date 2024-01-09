from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import sqlite_helpers as helpers

app = FastAPI()


@app.get('/')
def root():
    helpers.create_table()


@app.get('/create_url')
def create_url(url: str, alias: str):
    try:
        helpers.insert_url(url, alias)
        return JSONResponse(content={"url": url, "alias": alias})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/list_all')
def list_all():
    try:
        url_list = helpers.list_alias_url()
        return JSONResponse(content={"url_list": url_list})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/find/{alias}')
def find_alias(alias: str):
    try:
        url = helpers.alias_to_url(alias)
        return JSONResponse(content={"url": url})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/delete/{alias}')
def delete_alias(alias: str):
    try:
        helpers.delete_alias(alias)
        return JSONResponse(message={"The alias was deleted successfully."})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)
