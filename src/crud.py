import os
import json
import click
import const
import inquirer 

from rich.console import Console
from rich.table import Table

console = Console()
properties = ["title", "author", "pages", "isbn", "status", "rating"]

# Lists all books and asks for the user to pick one to do an action
def query_books(question: str) -> str:
    book_titles = []

    for filename in os.listdir(const.data_dir):
        isbn = filename.split(".")[0]

        with open(os.path.join(const.data_dir, f"{isbn}.json"), "r") as file:
            json_data = json.load(file)

            book_titles.append(json_data["title"])

    answer = inquirer.prompt([
        inquirer.List(
            "selected",
            message=question,
            choices=[*book_titles, "Cancel"]
        ),
    ])

    if answer is None or answer["selected"] == "Cancel":
        print("Aborting...")
        exit()

    selected = answer["selected"]
    book_idx = book_titles.index(selected)

    return [filename for filename in os.listdir(const.data_dir)][book_idx]

def print_book_info(info) -> None:
    table = Table(title="Book Information")

    for idx, property in enumerate(properties):
        if info["status"] != "done" and property == "rating":
            continue

        table.add_column(property.capitalize(), style=f"{"cyan" if idx % 2 == 0 else "magenta"}")
    
    if info["status"] == "done":
        table.add_row(
            *[info[key] for key in info.keys()]
        )
    else:
        table.add_row(
            *(filter(None, [info[key] if key != "rating" else None for key in info.keys()]))
        )

    console.print(table)

@click.command(help="Add a book with properties like its rating, author, pages, etc.")
def add() -> None:
    info = dict(zip(properties, len(properties) * ""))

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
        acquire_input()
    
        print_book_info(info)

        is_input_valid = click.confirm("Is the information correct? ")

        with open(os.path.join(const.data_dir, f"{info["isbn"]}.json"), "w") as file:
            json_data = json.dumps(info)

            file.write(json_data)


@click.command(help="Lists all the recorded books and allows you to delete one.")
@click.argument("isbn", required=False)
def delete(isbn: str) -> None:
    filename_to_delete = f"{isbn}.json" if isbn else query_books("What book to delete?")

    os.remove(os.path.join(const.data_dir, filename_to_delete))

    print(f"Successfully deleted book.")


@click.command(help="Lists all recorded books.")
@click.argument("isbn", required=False)
def list(isbn: str) -> None:
    filename_to_view = f"{isbn}.json" if isbn else query_books("What book to view?")
    info = dict(zip(properties, len(properties) * ""))

    with open(os.path.join(const.data_dir, filename_to_view), "r") as file:
        json_data = json.load(file)

        for property in properties:
            info[property] = json_data[property]

    print_book_info(info)

