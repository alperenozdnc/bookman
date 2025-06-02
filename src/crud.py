import click

from rich.console import Console
from rich.table import Table

@click.command(help="Add a book with properties like its rating, author, pages, etc.")
def add() -> None:
    info = {
        "title": "",
        "author": "",
        "pages": None,
        "isbn": None,
        "status": None,
        "rating": None
    };

    def acquire_input() -> None:
        is_isbn_valid = False
        is_status_valid = False

        info["title"] = input("Title: ")
        info["author"] = input("Author: ")
        info["pages"] = input("Page count: ")

        while (not is_isbn_valid):
            info["isbn"] = input("ISBN: ")

            isbn = info["isbn"]

            isbn_numbers = isbn.split("-")
            isbn_len = 0

            for num in isbn_numbers:
                isbn_len += len(num)

            if isbn_len == 13:
                is_isbn_valid = True
            else:
                print("ISBN has to be 13 numbers. Try again.")

        while not is_status_valid:
            info["status"] = input("Status (done/reading/want to read): ")

            status = info["status"]

            if status == "done" or status == "reading" or status == "want to read":
                is_status_valid = True
                break
            else:
                print("Invalid status. Please enter again.")
                continue

        if info["status"] == "done":
            info["rating"] = input("Rating (x/10): ")

    table = Table(title="Book Information")

    acquire_input()

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Author", style="magenta")
    table.add_column("Pages", style="cyan")
    table.add_column("ISBN", style="magenta", no_wrap=True)
    table.add_column("Status", style="cyan")
    
    if info["status"] == "done":
        table.add_column("Rating", style="magenta")

    if info["status"] == "done":
        table.add_row(
            info["title"],
            info["author"],
            info["pages"],
            info["isbn"],
            info["status"],
            info["rating"]
        )
    else:
        table.add_row(
            info["title"],
            info["author"],
            info["pages"],
            info["isbn"],
            info["status"]
        )



    console = Console()
    console.print(table)
