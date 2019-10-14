import click
from generator.text import test

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repo_path')
@click.option('--commit', default=-1, help='number of greetings')
def generate(repo_path, commit):
    test(repo_path, commit)

if __name__ == '__main__':
    generator()
    