import git

types = ['feat', 'fix', 'refactor']
bodys = ['BREAKING CHANGE', 'fix', 'refactor']

def pop_list(pop_list):
    for item in pop_list:
        yield item

def changelog_entry(releace, version):

    text = '## ' + version + '\n\n'
    text += changelog_entry_body(releace)
    text += '\n'
    return text

def changelog_entry_body(releace):
    text = ''
    commit_dict = {}
    for commit in releace:
        if commit['type'] in commit_dict:
            commit_dict[commit['type']].append(commit)
        else:
            commit_dict[commit['type']] = [commit]
                
    for commit_type, commits in commit_dict.items():
        if commit_type != None:

            text += changelog_block(commit_type, [commit['description'] + ' (' + commit['link'] + ')' for commit in commits])
            text += '\n'

    relevant_texts = get_relevant_texts(releace)
    if len(relevant_texts):

        text += changelog_block(None, relevant_texts)
        text += '\n'

    return text

def changelog_block(title, items):
    text = ''
    if title:
        text += '### ' + title + '\n'
    for item in items:
        if ':' in item[:18]:
            item = '**' + item[:item.index(':') + 1] + '**' + item[item.index(':') + 1:]
        text += '* ' + item + '\n'
    return text

def changelog_header(name):
    return '# ' + name + ' Changelog\n\n'

def changelog_footer(text):
    return text + '\n'

def get_relevant_texts(commits):
    texts = []
    for commit in commits:
        for body in bodys:
            if body in commit['body']:
                texts.append(commit['body'])
            elif body in commit['footer']:
                texts.append(commit['footer'])
    return texts


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

        try:
            commit_dict['scope'] = commit_dict['type'][commit_dict['type'].index('(')+1:commit_dict['type'].index(')')]
        except (ValueError, AttributeError):
            commit_dict['scope'] = None
        else:
            commit_dict['type'] = commit_dict['type'][:commit_dict['type'].index('(')]
        
        if commit_dict['type'] not in types:
            commit_dict['type'] = None
            commit_dict['scope'] = None
            commit_dict['description'] = message[0]
        elif commit_dict['scope']:
            commit_dict['description'] = commit_dict['scope'] + ': ' + message[0][message[0].index(': ')+2:]
        else: 
            commit_dict['description'] = message[0][message[0].index(': ')+2:]
        
        commit_dict['message'] = message[0]

        commit_dict['link'] = '(' + 'test' + ')'

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

            commit = tag.object
            while commit.type != 'commit':
                commit = commit.object
            
            tag_dict['commit'] = commit.binsha

            tags_list.append(tag_dict)

            # for tag in tags_list:
            #     print(tag['name'])

        return tags_list

    def generate_changelog(self):

        tags = self.get_tags()
        commits = self.get_commits()

        root = self.repo.git.rev_parse("--show-toplevel")
        name = root
        while '/' in name:
            name = name[name.index('/')+1:]
        text = changelog_header(name)

        if not len(tags): 
            footer = 'No versions structure available in this repo'
        else:
            footer = f'{len(commits)} commits in {len(tags)} version tags'
        # print('tags:', len(tags))
        # print('commits:',len(commits))

        commits.reverse()
        commits = pop_list(commits)

        releace = []
        releaces = []
        versions = []
        i = 0
        
        for tag in tags:
            i += 1
            for commit in commits:
                releace.append(commit)
                if commit['binsha'] == tag['commit']:
                    print(f"tag: {tag['name']} --> commits: {len(releace)}")

                    releaces.append(releace)
                    versions.append(tag['name'])
                    releace = []
                    i -= 1
                    break

        if len(releace):
            footer = changelog_block(f'{len(releace)} unallocable commits in {i} further version tags', [commit['message'] for commit in releace])
        
        releaces.reverse()
        versions.reverse()
        for index, releace in enumerate(releaces):
            text += changelog_entry(releace, version=versions[index])

        text += changelog_footer(footer)

        return text
