# App
app.build:
	docker build -t grow-app:latest app
app.build.src:
	npm --prefix app run build
app.start:
	docker compose up -d app
app.start.build:
	docker compose up -d app --build
app.stop:
	docker compose stop app

# Server
server.build:
	docker build -t grow-server:latest server
server.lint:
	black server
server.test:
	pytest server
## API
server.api.start:
	docker compose up -d api
server.api.start.build:
	docker compose up -d api --build
server.api.stop:
	docker compose stop api
## Worker
server.worker.start:
	docker compose up -d worker
server.worker.start.build:
	docker compose up -d worker --build
server.worker.stop:
	docker compose stop worker

# Client
client.build:
	pio run -d client
client.upload:
	pio run -d client -t upload
client.watch:
	pio device monitor -b 115200

# SQL
sql.start:
	docker compose up -d sql
sql.stop:
	docker compose stop sql

# Redis
redis.start:
	docker compose up -d redis
redis.stop:
	docker compose stop redis

# Git Hooks
pre-commit: server.lint server.test