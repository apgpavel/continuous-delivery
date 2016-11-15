#! /bin/bash

action=$1

usage() {
  echo -e "Usage: $0 <command>\n"
  echo -e "Options:"
  echo -e "  help\t- Show this message and exit"
  echo -e "  setup\t- Setup this project"
  echo -e "  test\t- Run all tests"
  exit 1;
}

activate_virtualenv() {
  if [[ -z $VIRTUAL_ENV ]]; then
    echo "★ Activating virtualenv"
    source venv/bin/activate
  fi
}

setup() {
  if [[ -d venv/ ]]; then
    echo "★ Removing old virtualenv"
    rm -rf venv/
  fi

  echo "★ Installing system-wide dependencies"
  apt-get install -y python pip virtualenv

  echo "★ Setting up virtualenv"
  virtualenv venv

  activate_virtualenv

  echo "★ Installing Python dependencies"
  pip install -r requirements.txt

  exit 0;
}

runTests() {
  activate_virtualenv
  pytest
  exit 0;
}

if [ -z "${1}" ]; then
  usage
fi

if [[ $action == "help" ]]; then
  usage
fi

if [[ $action == "setup" ]]; then
  setup
fi

if [[ $action == "test" ]]; then
  runTests
fi
