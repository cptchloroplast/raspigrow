# build
build: build-app
build.app:
	npm --prefix app run build
build.client:
	pio run -d client

# start
start:
	docker compose up -d --build
start.api:
	docker compose up -d api --build
start.worker:
	docker compose up -d worker --build
start.redis:
	docker compose up -d redis
start.sql:
	docker compose up -d sql

#stop
stop:
	docker compose down
stop.api:
	docker compose stop api
stop.worker:
	docker compose stop worker
stop.redis:
	docker compose stop redis
stop.sql:
	docker compose stop sql

# test
test.server:
	pytest

# lint
lint.server:
	black server

# watch
watch:
	pio device monitor -b 115200

# upload
upload:
	pio run -d client -t upload