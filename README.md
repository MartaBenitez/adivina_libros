# Adivina-Libros ![Static Badge](https://img.shields.io/badge/status-en_desarrollo-teal)

Juego para adivinar un libro en función de la primera frase del mismo.

## Índice

- [Tecnologías empleadas](#tecnologías-empleadas)
- [Instalación](#instalación)
- [Cómo jugar](#cómo-jugar)

## Tecnologías empleadas

- [Python][python] versión 3.10.12
- [HTMX][htmx]
- [FastApi][fastapi] con [Uvicorn][uvicorn]

## Instalación

1. Crear entorno virtual `.venv`

2. Variables de entorno

    Fichero `.env`:

    ```bash
    URL_OPENLIBRARY_API=https://openlibrary.org/
    ```

3. Dependencias

    ```bash
    pip install fastapi
    pip install uvicorn
    pip install typer
    pip install jinja2
    pip install python-multipart
    ```

4. Fichero `launch.json` para debug

    ```bash
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python Debug",
                "type": "python",
                "request": "launch",
                "program": "app/run.py",
                "console": "integratedTerminal",
                "justMyCode": true
            }
        ]
    }
    ```

5. Fichero `settings.json` para debug

    ```bash
    {
        "python.analysis.extraPaths": [
            "./app"
        ]
    } 
    ```

## Cómo jugar

[python]: https://www.python.org/
[htmx]: https://htmx.org/
[fastapi]: https://fastapi.tiangolo.com/
[uvicorn]: https://www.uvicorn.org/