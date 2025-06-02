import click
import crud

@click.group()
def cli() -> None:
    print("hello world")

cli.add_command(crud.add);

if __name__ == "__main__":
    cli()
