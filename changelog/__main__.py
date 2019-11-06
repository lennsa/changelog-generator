import click
from gitrepo import Repo

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repo_path')
def generate(repo_path):
    repo = Repo(repo_path)
    text = repo.generate_changelog()
    with open('changelog.md', 'w') as out_file:
        out_file.write(text)

@generator.command()
@click.argument('repo_path')
def add(repo_path):
    repo = Repo(repo_path)
    with open('changelog.md', 'r') as in_file:
        old_text = in_file.read()
    text = repo.add_changelog(old_text)
    if text:
        with open('changelog.md', 'w') as out_file:
            out_file.write(text)

if __name__ == '__main__':
    generator()
    