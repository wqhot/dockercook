#!/bin/bash

PWD=$(pwd)

docker run -it --rm \
  -v "${PWD}:/home/node/workspace" \
  -w "/home/node/workspace" \
  -e USER_ID=$(id -u) \
  -e GROUP_ID=$(id -g) \
  -e USE_CUSTOM_LLM=true \
  -e CUSTOM_LLM_ENDPOINT=http://192.168.50.102:11634/v1 \
  -e CUSTOM_LLM_MODEL_NAME=gpt-oss-20b:latest \
  wqhot/easy_llm_cli:v1.0 \
  /bin/bash