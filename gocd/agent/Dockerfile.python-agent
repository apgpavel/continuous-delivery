FROM gocd/gocd-agent-alpine-3.5:v17.4.0

RUN apk add --update \
    gcc \
    g++ \
    make \
    libffi-dev \
    openssl-dev \
    python-dev \
    python \
    py-pip \
    build-base \
    libffi \
    nodejs \
  && pip install virtualenv \
  && rm -rf /var/cache/apk/*


