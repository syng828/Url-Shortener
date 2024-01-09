from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
import sqlite_helpers as helpers
from fastapi.testclient import TestClient

app = FastAPI()

helpers.create_table()


@app.get('/')
def root():
    pass


@app.post('/create_url')
async def create_url(request: Request):
    try:
        data = await request.json()
        url = data["url"]
        alias = data["alias"]
        helpers.insert_url(url, alias)
        return {"url": url, "alias": alias}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/list_all')
def list_all():
    try:
        url_list = helpers.list_alias_url()
        return {"url_list": url_list}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get('/find/{alias}')
def find_alias(alias: str):
    try:
        url = helpers.alias_to_url(alias)
        return {"url": url}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post('/delete/{alias}')
def delete_alias(alias: str):
    try:
        helpers.delete_alias(alias)
        return {"The alias was deleted successfully."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, reload=True)

# testing
'''client = TestClient(app)

url = "/create_url"
data = {"url": "https://example.com", "alias": "example"}
response = client.post(url, json=data)

data = {"url": "https://google.com", "alias": "google"}
response = client.post(url, json=data)

url = "/delete/example"
response = client.post(url)

print(response.status_code)
print(response.json())'''
