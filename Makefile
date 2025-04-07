.PHONY: build run stop logs shell

build:
	docker compose build

up:
	docker compose up

stop:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec clockmaker-bot bash
