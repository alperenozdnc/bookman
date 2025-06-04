import os
import click
import crud
import const

@click.group()
def cli() -> None:
    try:
        os.mkdir(const.data_dir)
        print("You are a first timer. Creating data folder... \n")
    except FileExistsError:
        pass
    except PermissionError:
        print(f"Permission denied: Unable to create '{const.data_dir}'.")
    except Exception as e:
        print(f"An error occurred trying to create data directory: {e}")

cli.add_command(crud.add)
cli.add_command(crud.delete)
cli.add_command(crud.list)

if __name__ == "__main__":
    cli()
