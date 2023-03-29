#!/bin/sh
export PLATFORM=mqtddsim
export IMAGE_NAME=${PLATFORM}benchmark 
export IMAGE_TAG=${PLATFORM}benchmarktag

docker run --rm -it -p 8888:8888 --name benchmark_${platform}\
${IMAGE_NAME}:${IMAGE_TAG}