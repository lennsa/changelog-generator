import git

def get_commits(repo_path):

    repo = git.Repo(repo_path)

    commits = list(repo.iter_commits("master"))

    commits_list = []

    for commit in commits:

        message = commit.message

        message = message.split('\n')

        commit_dict = {}

        commit_dict['type'] = None
        commit_dict['scope'] = None

        try:
            commit_dict['type'] = message[0][:message[0].index(': ')]
        except ValueError:
            commit_dict['type'] = None

        if commit_dict['type'] not in ['feat', 'fix', 'refactor', 'chore']:
            commit_dict['type'] = None
            commit_dict['description'] = message[0]
        else:

            try:
                commit_dict['scope'] = commit_dict['type'][commit_dict['type'].index('(')+1:commit_dict['type'].index(')')]
            except ValueError:
                commit_dict['scope'] = None
            else:
                commit_dict['type'] = commit_dict['type'][:commit_dict['type'].index('(')]


            commit_dict['description'] = message[0][message[0].index(': ')+2:]
        
        commit_dict['message'] = message[0]

        pos = 0
        commit_dict['body'] = ''
        commit_dict['footer'] = ''
        for line in message[1:]:
            if not line:
                pos += 1
            elif pos == 1:
                commit_dict['body'] += line + '\n'
            elif pos == 2:
                commit_dict['footer'] += line + '\n'

        commits_list.append(commit_dict)
    
    return commits_list