#!make
SHELL = /bin/sh
.DEFAULT: help

-include .env .env.local .env.*.local

# Defaults
DOCKER_COMPOSE = USERID=$(shell id -u):$(shell id -g) docker-compose ${compose-files}
LOAD_DATA = ./bin/loader run ${output-path} ${url} ${fixture-path}

.PHONY: help
help:
	@echo "StockBall pipeline"
	@echo ""
	@echo "Usage:"
	@echo "  docker.run.dependencies        - Run only InfluxDB and Grafana container.
	@echo "  load.data                      - Load event data from public sources.
	@echo "  docker.stop                    - Stop and remove all running containers from this project using docker-compose down (default env=${env})"
	@echo ""
	@echo "Note: Store protected environment variables in .env.local or .env.*.local"
	@echo ""

.PHONY: load.data
load.data:
	$(call LOAD_DATA) ${SOURCE-PATH} ${SOURCE-URL} ${FIXTURE-PATH}

.PHONY: docker.run.dependencies
docker.run.dependencies: d.compose.down
	make d.compose.up
	make docker.wait
	docker-compose up -d
	docker-compose ps

.PHONY: docker.stop
docker.stop: d.compose.down

.PHONY: d.compose.up
d.compose.up:
	$(call DOCKER_COMPOSE) up -d --remove-orphans

.PHONY: d.compose.down
d.compose.down:
	$(call DOCKER_COMPOSE) down -v || true
	$(call DOCKER_COMPOSE) rm --force || true
	docker rm "$(docker ps -a -q)" -f || true

.PHONY: docker.wait
docker.wait:
	./bin/docker-wait

.PHONY: docker.logs
docker.logs:
	./bin/docker-logs