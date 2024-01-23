
from fastapi.responses import HTMLResponse
import typer
import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from adapters.sentences_repository import InMemorySentencesRepository
from domain.daily_sentence import DailySentence

app = FastAPI()
repository = InMemorySentencesRepository()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def init(request: Request):
    context = {
        "request": request,
        "sentence": ""
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/daily-sentence", response_class=HTMLResponse)
def sentence(request: Request):
    respuesta = repository.get_sentence()
    context = {
        "request": request,
        "sentence": respuesta.sentence
    }
    return templates.TemplateResponse("index.html", context)

@app.post("/user-response")
def response(rsp: str) -> bool:
    return repository.check_response(rsp)

def run_server() -> None:
    uvicorn.run(
        app,
        host="localhost",
        port=5050,
    )

def main() -> None:
    typer.run(run_server)


if __name__ == "__main__":
    main()

