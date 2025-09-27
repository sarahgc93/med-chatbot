.PHONY: build

#!make
include .env
export $(shell sed 's/=.*//' .env)

NAME	:= med-chatbot
TAG		:= $$(git rev-parse --short HEAD)
IMG		:= $(NAME):$(TAG)
LATEST	:= $(NAME):latest

build:
	@docker build \
		-t $(IMG)	.
	@docker tag $(IMG)	$(LATEST)

run:
	@docker run -it -p 8888:8888 $(NAME) jupyter lab --allow-root --port=8888 --ip=0.0.0.0