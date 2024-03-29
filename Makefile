.PHONY: help
help:
		@echo "USAGE"
		@echo "    make <commands>"
		@echo ""
		@echo "AVAILABLE COMMANDS"
		@echo "build      Build services."
		@echo "up         Create and start containers in the background."
		@echo "start      Starts existing containers for a service."
		@echo "down       Stop and remove containers, networks."
		@echo "destroy    Remove named volumes declared in the volumes section of the Compose file and anonymous volumes attached to containers."
		@echo "stop       Stops running containers without removing them."
		@echo "restart    Restart containers."
		@echo "export-dep Exporting dependencies to start containers."

.PHONY: build
build:
		make export-dep
		docker-compose -f docker-compose-local.yaml build

.PHONY: up
up:
		make export-dep
		docker-compose -f docker-compose-local.yaml up -d

.PHONY: start
start:
		make export-dep
		docker-compose -f docker-compose-local.yaml start

.PHONY: down
down:
		docker-compose -f docker-compose-local.yaml down && docker network prune --force

.PHONY: destroy
destroy:
		docker-compose -f docker-compose-local.yaml down -v

.PHONY: stop
stop:
		docker-compose -f docker-compose-local.yaml stop

.PHONY: restart
restart:
		docker-compose -f docker-compose-local.yaml stop
		docker-compose -f docker-compose-local.yaml up -d

.PHONY: export-dep
export-dep:
		poetry export --without-hashes --without dev -f requirements.txt -o ./requirements.txt

# Alembic
.PHONY: generate
generate:
	poetry run alembic revision --m="$(m)" --autogenerate

.PHONY: migrate
migrate:
	poetry run alembic upgrade head
