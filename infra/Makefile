# Makefile to manage production.

all: help

help:
	@printf "SandWalker Production, available rules:\n"
	@printf "\n"
	@printf " \033[0;32mdeploy\e[0m\t\trebuilds the infra and redeploy\n"
	@printf " \033[0;32mhelp\e[0m\t\this help\n"
	@printf " \033[0;32mlogs\e[0m\t\tprint last logs and attach\n"
	@printf "\n"

deploy:
	docker-compose build
	docker-compose up -d

logs:
	docker-compose logs -f --tail=1000

.PHONY: rebuild logs help
