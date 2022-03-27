# build
build: build-app
build-app:
	npm --prefix app run build

# develop
dev: start-redis dev-api dev-app
dev-api:
	uvicorn api.src.main:app --reload
dev-app:
	npm --prefix app run dev

# start
start:
	docker-compose up -d
start-build:
	docker-compose up -d --build
start-api:
	docker-compose up -d api
start-redis:
	docker-compose up -d redis

#stop
stop:
	docker-compose down
stop-api:
	docker-compose stop api
stop-redis:
	docker-compose stop redis