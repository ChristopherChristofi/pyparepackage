project ?= pyparepackage
target ?= dev
location ?= $(shell pwd)

build:
	docker build --target ${target} . --tag ${project}-${target}

debug:
	docker run --rm -it -v ${location}:/work ${project}-${target} sh
