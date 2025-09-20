# Monkey Expense Tracker

I developed this project to better control my expenses. The `main.py` script is designed to add new expenses to a CSV file that tracks all expenses for the month. The `utils/config` file has all the configuration constants that you can change if you'd like to customize the program.

## How to Run

This project requires a few steps to get started.

1.  **Install UV**: This project uses **UV**, a package and project manager. You'll need to install it first. For a complete guide, refer to the [official documentation](https://docs.astral.sh/uv/).

2.  **Set Your Income**: In the root of the project, copy the file `.income.example.json` and rename it to `.income.json`. Then, update the date (in `YYYY-MM` format) and set your income for your currency.

3.  **View Instructions**: To see a full list of instructions and all available script options, run the `uv run main.py -h` command.

## How expense data is stored

Expense data is stored in CSV files located in the `expense_files/current/` folder. Each month has its own dedicated file, named `expense_YYYY-MM.csv`.

When a new expense is added, it is appended as a new line in the CSV file. This new file then overwrites the previous version, while a backup of the current file is saved. Backups are stored in a dedicated directory for each month, located at `expense_files/current/backup/YYYY-MM/`. These backup files follow the naming convention `backup_YYYY-MM-DD_HH:MM:SS.csv`.

An alternative storage method is available for development mode. By setting the `DEVELOPING` constant to `True` in `utils/config.py`, files will be stored as `dev_YYYY-MM.csv` in the `expanse_files/dev/` directory and the backup files will be stored at `expanse_files/dev/backup/`. When `DEVELOPING` is `False`, the data is stored using the default method.

## How installments are implemented

One of the key features implemented is the option to add expenses paid in installments. By default, the number of installments is set to one, but you can choose how many installments you need. Since it’s impossible to know your exact income in future months, the system uses your current income as a reference. The implementation checks the nearest available income value and updates `income/.income.json` with that value for the upcoming months. If your income changes, you need to manually update `income/.income.json` with the new value.

## Data Visualization

I also created a dashboard using Dash to visualize both monthly and custom time-range expenses. To run it, use the command: `uv run app.py`.
