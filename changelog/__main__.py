import click
from gitrepo import Repo

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repo_path')
@click.option("--types", default='feat,fix,refactor,docs', help="commit types to show in changelog")
@click.option("--bodytags", default='BREAKING CHANGE,MAJOR', help="body tags that schould be shown in changelog")
def generate(repo_path, types, bodytags):
    repo = Repo(repo_path)
    types = types.split(',')
    bodytags = bodytags.split(',')
    text = repo.generate_changelog(types, bodytags)
    with open('changelog.md', 'w') as out_file:
        out_file.write(text)

@generator.command()
@click.argument('repo_path')
@click.option("--types", default='feat,fix,refactor,docs', help="commit types to show in changelog")
@click.option("--bodytags", default='BREAKING CHANGE,MAJOR', help="body tags that schould be shown in changelog")
def add(repo_path, types, bodytags):
    repo = Repo(repo_path)
    types = types.split(',')
    bodytags = bodytags.split(',')
    with open('changelog.md', 'r') as in_file:
        old_text = in_file.read()
    text = repo.add_changelog(old_text, types, bodytags)
    if text:
        with open('changelog.md', 'w') as out_file:
            out_file.write(text)

if __name__ == '__main__':
    generator()
    