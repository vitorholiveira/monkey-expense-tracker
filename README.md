# Expense Tracker

I developed this project to better control my expenses. The `main.py` script is designed to add new expenses to a CSV file that tracks all expenses for the month. The `utils/config` file has all the configuration constants that you can change if you'd like to customize the program.

## How to Run

This project requires a few steps to get started.

1.  **Install UV**: This project uses **UV**, a package and project manager. You'll need to install it first. For a complete guide, refer to the [official documentation](https://docs.astral.sh/uv/).

2.  **Set Your Income**: In the `income/` directory, copy the file `.income.example.json` and rename it to `.income.json`. Then, update the date (in `YYYY-MM` format) and set your income for your currency.

3.  **View Instructions**: To see a full list of instructions and all available script options, run the `uv run main.py -h` command.

## Data Visualization

I also created a dashboard using Dash to visualize both monthly and custom time-range expenses. To run it, use the command: `uv run app.py`.