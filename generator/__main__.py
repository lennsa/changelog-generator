import click
from text import Repo

@click.group()
def generator():
    pass

@generator.command()
@click.argument('repo_path')
def generate(repo_path):
    repo = Repo(repo_path)
    # commits = repo.get_commits()
    # for commit in commits:
    #     print(commit['description'])
    # tags = repo.get_tags()
    # for tag in tags:
    #     print(tag)
    text = repo.generate_changelog()
    # print(text)

@generator.command()
@click.argument('repo_path')
@click.option('--commit', default=-1, help='number of commit (latest =^ 0)')
def getcommit(repo_path, commit):
    repo = Repo(repo_path)
    commits = repo.get_commits()
    print(commits[commit])

if __name__ == '__main__':
    generator()
    