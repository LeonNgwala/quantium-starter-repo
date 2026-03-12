# Pink Morsel Sales Analysis Dashboard

A modern, interactive Dash application for analyzing the sales of **Pink Morsels** across different regions. This project was developed as part of the Quantium data analyst program.

## Features

- **Interactive Line Chart**: Visualize monthly sales trends for Pink Morsels.
- **Regional Filtering**: Filter data by region (North, East, South, West, or All).
- **Date Range Picker**: Focus on specific time periods for granular analysis.
- **Price Increase Indicator**: A visual marker at January 15, 2021, to highlight the impact of the price increase.
- **Data Export**: Download the filtered sales data directly as a CSV file.
- **Modern UI**: Styled with clean, responsive Vanilla CSS and a Quantium-inspired theme.

## Getting Started

### Prerequisites

- Python 3.9+
- Chrome Browser (for integration tests)

### Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd quantium-starter-repo
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Data Processing

Before running the dashboard, the raw data in the `data/` directory must be processed. This script cleans the data, calculates total sales, and prepares it for the dashboard.

```bash
python process_data.py
```
This will generate the `processed_sales_data.csv` file.

### Running the Dashboard

To launch the Dash application:

```bash
python app.py
```
By default, the app will be available at `http://127.0.0.1:8050/`.

## Testing

This project uses `pytest` and `Selenium` for automated integration testing.

To run the test suite:
```bash
pytest test_app.py
```
The tests are also automated via GitHub Actions on every push and pull request to the `main` branch.

## Project Structure

- `app.py`: The main Dash application.
- `process_data.py`: Script to clean and prepare the sales data.
- `assets/`: Custom CSS for modern styling.
- `test_app.py`: Integration tests using Selenium.
- `data/`: Raw CSV files containing daily sales data.
- `.github/workflows/ci.yml`: CI configuration for automated testing.
