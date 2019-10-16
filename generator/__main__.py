import click
from text import get_commits

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repo_path')
@click.option('--commit', default=-1, help='number of greetings')
def generate(repo_path, commit):
    commits = get_commits(repo_path)
    print(commits[commit])

if __name__ == '__main__':
    generator()
    