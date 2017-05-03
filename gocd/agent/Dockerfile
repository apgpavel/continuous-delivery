FROM gocd/gocd-agent-alpine-3.5:v17.4.0

RUN apk add --update \
    python \
    py-pip \
    python-dev \
    build-base \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*


