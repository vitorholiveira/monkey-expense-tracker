# Expense

I developed this project to gain better control over my expenses. The main script's purpose is to add new expenses to a CSV file that represents all expenses for the month.

## How to Run

This project requires some initial setup before you can run it.

1.  **Install UV**: This project uses **UV**, a package and project manager. You will need to install it first. A complete installation guide is available in the [official documentation](https://docs.astral.sh/uv/).

2.  **Set Your Income**: Create a file named `.env` in the project's root directory. In this file, add `INCOME=<your_income>` to the first line, replacing `<your_income>` with an integer or float.

3.  **View Instructions**: To see the complete instructions on how the script works and all its available options, run the `uv run main.py -h` command.