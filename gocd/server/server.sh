#!/bin/bash

docker pull gocd/gocd-server:v17.4.0
docker run -d -p8153:8153 -p8154:8154 gocd/gocd-server:v17.4.0
