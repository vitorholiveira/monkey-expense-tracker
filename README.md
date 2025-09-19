# Monkey Expense Tracker

I developed this project to better control my expenses. The `main.py` script is designed to add new expenses to a CSV file that tracks all expenses for the month. The `utils/config` file has all the configuration constants that you can change if you'd like to customize the program.

## How to Run

This project requires a few steps to get started.

1.  **Install UV**: This project uses **UV**, a package and project manager. You'll need to install it first. For a complete guide, refer to the [official documentation](https://docs.astral.sh/uv/).

2.  **Set Your Income**: In the `income/` directory, copy the file `.income.example.json` and rename it to `.income.json`. Then, update the date (in `YYYY-MM` format) and set your income for your currency.

3.  **View Instructions**: To see a full list of instructions and all available script options, run the `uv run main.py -h` command.

## How expense data is stored

Expense data is stored in CSV files located in the `expense_files/current` folder. Each month has its own dedicated file, named `expense_YYYY-MM.csv`.

When a new expense is added, it is appended as a new line in the CSV file. This new file then overwrites the previous version, while a backup of the current file is saved. Backups are stored in a dedicated directory for each month, located at `expense_files/backup/YYYY-MM/`. These backup files follow the naming convention `expense_YYYY-MM-DD_HH:MM:SS.csv`.

An alternative storage method is available for development mode. By setting the `DEVELOPING` constant to `True` in `utils/config.py`, files will be stored as `dev_YYYY-MM.csv` in the `expanse_files/dev` directory, and the backup logic will be disabled. When `DEVELOPING` is `False`, the data is stored using the default method, including backups.

## Data Visualization

I also created a dashboard using Dash to visualize both monthly and custom time-range expenses. To run it, use the command: `uv run app.py`.
