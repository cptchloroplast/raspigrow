FROM python:3.10-bullseye as build
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry export -o requirements.txt
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

FROM python:3.10-slim-bullseye as release
ENV PYTHONUNBUFFERED True
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /home
COPY . .
CMD uvicorn --factory main:create_api --host 0.0.0.0
