FROM python:3.10-slim

WORKDIR /src
EXPOSE 8000

RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml src ./
RUN poetry install --no-dev

CMD ["gunicorn", "app.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]