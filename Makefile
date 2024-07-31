CONTAINER_NAME=d176ef7394ba
POSTGRES_DB=wg_forge_db
POSTGRES_USER=wg_forge
POSTGRES_PASSWORD=42a
PORT=5433

all:

run:
	docker run --name $(CONTAINER_NAME) \
	  -e POSTGRES_DB=$(POSTGRES_DB) \
	  -e POSTGRES_USER=$(POSTGRES_USER) \
	  -e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	  -p $(PORT):5432 \
	  -d postgres

stop:
	docker stop $(CONTAINER_NAME)

remove:
	docker rm $(CONTAINER_NAME)

.PHONY: run stop remove