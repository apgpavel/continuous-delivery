#!/bin/bash

docker build -t gocd-agent .
docker run -d -e GO_SERVER_URL=https://172.17.0.2:8154/go gocd-agent

