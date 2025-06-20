import os
import json
import click
import const
import inquirer

from prompt_toolkit import prompt
from datetime import date 
from dateutil.parser import parse, ParserError
from rich.console import Console
from rich.table import Table

console = Console()
properties = ["title", "author", "pages", "isbn", "status", "current_page", "date", "rating"]

def is_valid_date(date):
    if not date:
        return False
    try:
        parse(date)
        return True
    except ParserError:
        return False

def is_string_float(s):
    try:
        return "." in s or "e" in s.lower() and float(s)
    except ValueError:
        return False


def validate_isbn(isbn: str) -> bool:
    is_valid = False

    for i in range(0, len(isbn)):
        c = isbn[i]

        if not c.isdigit() and c != "-":
            print(f"{c} is not allowed. Try again.")
            return False

        if c == "-":
            if i == 0 or i == len(isbn) - 1:
                print("ISBN can't start or end with a dash. Please try again.")
                return False

        if c == "-" and isbn[i + 1] == "-":
            print("Two dashes can't be next to eachother. Please try again.")
            return False

    isbn_numbers = isbn.split("-")
    isbn_len = 0

    for num in isbn_numbers:
        isbn_len += len(num)

    if isbn_len == 13:
        is_valid = True
    else:
        print("ISBN has to be 13 numbers. Try again.")

    return is_valid


# Lists all books and asks for the user to pick one to do an action
def query_books(question: str) -> str:
    book_titles = []

    for filename in os.listdir(const.data_dir):
        isbn = filename.split(".")[0]

        with open(os.path.join(const.data_dir, f"{isbn}.json"), "r") as file:
            json_data = json.load(file)

            book_titles.append(json_data["title"])

    answer = inquirer.prompt(
        [
            inquirer.List(
                "selected", message=question, choices=[*book_titles, "Cancel"]
            ),
        ]
    )

    if answer is None or answer["selected"] == "Cancel":
        print("Aborting...")
        exit()

    selected = answer["selected"]
    book_idx = book_titles.index(selected)

    return [filename for filename in os.listdir(const.data_dir)][book_idx]

def is_valid_current_page(current_page: str, total_pages: int) -> bool:
    is_valid = False

    if not current_page.isdigit():
        print("Current page has to be a number. Try again.")
    elif int(current_page) > total_pages:
        print("Current page can't be higher than total page count. Try again.")
    elif int(current_page) == total_pages:
        print("Why not just mark book as 'done' if you are on the last page? Try again or <C-c> to cancel.")
    else:
        is_valid = True

    return is_valid

def print_book_info(info) -> None:
    table = Table(title="Book Information")

    for idx, property in enumerate(properties):
        if info["status"] != "done" and property == "rating":
            continue

        if info["status"] == "want to read" and property == "date":
            continue

        if info["status"] != "reading" and property == "current_page":
            continue

        table.add_column(
            property.capitalize(), style=f"{"cyan" if idx % 2 == 0 else "magenta"}"
        )

    if info["status"] == "done":
        table.add_row(
            *(
                filter(
                    None,
                    [info[key] if key != "current_page" else None for key in info.keys()],
                )
            )
        )
    elif info["status"] == "reading":
        table.add_row(
            *(
                filter(
                    None,
                    [info[key] if key != "rating" else None for key in info.keys()],
                )
            )
        )
    else:
        table.add_row(
            *(
                filter(
                    None,
                    [info[key] if key != "rating" and key != "date" and key != "current_page" else None for key in info.keys()],
                )
            )
        )

    console.print(table)


@click.command(help="Add a book with properties like its rating, author, pages, etc.")
def add() -> None:
    info = dict(zip(properties, [""] * len(properties)))

    def acquire_input() -> None:
        is_isbn_valid = False
        is_status_valid = False
        is_date_valid = False
        is_rating_valid = False
        is_page_count_valid = False

        info["title"] = input("Title: ")
        info["author"] = input("Author: ")

        while not is_page_count_valid:
            info["pages"] = input("Page count: ")

            page_count: str = info["pages"]

            if not page_count.isdigit():
                print("Page count has to be a number. Try again.")
            else:
                is_page_count_valid = True

        while not is_isbn_valid:
            info["isbn"] = input("ISBN: ")

            is_isbn_valid = validate_isbn(info["isbn"])

        while not is_status_valid:
            info["status"] = input("Status (done/reading/want to read): ")

            status = info["status"].lower()

            if status == "done" or status == "reading" or status == "want to read":
                is_status_valid = True
                break
            else:
                print("Invalid status. Please enter again.")
                continue

        if info["status"] == "reading":
            while True:
                info["current_page"] = input("What page are you on: ")

                current_page: str = info["current_page"]

                if is_valid_current_page(current_page, int(info["pages"])):
                    break

        if info["status"] == "done":
            while not is_date_valid:
                info["date"] = input("Date of reading (DD/MM/YYYY or MM/DD/YYYY): ")

                if not is_valid_date(info["date"]):
                    print("Invalid date. Try again.")
                    continue

                is_date_valid = True

            while not is_rating_valid:
                info["rating"] = input("Rating (x/10): ")

                rating: str = info["rating"]

                if not rating.isdigit() and not is_string_float(rating):
                    print("Rating has to be a digit or a float. Try again.")
                    continue
                else:
                    rating_value = int(rating) if rating.isdigit() else float(rating)

                    if rating_value > 10:
                        print("Rating can't be bigger than 10. Try again.")
                    elif rating_value < 0:
                        print("Rating can't be smaller than 0. Try again.")
                    else:
                        is_rating_valid = True

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
    is_user_done = False

    while not is_user_done:
        is_data_manipulated = False
        info = dict(zip(properties, [""] * len(properties)))
        os.system("clear")
        filename_to_view = f"{isbn}.json" if isbn else query_books("What book to view?")

        with open(os.path.join(const.data_dir, filename_to_view), "r") as file:
            json_data = json.load(file)

            for property in properties:
                if info["status"] == "want to read" and property == "date":
                    continue

                if info["status"] != "done" and property == "rating":
                    continue

                if property in json_data:
                    info[property] = json_data[property]

        os.system("clear")
        print_book_info(info)

        answer = inquirer.prompt(
            [
                inquirer.List(
                    "selected",
                    message="What do you want to do?",
                    choices=[
                        *filter(
                            None,
                            [
                                "Change status",
                                "Delete",
                                "Set date" if info["status"] == "done" or info["status"] == "reading" else None,
                                "Set current page" if info["status"] == "reading" else None,
                                "Set rating" if info["status"] == "done" else None,
                                "Go back to menu",
                            ],
                        )
                    ],
                )
            ]
        )

        if answer is None:
            continue

        selected = answer["selected"]

        if selected == "Delete":
            os.remove(os.path.join(const.data_dir, filename_to_view))

            print(f"Successfully deleted book.")
        elif selected == "Change status":
            answer_status = inquirer.prompt(
                [
                    inquirer.List(
                        "selected",
                        message="Set status",
                        choices=[
                            *filter(
                                None,
                                [
                                    status if status.lower() != info["status"] else None
                                    for status in ["Done", "Reading", "Want to read"]
                                ],
                            ),
                            "Cancel",
                        ],
                    ),
                ]
            )

            if answer_status is None:
                continue

            selected_status: str = answer_status["selected"].lower()

            if selected_status == "cancel":
                continue

            info["status"] = selected_status

            is_data_manipulated = True
        elif selected == "Set current page":
            while True:
                info["current_page"] = prompt("What page are you on? ", default=info["current_page"] if info["current_page"] else "0")

                if not is_valid_current_page(info["current_page"], int(info["pages"])):
                    continue

                break

            is_data_manipulated = True
        elif selected == "Set date":
            while True:
                if info["date"]:
                    info["date"] = prompt("Date of reading [DD/MM/YY]? ", default=info["date"])
                else:
                    info["date"] = prompt("Date of reading [DD/MM/YY] (defaults to today)? ", default=date.today().strftime("%d/%m/%Y"))

                if not is_valid_date(info["date"]):
                    print("Invalid date. Try again.")
                    continue

                break

            is_data_manipulated = True
        elif selected == "Set rating":
            rating = input("What's the rating out of 10? ")
            info["rating"] = rating

            is_data_manipulated = True
        else:
            continue

        if is_data_manipulated:
            with open(os.path.join(const.data_dir, filename_to_view), "w") as file:
                file.write(json.dumps(info))

        is_user_done = True

@click.command(help="Cleans all recorded books.")
def clean() -> None:
    book_files = os.listdir(const.data_dir)

    for file in book_files:
        os.remove(os.path.join(const.data_dir, file))

    print("All data cleaned successfully.")

@click.command(help="Shows statistics like amount of books read, ratings, etc. over a month.")
def stats() -> None:
    console = Console()
    book_datas = os.listdir(const.data_dir)

    if len(book_datas) == 0:
        console.print("[bold red]No stats to view.[/bold red]")
        return

    total_books_read = 0
    total_books_being_read = 0
    total_books_to_be_read = 0
    total_pages_read = 0
    average_rating_total = 0

    for book_file in book_datas:
        with open(os.path.join(const.data_dir, book_file), "r") as file:
            info = json.load(file)
        
        status = info.get("status", "").lower()

        if status == "done":
            try:
                book_date = parse(info.get("date", ""), dayfirst=True)
                now = parse(date.today().strftime("%d/%m/%Y"), dayfirst=True)
                delta = now - book_date
            except ParserError:
                continue

            if delta.days > 30:
                continue

            total_books_read += 1
            total_pages_read += int(info.get("pages", 0))
            rating = info.get("rating", "0")

            average_rating_total += float(rating) if is_string_float(rating) else int(rating)
        elif status == "reading":
            try:
                book_date = parse(info.get("date", ""), dayfirst=True)
                now = parse(date.today().strftime("%d/%m/%Y"), dayfirst=True)
                delta = now - book_date
            except ParserError:
                continue

            if delta.days > 30:
                continue

            total_books_being_read += 1
            total_pages_read += int(info["current_page"]) if info["current_page"] else 0
        elif status == "want to read":
            total_books_to_be_read += 1

    average_rating = (average_rating_total / total_books_read) if total_books_read > 0 else 0

    # Monthly stats table
    month_stats = Table(title="[bold cyan]Stats for This Month[/bold cyan]", show_lines=True)
    month_stats.add_column("Metric", style="magenta bold")
    month_stats.add_column("Value", style="green")

    month_stats.add_row("Books Read", str(total_books_read))
    month_stats.add_row("Pages Read", str(total_pages_read))
    month_stats.add_row("Currently Reading", str(total_books_being_read))
    month_stats.add_row("Average Rating", f"{average_rating:.2f}" if total_books_read > 0 else "N/A")

    # Overall stats table
    overall_stats = Table(title="[bold cyan]Overall Reading Status[/bold cyan]", show_lines=True)

    overall_stats.add_column("Status", style="magenta bold")
    overall_stats.add_column("Count", style="green")
    overall_stats.add_row("Want to Read", str(total_books_to_be_read))

    console.print(month_stats)
    console.print(overall_stats)

