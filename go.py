#! /usr/bin/env python
import click
import pytest
import os
import yaml
import paramiko
from subprocess import call

config = {}


def load_config():
    config_file = open('go.yml', 'r')
    global config
    config = yaml.load(config_file)


def marker():
    click.echo(click.style(u'\u2605 ', fg='yellow'), nl=False)


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
    directory_name = os.getcwd().split(os.sep)[-1]
    project_name = config.get('project_name', directory_name)
    dockerhub_user = config.get('dockerhub_user')
    tag = '{0}/{1}:{2}'.format(dockerhub_user, project_name, version)

    call(['docker', 'build', directory, '-t', tag])


@cli.command()
def test():
    marker()
    click.echo('Running tests')
    pytest.main()


@cli.command()
def push():
    marker()
    click.echo('Pushing docker image')
    tag = '{0}/{1}:latest'.format(
        config.get('dockerhub_user'),
        config.get('project_name')
    )

    call(['docker', 'push', tag])


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
        client.connect(hostname=config.get('ssh_host'), username=config.get('ssh_user')
        tag = '{0}/{1}:latest'.format(
            config.get('dockerhub_user'),
            config.get('project_name')
        )
        stdin, stdout, stderr = client.exec_command('docker pull {0}'.format(tag))
        click.echo(stdout.read())
        stdin, stdout, stderr = client.exec_command('docker run -d -p 5000:5000 {0}'.format(tag))
        click.echo(stdout.read())
        client.close()
    except paramiko.SSHException as err:
        click.echo(click.style('Error: ', fg='red', bold=True), nl=False)
        click.echo('Could not connect to server. You need to manually establish a connection first to add it to your known hosts')
        click.echo(err)


@cli.command()
def run():
    marker()
    click.echo('Running application')
    call(['gunicorn', '-w', '4', 'helloworld:app', '-b', 'localhost:5000'])


if __name__ == '__main__':
    load_config()
    cli()
