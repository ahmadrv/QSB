FROM ubuntu:jammy

LABEL name="MQTDDSIM" \
      version="1.0" \
      description="MQTDDSIM installation"

# Install dependencies
RUN apt-get update \
&&  apt-get install python-is-python3 -y \
&&  pip pip install mqt.ddsim