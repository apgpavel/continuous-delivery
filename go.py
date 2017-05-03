#! /usr/bin/env python
import click
import pytest
import os
import yaml
import paramiko
import time
import re
from subprocess import call, Popen

config = {}


def load_config():
    config_file = open('go.yml', 'r')
    global config
    config = yaml.load(config_file)
    config['docker_tag'] = '{0}/{1}'.format(
        config['dockerhub_user'],
        config['project_name']
    )
    resolve_env_vars(config)


def resolve_env_vars(config):
    placeholder_pattern = re.compile('^\${(.*)}$')
    for key, value in config.items():
        match = placeholder_pattern.search(value)
        if(match):
            value_from_env = os.environ.get(match.group(1), None)

            if not value_from_env:
                error()
                click.echo('Environment variable {0} not found (was declared in go.yml)'.format(match.group(1)))
                exit(1)
            else: 
                config[key] = value_from_env


def marker():
    click.echo(click.style(u'\u2605 ', fg='yellow'), nl=False)


def error():
    click.echo(click.style(u'\u26a0 Error: ', fg='red', bold=True), nl=False)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('version', default=lambda: os.environ.get('VERSION', 'local'))
def build(version):
    marker()
    click.echo('Building version ', nl=False)
    click.echo(click.style(version, fg='green', bold=True))

    directory = os.path.dirname(__file__)
    tag = '{0}:{1}'.format(config['docker_tag'], version)

    call(['docker', 'build', directory, '-t', tag])


@cli.command()
def test():
    marker()
    click.echo('Running tests')
    pytest.main()


@cli.command()
@click.argument('environment', default='default')
def functionalTest(environment):
    marker()
    click.echo('Running functional tests')
    phantom = Popen(['./node_modules/.bin/phantomjs', '-w'])
    time.sleep(3)
    call(['./node_modules/.bin/nightwatch', '--env', environment])
    phantom.terminate()


@cli.command()
def push():
    marker()
    click.echo('Pushing docker image')

    call(['docker', 'push', config['docker_tag'])


@cli.command()
@click.argument('environment')
def deploy(environment):
    marker()
    click.echo('Deploying to ', nl=False)
    click.echo(click.style(environment, fg='green', bold=True))
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(hostname=config['ssh_host'], username=config['ssh_user'])
        
        tag = '{0}:latest'.format(config['docker_tag'], 'latest')
        
        stdin, stdout, stderr = client.exec_command('docker pull {0}'.format(tag))
        click.echo(stdout.read())
        stdin, stdout, stderr = client.exec_command('docker run -d -p 5000:5000 {0}'.format(tag))
        click.echo(stdout.read())
        client.close()
    except paramiko.SSHException as err:
        error()
        click.echo('Could not connect to server. You need to manually establish a connection first to add it to your known hosts')
        click.echo(err)


@cli.command()
def run():
    marker()
    click.echo('Running application')
    call(['docker', 'run', '-d', '-p', '5000:5000', config.docker_tag])


if __name__ == '__main__':
    load_config()
    cli()
