import utils


def changelog_entry(releace, version, date):

    text = '## ' + version + ' (' + date + ')\n\n'
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

            text += changelog_block(
                commit_type, 
                [commit['description'] + ' ' + commit['link'] for commit in commits] # body
            )
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
        for body in utils.bodys:
            if 'body' in commit.keys() and body in commit['body']:
                texts.append(commit['body'])
            if 'footer' in commit.keys() and body in commit['footer']:
                texts.append(commit['footer'])
    return texts

def get_relevant_text(commit):
    texts = []
    for body in utils.bodys:
        if 'body' in commit.keys() and body in commit['body']:
            texts.append(commit['body'])
        if 'footer' in commit.keys() and body in commit['footer']:
            texts.append(commit['footer'])
    return texts
