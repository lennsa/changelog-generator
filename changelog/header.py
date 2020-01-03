def remove_header(old_changelog):
    for index, line in enumerate(old_changelog):
        if line and not line.startswith('# '):

            # Search for the first line which is not Empty and not the Title.
            # Strip the prior lines

            old_changelog = old_changelog[index:]
            return

def generate_header(name):
    return f"# { name } Changelog\n\n\n"
