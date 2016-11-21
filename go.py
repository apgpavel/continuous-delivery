#! /usr/bin/env python
import click
import pytest
import time

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
def test():
    marker()
    click.echo('Running tests')
    pytest.main()

if __name__ == '__main__':
    cli()
