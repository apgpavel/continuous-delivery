**Snap-CI**: [![Build Status](https://snap-ci.com/hamvocke/continuous-delivery/branch/master/build_image)](https://snap-ci.com/hamvocke/continuous-delivery/branch/master)
**Travis-CI**: [![Build Status](https://travis-ci.org/hamvocke/continuous-delivery.svg?branch=master)](https://travis-ci.org/hamvocke/continuous-delivery)
**GitLab CI**: [![build status](https://gitlab.com/hamvocke/continuous-delivery/badges/master/build.svg)](https://gitlab.com/hamvocke/continuous-delivery/commits/master)

## Getting Started
Configure your environment by renaming `go.yml.example` to `go.yml` and replace all placeholders with your configuration values.

If you have any secrets you don't want to check in to version control you can declare variables in your `go.yml` file and provide the values as environment variables, e.g.:
    
    # go.yml
    my_secret = ${SOME_ENV_VAR}

Now you simply need to make sure that `SOME_ENV_VAR` is set in your environment. You can rename `env.example` to `.env` and add all your environment variables there and then source it using `source .env`.
