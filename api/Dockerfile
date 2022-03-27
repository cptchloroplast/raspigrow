FROM python:3.9-alpine as build
RUN apk update
RUN apk add python3-dev gcc libc-dev
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r requirements.txt

FROM python:3.9-alpine as release
ENV PYTHONUNBUFFERED True
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /home
COPY . .
CMD uvicorn src.main:app --host 0.0.0.0
