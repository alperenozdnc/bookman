import os
import json
import click
import const
import inquirer 

from rich.console import Console
from rich.table import Table

console = Console()

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


    is_input_valid = False

    while not is_input_valid:
        table = Table(title="Book Information")

        acquire_input()

        table.add_column("Title", style="cyan", no_wrap=True)
        table.add_column("Author", style="magenta")
        table.add_column("Pages", style="cyan")
        table.add_column("ISBN", style="magenta", no_wrap=True)
        table.add_column("Status", style="cyan")
        
        if info["status"] == "done":
            table.add_column("Rating", style="magenta")
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

        console.print(table)

        is_input_valid = click.confirm("Is the information correct? ")

        with open(os.path.join(const.data_dir, f"{info["isbn"]}.json"), "w") as file:
            json_data = json.dumps(info)

            file.write(json_data)


@click.command(help="Lists all the recorded books and allows you to delete one.")
@click.argument("isbn", required=False)
def delete(isbn: str) -> None:
    selected = None
    path_to_delete = ""

    if not isbn:
        book_titles = []

        for filename in os.listdir(const.data_dir):
            isbn = filename.split(".")[0]

            with open(os.path.join(const.data_dir, f"{isbn}.json"), "r") as file:
                json_data = json.load(file)

                book_titles.append(json_data["title"])

        answer = inquirer.prompt([
            inquirer.List(
                "selected",
                message="What book to delete?",
                choices=book_titles
            ),
        ])

        selected = answer["selected"]
        book_idx = book_titles.index(selected)

        path_to_delete = os.path.join(const.data_dir, [filename for filename in os.listdir(const.data_dir)][book_idx])
    else:
        path_to_delete = os.path.join(const.data_dir, f"{isbn}.json")

    os.remove(path_to_delete)
