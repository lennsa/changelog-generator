import git

def test(repo_path, commit):
    repo = git.Repo(repo_path)
    master = repo.heads.master
    log = master.log()

    commits = list(repo.iter_commits("master"))

    for commit in commits:

        message = commit.message
        print(message)

        message = message.split('\n')

        commit = {}

        try:
            commit['type'] = message[0][:message[0].index(': ')]
        except ValueError:
            continue
        if commit['type'] not in ['feat', 'fix', 'refactor']:
            continue

        try:
            commit['scope'] = commit['type'][commit['type'].index('(')+1:commit['type'].index(')')]
        except ValueError:
            commit['scope'] = None
        else:
            commit['type'] = commit['type'][:commit['type'].index('(')]

        commit['description'] = message[0][message[0].index(': ')+2:]


        # if len(message) > 1:
        #     commit['body'] = message[1]
        # else:
        #     commit['body'] = None
        # if len(message) > 2:
        #     commit['footer'] = message[2]
        # else:
        #     commit['footer'] = None

        # print(commit)