# build
build: build-app
build-app:
	npm --prefix app run build
build-client:
	pio run -d client

# develop
dev: start-redis start-sql dev-api dev-app
dev-api:
	uvicorn api.src.main:app --reload
dev-app:
	npm --prefix app run dev

# start
start:
	docker compose up -d --build
start-api:
	docker compose up -d api
start-redis:
	docker compose up -d redis
start-sql:
	docker compose up -d sql

#stop
stop:
	docker compose down
stop-api:
	docker compose stop api
stop-redis:
	docker compose stop redis
stop-sql:
	docker compose stop sql

# test
test-api:
	pytest

# lint
lint-api:
	black api

# watch
watch:
	pio device monitor -b 115200

# upload
upload:
	pio run -d client -t upload