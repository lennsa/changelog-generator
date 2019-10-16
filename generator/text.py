import git


def pop_list(pop_list):
    for item in pop_list:
        yield item


class Repo():

    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

    def get_commits(self):

        commits = list(self.repo.iter_commits("master"))

        commits_list = []

        for commit in commits:

            commits_list.append(self.commit_dict(commit))
        
        return commits_list

    def commit_dict(self, commit):
        
        message = commit.message

        message = message.split('\n')

        commit_dict = {}

        commit_dict['binsha'] = commit.binsha

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
                
        return commit_dict

    def get_tags(self):
        
        tags = self.repo.tags

        tags_list = []

        for tag in tags:

            tag_dict = {}

            tag_dict['name'] = tag.name

            if tag.object.type == 'commit':
                commit = tag.object
            else:
                commit = tag.object.object
            tag_dict['commit'] = commit.binsha

            tags_list.append(tag_dict)

        return tags_list

    def generate_changelog(self):

        tags = self.get_tags()
        commits = self.get_commits()

        print('tags:', len(tags))
        print('commits:',len(commits))

        tags.reverse()
        tags = pop_list(tags)
        commits = pop_list(commits)

        releace = []
        i = 0
        
        for tag in tags:
            i += 1
            for commit in commits:
                releace.append(commit)
                if commit['binsha'] == tag['commit']:
                    print(f"tag: {tag['name']} --> commits: {len(releace)}")
                    releace = []
                    i -= 1
                    break
        
        print('rest tags:', i)
        print('rest commits:', len(releace))

        # while tags:
        #     tag = tags.pop()
        #     while commits:
        #         commit = commits.pop()
        #         releace.append(commit)
        #         if commit['binsha'] == tag['commit']:
        #             print(tag['name'], 'commits:', len(releace), 'rest commits:', len(commits))
        #             releace = []
        #             break
