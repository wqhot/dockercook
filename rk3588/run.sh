#!/bin/bash

# 本地 SDK 目录映射
LOCAL_SDK_PATH="${HOME}/temp"
CONTAINER_SDK_PATH="/home/wq/sdk"

# 启动容器并进入 Zsh
docker run -it --rm \
  --platform linux/amd64 \
  -v "${LOCAL_SDK_PATH}:${CONTAINER_SDK_PATH}" \
  -w "${CONTAINER_SDK_PATH}" \
  -e USER_ID=$(id -u) \
  -e GROUP_ID=$(id -g) \
  rk-builder:18.04 \
  /bin/zsh