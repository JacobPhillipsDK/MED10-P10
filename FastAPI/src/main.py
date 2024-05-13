from fastapi import FastAPI, HTTPException
from starlette.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Union
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/html", StaticFiles(directory="static/html"), name="html")
app.mount("/images", StaticFiles(directory="static/images"), name="images")
app.mount("/javascript", StaticFiles(directory="static/javascript"), name="javascript")
app.mount("/javascript/geodata", StaticFiles(directory="static/javascript/geodata"), name="geodata")

@app.get("/")
async def redirect_to_html():
    return RedirectResponse(url="/html/index.html")

@app.get("/api/get_path")
def get_path(startPos: str, endPos: str):
    return {"startPos": startPos, "endPos": endPos}

