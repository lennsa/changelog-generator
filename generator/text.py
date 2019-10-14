import git

def test(repo_path, commit):
    repo = git.Repo(repo_path)
    master = repo.heads.master
    log = master.log()
    print(log[commit])
