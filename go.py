#! /usr/bin/env python
import click
import pytest
import os
from subprocess import call

def marker():
    click.echo(click.style('★ ', fg='yellow'), nl=False)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('environment')
def deploy(environment):
    marker()
    click.echo('Deploying to ', nl=False)
    click.echo(click.style(environment, fg='green', bold=True))

@cli.command()
@click.argument('version', default=lambda: os.environ.get('VERSION', 'local'))
def build(version):
    project_name = os.getcwd().split(os.sep)[-1]
    marker()
    click.echo('Building version ', nl=False)
    click.echo(click.style(version, fg='green', bold=True))
    call(['docker',
        'build',
        os.path.dirname(__file__),
        '-t',
        '{0}:{1}'.format(project_name, version)])

@cli.command()
def test():
    marker()
    click.echo('Running tests')
    pytest.main()

if __name__ == '__main__':
    cli()
