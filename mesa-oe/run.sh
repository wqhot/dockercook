#!/bin/bash

PWD=$(pwd)

# 启动容器并进入 Zsh
docker run -it --rm \
  --platform linux/amd64 \
  -v "${PWD}:/home/builduser/mesa" \
  -w "/home/builduser/mesa" \
  -e USER_ID=$(id -u) \
  -e GROUP_ID=$(id -g) \
  wqhot/mesa-oe:v1.0 \
  /bin/bash