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