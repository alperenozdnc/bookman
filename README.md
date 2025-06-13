# 📚 bookman — a light book management cli 

![python](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![license](https://img.shields.io/badge/license-GPLv3-blue?style=flat-square)
![platform](https://img.shields.io/badge/platform-terminal-lightgrey?style=flat-square)

> track your reading list from the terminal. add, update, delete, and view books — with interactive prompts, validation, and decent stats.

---

## 🚀 features

- add books with title, author, pages, isbn, status, etc.
- update reading progress with simple prompts
- delete books (or wipe everything if you're feeling wild)
- monthly stats: pages read, books done, avg rating
- all local, all `.json` — no databases

---

## 📦 installation

### 1. clone the repo

```bash
git clone https://github.com/alperenozdnc/bookman.git
cd bookman
```

### 2. install dependencies

```bash
pip install -r requirements.txt
```

or just:

```bash
pip install click inquirer prompt_toolkit python-dateutil rich
```

---

## 🧠 where your books live

bookman stores each book in:

```bash
~/.local/bookman/
```

each file is named with the book's isbn, like `978-3-16-148410-0.json`.

---

## 🛠️ commands

run the app with:

```bash
python run.py <command>
```

### ➕ `add`

add a book interactively.

```bash
python run.py add
```

### 📋 `list [isbn]`

view/edit a book by isbn. if you don’t pass one, you’ll be asked.

```bash
python run.py list
```

you can:
- change status
- update current page
- set reading date
- add rating

### 🗑 `delete [isbn]`

delete by isbn or pick from a list.

```bash
python run.py delete
```

### 🔄 `clean`

delete *all* books.

```bash
python run.py clean
```

⚠️ can’t undo this.

### 📈 `stats`

show stats for the last 30 days + overall status.

```bash
python run.py stats
```

---

## 📊 example output

```text
📊 stats for this month
------------------------
books read         | 3
pages read         | 850
currently reading  | 2
average rating     | 8.33

📘 overall status
-------------------------
want to read       | 4
```

---

## ✅ input checks

- isbn must be 13 digits (hyphens ok)
- current page can’t go past total pages
- rating: 0–10, supports floats
- dates work in `dd/mm/yyyy` or `mm/dd/yyyy`

---

## 📁 sample book file

```json
{
  "title": "1984",
  "author": "george orwell",
  "pages": "328",
  "isbn": "978-0-452-28423-4",
  "status": "done",
  "date": "03/06/2025",
  "rating": "9"
}
```

---

## 🤝 contributing

totally open to pull requests, fixes, features, whatever.

1. fork it
2. make a branch (`git checkout -b cool-stuff`)
3. commit and push (`git commit -am 'do something' && git push`)
4. open a pr

---

## 📄 license

bookman is licensed under the gplv3. see [`LICENSE`](./LICENSE).

---

## ⭐ show some love

if you like this project, toss it a star on [github](https://github.com/alperenozdnc/bookman). thanks!
