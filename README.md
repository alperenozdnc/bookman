# 📚 Bookman — A CLI Reading Tracker

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/platform-CLI-informational?style=flat-square)

> Track your reading list from the terminal. Add, update, delete, and view books — with interactive prompts, validation, and rich stats.

---

## 🚀 Features

- 📖 Add books with metadata like author, ISBN, status, rating, etc.
- 🔄 Update reading progress interactively
- 🗑 Delete books or wipe your entire list
- 📊 View beautiful monthly statistics (pages read, ratings, etc.)
- 💾 Lightweight: stores data in `.json` files

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/alperenozdnc/bookman.git
cd bookman
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install click inquirer prompt_toolkit python-dateutil rich
```

---

## 🧠 Book Data Format

Bookman stores each book in:

```bash
~/.local/bookman/
```

Each file is named after the book’s ISBN (`<isbn>.json`).

---

## 🛠️ Commands

Run the app with:

```bash
python run.py <command>
```

### ➕ `add`

Interactively add a new book.

```bash
python run.py add
```

### 📋 `list [isbn]`

View and edit a book by ISBN. If omitted, a list will be shown.

```bash
python run.py list
```

Edit options:
- Change status
- Update current page
- Set reading date
- Set rating

### 🗑 `delete [isbn]`

Delete a book by ISBN or choose interactively.

```bash
python run.py delete
```

### 🔄 `clean`

Delete all book entries.

```bash
python run.py clean
```

⚠️ This action is irreversible.

### 📈 `stats`

Show stats for the past month and overall book status.

```bash
python run.py stats
```

---

## 📊 Example Output

```text
📊 Stats for This Month
------------------------
Books Read         | 3
Pages Read         | 850
Currently Reading  | 2
Average Rating     | 8.33

📘 Overall Reading Status
-------------------------
Want to Read       | 4
```

---

## ✅ ISBN & Input Validation

- ISBN must be 13 digits (hyphens allowed, validated format)
- Page count, current page, rating, and dates are all validated
- Supports both `DD/MM/YYYY` and `MM/DD/YYYY` formats

---

## 📁 Example Data File

```json
{
  "title": "1984",
  "author": "George Orwell",
  "pages": "328",
  "isbn": "978-0-452-28423-4",
  "status": "done",
  "date": "03/06/2025",
  "rating": "9"
}
```

---

## 🤝 Contributing

PRs, bug reports, and feature suggestions are welcome!

1. Fork the repo
2. Create your branch (`git checkout -b feature/foo`)
3. Commit and push (`git commit -am 'Add foo' && git push`)
4. Open a Pull Request

---

## 📄 License

Licensed under the MIT License — see [`LICENSE`](./LICENSE) for details.

---

## 🌟 Star this project!

If you find Bookman useful, consider giving it a ⭐ on [GitHub](https://github.com/alperenozdnc/bookman) — it really helps!
