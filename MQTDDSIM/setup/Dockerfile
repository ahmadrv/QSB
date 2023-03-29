FROM ubuntu:jammy

ARG platform=MQTDDSIM

LABEL name="${platform}" \
      version="1.0" \
      description="MQTDDSIM installation"

# Install dependencies
RUN apt-get update \
&&  apt-get install python-is-python3 -y \
&&  pip install mqt.ddsimq

# Run bash
SHELL ["/bin/bash", "-c"]

# Define arguments
ARG username=tester
ARG uid=1000
ARG gid=100
ARG broot=.

ENV PLATFORM=$platform
ENV USER $username
ENV UID $uid
ENV GID $gid
ENV HOME /home/$username
ENV BROOT $broot
ENV CROOT $broot/$platform/setup

# Create user
RUN adduser --disabled-password \
    --gecos "Non-root user" \
    --uid $UID \
    --gid $GID \
    --home $HOME \
    ${USER}

ENV PROJECT_DIR $HOME

ADD ${BROOT} ${PROJECT_DIR}

WORKDIR ${PROJECT_DIR}/${PLATFORM}

SHELL [ "python", "benchmarks.py" ]