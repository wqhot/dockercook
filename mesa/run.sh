#!/bin/bash

PWD=$(pwd)

# 启动容器并进入 Zsh
docker run -it --rm \
  --platform linux/amd64 \
  -v "${PWD}:/home/ubuntu/mesa" \
  -w "/home/ubuntu/mesa" \
  -e USER_ID=$(id -u) \
  -e GROUP_ID=$(id -g) \
  wqhot/mesa:v1.0 \
  /bin/zsh