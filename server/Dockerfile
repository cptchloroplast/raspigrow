FROM python:3.10-bullseye as build
RUN apt update && apt install -y build-essential libssl-dev libffi-dev python3-dev cargo
RUN pip install --upgrade pip
RUN pip install poetry
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml poetry.lock ./

FROM build as development
RUN poetry export -o requirements.txt --dev
RUN pip install -r requirements.txt

FROM build as release
RUN poetry export -o requirements.txt
RUN pip install -r requirements.txt

FROM python:3.10-slim-bullseye as base
ENV PYTHONUNBUFFERED True
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /home
COPY . .

FROM base as server
COPY --from=release /opt/venv /opt/venv

FROM base as utility
COPY --from=development /opt/venv /opt/venv

FROM utility as test
ENV TEST_INTEGRATION=True
CMD pytest

FROM utility as migrations
CMD alembic upgrade head

FROM server as worker
CMD python main.py

FROM server as api
CMD uvicorn --factory main:create_api --host 0.0.0.0