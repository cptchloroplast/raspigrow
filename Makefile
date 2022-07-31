-include client/.env
export

# App
app.install:
	npm --prefix app install
app.build:
	npm --prefix app run build
app.start:
	docker compose up -d app
app.start.build:
	docker compose up -d app --build
app.stop:
	docker compose stop app
app.test:
	npm --prefix app test

# Server
server.install:
	cd server; poetry install
server.lint:
	black server
server.lint.check:
	black --check server
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
## Migrations
server.migrations.upgrade:
	cd server; alembic upgrade head

# Client
client.install:
	pio pkg install -d client
client.build:
	pio run -d client -e board
client.upload:
	pio run -d client -t upload -e board
client.watch:
	pio device monitor -b 115200
client.test:
	pio test -d client -e test

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

# MQTT
mqtt.start:
	docker compose up -d mqtt
mqtt.stop:
	docker compose stop mqtt

# Git Hooks
hooks.install:
	git config core.hooksPath .githooks
hooks.pre-commit: server.lint.check server.test client.test app.test