
from fastapi.responses import HTMLResponse
import typer
import uvicorn
from fastapi import FastAPI, Request, Form
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
    }
    return templates.TemplateResponse("index.html", context)

@app.get("/daily-sentence", response_class=HTMLResponse)
def sentence(request: Request):
    respuesta = repository.get_sentence()
    context = {
        "request": request,
        "sentence": respuesta.sentence
    }
    return templates.TemplateResponse("game.html", context)
    
@app.post("/user-response", response_class=HTMLResponse)
def response(request: Request, response: str = Form(...)):
    resultado_bool=repository.check_response(response)
    mensaje="Incorrecto"
    if resultado_bool:
        mensaje="Correcto"
    context = {
        "request": request,
        "result": mensaje
    }
    return templates.TemplateResponse("result.html", context)

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

