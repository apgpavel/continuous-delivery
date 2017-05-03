#!/bin/bash

docker pull gocd/gocd-agent-alpine-3.5:v17.4.0
docker run -d -e GO_SERVER_URL=https://172.17.0.2:8154/go gocd/gocd-agent-alpine-3.5:v17.4.0

