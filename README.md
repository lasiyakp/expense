# Expense Tracking System (Python)

A lightweight expense tracking application built with:

- **MVC pattern**
- **Singleton pattern** (`AppConfig`)
- **Factory pattern** (`RepositoryFactory`)

## Project Structure

- `expense_tracker/models` → data models
- `expense_tracker/views` → UI rendering logic
- `expense_tracker/controllers` → application/business logic
- `expense_tracker/storage` → repository implementations
- `expense_tracker/factories` → repository creation factory

## Run the Demo

```bash
python -m expense_tracker.app
```

## Run Tests

```bash
pytest -q
```


## Web Dashboard

Run a professional browser dashboard powered by **WSGI + Bootstrap**:

```bash
python -m expense_tracker.web_app
```

Then open `http://localhost:5000` to add expenses and view summary cards, category breakdown, and a recent-expense table.
