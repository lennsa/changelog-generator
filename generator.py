import click

@click.group()
def generator():
    pass

@generator.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def generate(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)

if __name__ == '__main__':
    generator()
    