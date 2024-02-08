
from fastapi.responses import HTMLResponse
import typer
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates

from adapters.cookies_repository import CookiesRepository
from adapters.sentences_repository import InMemorySentencesRepository

app = FastAPI()
repository = InMemorySentencesRepository()
cookiesRepo = CookiesRepository()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def init(request: Request):
    respuesta = repository.get_sentence()
    context = {
        "request": request,
        "sentence": respuesta.sentence
    }
    response = templates.TemplateResponse("index.html", context)
    if cookiesRepo.check_cookie(request) is False:
        response.set_cookie(key="adivina_libros", value=cookiesRepo.generate_cookie(), httponly=True)
    return response

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

    resp = templates.TemplateResponse("result.html", context)
    if resultado_bool:
        resp.set_cookie(key="adivina_libros", value=cookiesRepo.update_cookie_correct(request), httponly=True)
    else:
        resp.set_cookie(key="adivina_libros", value=cookiesRepo.update_cookie_incorrect(request), httponly=True)

    return resp

@app.post("/search-title", response_class=HTMLResponse)
def search(request: Request, response: str = Form(...)):
    sugerencias=repository.search_title(response)
    context = {
        "request": request,
        "suggestions": sugerencias
    }
    return templates.TemplateResponse("suggestions.html", context)

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

