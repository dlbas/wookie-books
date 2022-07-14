FROM python:3.10-slim

WORKDIR /src
EXPOSE 8000

RUN pip install poetry && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml src ./
RUN poetry install

CMD ["uvicorn", "--host", "0.0.0.0", "app.main:app"]