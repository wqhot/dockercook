#!/bin/bash

PWD=$(pwd)

# 启动容器并进入 Zsh
docker run -it --rm \
  -v "${PWD}:/home/builduser/qt5" \
  -w "/home/builduser/qt5" \
  -e USER_ID=$(id -u) \
  -e GROUP_ID=$(id -g) \
  wqhot/qt5_oe:v1.0 \
  /bin/bash