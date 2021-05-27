#!/bin/bash

if docker images | grep -q "wow-news-bot"; then
  docker ps -a | awk '{ print $1,$2 }' | grep wow-news | awk '{ print $1 }' | xargs -I {} docker rm -f {}
	docker rmi wow-news-bot
fi

docker build . -t wow-news-bot:latest