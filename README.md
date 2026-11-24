# Pedidos: CSV → SQL → FastAPI + LLM

Pequeño proyecto en Python que genera un CSV de pedidos con errores, valida y limpia los datos y los almacena en SQLite, permitiendo hacer preguntas en lenguaje natural sobre ellos a través de una API con FastAPI y un LLM. Está orientado a preguntas sobre clientes y meses en relación con las ventas.

## Cómo ejecutarlo

Necesitas [uv](https://docs.astral.sh/uv/) instalado.

```bash
uv sync
cp .env.example .env                    # se requiere llenar las variables: LLM_API_KEY, LLM_BASE_URL y LLM_MODEL
uv run --env-file .env python run.py
```

`run.py` genera el CSV, lo limpia, lo carga en la base de datos y arranca la API. Después abre **http://127.0.0.1:8000** y escribe tu pregunta. La documentación de la API está en **http://127.0.0.1:8000/docs**. Se ha realizado una interfaz web sencilla para mejorar la experiencia de usuario.

Los pasos también se pueden ejecutar por separado:

```bash
uv run python -m csv_generator.csv_generator       # genera el CSV
uv run python -m cleaner_uploader.uploader         # limpia y carga en SQLite
uv run --env-file .env uvicorn api.main:app        # arranca la API
```

Tests:

```bash
uv run pytest -v
```

## Estructura

```
csv_generator/      genera el CSV de pedidos con errores a propósito
cleaner_uploader/   limpia los datos y los guarda en SQLite
sql/views.sql       vistas: ventas por mes y país, top 10 clientes
api/                API con FastAPI, llamada al LLM, validación y página web
tests/              tests con pytest
run.py              ejecutar todo de una vez
```

## Decisiones

- SQLite, porque no necesita servidor y viene incluido en Python.
- La limpieza está separada de la carga a la base de datos, para poder testear cada parte por separado.
- Solo se consideran ventas los pedidos completados.
- El SQL que genera el LLM se valida antes de ejecutarse (solo lectura y solo las tablas permitidas) y la base de datos se abre en modo solo lectura.
- El LLM se configura desde el `.env`, así cada persona puede usar su propio proveedor y clave.

## Qué haría con más tiempo

- Limitar el número de filas y el tiempo máximo de cada consulta.
- Redactar la respuesta en lenguaje natural con el LLM (requiere más tokens para las pruebas).
- Añadir Docker para facilitar la ejecución.

## Cómo usé la IA

Usé un asistente de IA como apoyo durante el proyecto. Yo le daba contexto y el código realizado por mí, sirviéndome para validar el código y confirmar mi desarrollo.

- **Qué le pedí:** configurar el proyecto con uv, revisar el código y los tests, y explicarme FastAPI viniendo de Django.
- **Qué acepté:** la estructura general, la validación de las consultas y la base de los tests.
- **Qué corregí:** renombré y separé módulos, simplifiqué partes que veía excesivas, cambié el proveedor del LLM por uno configurable y descarté una segunda llamada al LLM para no gastar más tokens.

## Tiempo utilizado
- 5 horas.