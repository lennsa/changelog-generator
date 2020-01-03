import codecs
import git
import generate
import footer
import time

def pop_list(pop_list):
    for item in pop_list:
        yield item

class Repo():

    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)

        root = self.repo.git.rev_parse("--show-toplevel")
        self.name = root
        while '/' in self.name:
            self.name = self.name[self.name.index('/') + 1:]

    def get_commits(self, types):

        commits = list(self.repo.iter_commits("master"))

        commits_list = []
        for commit in commits:
            commits_list.append(self.commit_dict(commit, types))
        
        return commits_list

    def commit_dict(self, commit, types):
        
        message = commit.message

        message = message.split('\n\n')
        for index, section in enumerate(message):
            if section.endswith('\n'):
                section = section [:-1] 
            message[index] = section.replace('\n', ' ')

        commit_dict = {}

        commit_dict['message'] = message[0]

        commit_dict['type'] = None
        commit_dict['scope'] = None

        try:
            commit_dict['type'] = message[0][:message[0].index(': ')]
            commit_dict['description'] = message[0][message[0].index(': ')+2:]
        except ValueError:
            commit_dict['type'] = None

        try:
            commit_dict['scope'] = commit_dict['type'][commit_dict['type'].index('(')+1:commit_dict['type'].index(')')]
        except (ValueError, AttributeError):
            commit_dict['scope'] = None
        else:
            commit_dict['type'] = commit_dict['type'][:commit_dict['type'].index('(')]
            commit_dict['description'] = commit_dict['scope'] + ': ' + message[0][message[0].index(': ')+2:]
        
        if commit_dict['type'] not in types:
            commit_dict['type'] = None
            commit_dict['scope'] = None
            commit_dict['description'] = message[0]

        if len(message) > 1:
            commit_dict['body'] = message[1]
        if len(message) > 2:
            commit_dict['footer'] = message[2]

        commit_dict['binsha'] = codecs.encode(commit.binsha, 'hex').decode('utf-8')

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
            
            tag_dict['commit'] = codecs.encode(commit.binsha, 'hex').decode('utf-8')
            date = time.gmtime(commit.committed_date)
            tag_dict['date'] = f'{date.tm_year}-{date.tm_mon}-{date.tm_mday}'

            tags_list.append(tag_dict)

        return tags_list

    def generate_changelog(self, types, bodytags):

        text = generate.changelog_header(self.name)

        releaces, versions, dates, new_footer = self.get_changelog(types)

        if len(releaces) == 0:
            print("No versions structure available in this repo")
            return

        # Render and append all releases to the changelog.

        for index, releace in enumerate(releaces):
            text += generate.changelog_entry(releace, version=versions[index], date=dates[index], bodytags=bodytags)

        text += generate.changelog_footer(new_footer)

        return text

    def add_changelog(self, old_text, types, bodytags):

        text = generate.changelog_header(self.name)

        releaces, versions, dates, new_footer = self.get_changelog(types)

        if len(releaces) == 0:
            print("No versions structure available in this repo")
            return

        old_changelog = old_text.split('\n')

        # If the footer is valide, the funktion returns the ammount of old versions.
        # If not, the Funktion will return False.

        old_versions = footer.verify_footer(old_changelog, releaces)
        if (old_versions):

            # Render and append all new releases to the changelog.

            for index, releace in enumerate(releaces[:-old_versions]):
                text += generate.changelog_entry(releace, version=versions[index], date=dates[index], bodytags=bodytags)

            for index, line in enumerate(old_changelog):
                if line and not line.startswith('# '):

                    # Search for the first line which is not Empty and not the Title.
                    # Append the subsequent lines to the changelog.

                    text += '\n'.join(old_changelog[index:])
                    break

            text += generate.changelog_footer(new_footer)

            return text

        else:
            return None

    def get_changelog(self, types):
        tags = self.get_tags()
        commits = self.get_commits(types)

        if len(tags):
            new_footer = footer.generate_footer(tags, commits)
        else:
            new_footer = None

        commits.reverse()
        commits = pop_list(commits)

        releace = []
        releaces = []
        versions = []
        dates = []
        
        for tag in tags:
            for commit in commits:

                releace.append(commit)
                
                if commit['binsha'] == tag['commit']:
                    print(f"tag: {tag['name']} --> commits: {len(releace)}")

                    releaces.append(releace)
                    versions.append(tag['name'])
                    dates.append(tag['date'])
                    releace = []
                    break

        releaces.reverse()
        versions.reverse()
        dates.reverse()
        
        return releaces, versions, dates, new_footer