import git

def test(repo_path, commit):
    repo = git.Repo(repo_path)
    master = repo.heads.master
    log = master.log()

    for item in log:

        message = item.message
        message = message.strip('commit: ')
        message = message.split('\n')

        commit = {}

        try:
            commit['type'] = message[0][:message[0].index(': ')]
            commit['description'] = message[0][message[0].index(': ')+2:]
        except ValueError:
            continue

        if commit['type'] not in ['feat', 'fix', 'refactor']:
            continue

        if len(message) > 1:
            commit['body'] = message[1]
        else:
            commit['body'] = None
        if len(message) > 2:
            commit['footer'] = message[2]
        else:
            commit['footer'] = None

        print(commit)