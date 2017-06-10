#! /usr/bin/env bash

set -e

echo "Generating new SSH key for travis"
ssh-keygen -t rsa -b 4096 -f ./travis_rsa

echo "Encrpyting travis SSH key"
travis encrypt-file travis_rsa --add

echo "Uploading SSH public key to deployment host"
ssh-copy-id -i travis_rsa.pub root@138.68.72.121


echo "Removing generated key files"
rm -f travis_rsa travis_rsa.pub

echo "Done"
