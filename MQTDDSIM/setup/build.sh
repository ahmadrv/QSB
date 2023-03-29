#!/bin/sh
export PLATFORM=mqtddsim
export IMAGE_NAME=${PLATFORM}benchmark 
export IMAGE_TAG=${PLATFORM}benchmarktag

docker image build \
    --build-arg username=$USER \
    --build-arg uid=$UID \
    --build-arg gid=`id -g` \
    --build-arg platform=${PLATFORM} \
    --file /home/$USER/QSB/MQTDDSIM/setup/Dockerfile \
    --tag $IMAGE_NAME:$IMAGE_TAG \
  .