def verify_footer(old_changelog, releaces):
    old_footer = None
    for line in old_changelog:

        # Search for footer.

        if line.startswith('::>'):
            old_footer = line.split(' ')
            old_changelog.remove(line)

    if not old_footer:
        print('no readable footer')
        return False

    latest_commit = old_footer[-1]
    old_commits = int(old_footer[old_footer.index('commits') - 1])
    old_versions = int(old_footer[old_footer.index('version') - 1])
    
    print(
        'start at commit:', latest_commit,
        '\nskip commits:', old_commits, 
        '\nskip versions:', old_versions, 
        '\nfound entrypoint in changelog:', releaces[-old_versions][-1]['binsha'] == latest_commit
    )

    if old_versions > len(releaces) or not releaces[-old_versions][-1]['binsha'] == latest_commit:
        print('unable to read old changelog')
        return False

    return old_versions

def generate_footer(tags, commits):
    return f"::> {len(commits)} commits in {len(tags)} version tags, last considered commit: {tags[-1]['commit']}\n"
