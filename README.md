# Capstone_Selenium — Test Automation Project

A Selenium-based end-to-end test automation framework built with pytest.  
This repo provides reusable utilities, a keyword engine, example data files (CSV/XLSX), and integration with Allure reporting. It is intended as a capstone/test automation reference project.

---

Table of Contents
- [Quick start](#quick-start)
- [Prerequisites](#prerequisites)
- [Install](#install)
- [Run tests](#run-tests)
- [Allure reporting](#allure-reporting)
- [Selenium Grid / Cloud providers](#selenium-grid--cloud-providers)
- [Data sources](#data-sources)
- [Keyword-driven execution](#keyword-driven-execution)
- [Project structure](#project-structure)
- [Contributing](#contributing)
- [License & Contact](#license--contact)

---

## Quick start

Windows (cmd.exe)
```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
pytest tests
```

macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest tests
```

---

## Prerequisites

- Python 3.8+
- pip
- (Optional) Allure CLI for serving reports
- (Optional) A Selenium Grid or cloud provider (e.g., Selenium Grid, BrowserStack, Sauce Labs) if running remote tests
- For Excel support: pandas and openpyxl (install via requirements.txt if needed)

---

## Install

1. Clone the repo
```bash
git clone https://github.com/PratyushJaishankar/ASC_Capstone.git
cd ASC_Capstone
```

2. Create & activate a virtual environment and install dependencies
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Run tests

Run all tests (single process)
```bash
pytest tests
```

Run tests in parallel (requires pytest-xdist)
```bash
pytest tests -n auto
```

Run tests and store Allure results
```bash
pytest tests -n auto --alluredir=reports/allure-results
```

Examples that use environment variables (Windows CMD shown):
```cmd
set SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
set BROWSER=chrome
pytest tests -n 1 --alluredir=reports/allure-results
```

On macOS/Linux:
```bash
export SELENIUM_REMOTE_URL=http://localhost:4444/wd/hub
export BROWSER=chrome
pytest tests -n 1 --alluredir=reports/allure-results
```

Notes:
- The tests and fixtures are configured via `conftest.py`.
- Use `-k` or `-m` pytest options to select tests if needed.

---

## Allure reporting

To generate and serve an Allure report after running tests with `--alluredir=reports/allure-results`:

1. Ensure Allure CLI is installed and on your PATH (https://docs.qameta.io/allure/).
2. Serve the report:
```bash
allure serve reports/allure-results
```

---

## Selenium Grid / Cloud providers

- To run tests against a remote Selenium Grid or a cloud provider, set `SELENIUM_REMOTE_URL` to your grid/provider URL and set `BROWSER` to the desired browser name.
- The driver creation and remote capability handling are centralized in `utils/driver_utils.py`. Extend or adapt that file for provider-specific capabilities.

Example:
```bash
export SELENIUM_REMOTE_URL="http://localhost:4444/wd/hub"
export BROWSER="chrome"
pytest tests
```

---

## Data sources

- Test data files live in the `data/` directory.
- Supported formats: CSV and Excel (.xlsx). The main loader is `data/data_loader.py`.
- Example files include `data/add_customer_data.csv`, `data/login_data.csv`, `data/search_data.csv`.
- CSV rows can include an optional `result` column with `success` or `failed` to indicate expected outcome for that row. Tests will treat rows marked `failed` accordingly (see `data/data_loader.py` for behavior).

Example CSV row:
```csv
first_name,last_name,email,password,result
Jane,Doe,jane.doe+1@example.com,Pass@1234,success
```

---

## Keyword-driven execution

A lightweight keyword engine is available at `utils/keyword_engine.py`. Use it to define keyword-driven steps in CSV (example: `data/keywords.csv`).

Example usage:
```python
from utils.keyword_engine import load_keywords, run_keywords
from utils.driver_utils import get_driver

driver = get_driver('chrome')
steps = load_keywords('data/keywords.csv')
run_keywords(driver, steps)
driver.quit()
```

---

## Project structure

Top-level files & directories you will find in this repository:
- .github/                — GitHub workflow configs (if present)
- .gitignore
- .idea/                  — IDE configs (PyCharm)
- conftest.py             — pytest fixtures and configuration
- data/                   — test data files (CSV/XLSX)
- page_objects/           — page object classes used by tests
- requirements.txt        — Python dependencies
- tests/                  — pytest test cases
- utils/                  — helpers (driver_utils.py, keyword_engine.py, etc.)
- reports/                — test reports / allure-results (generated)

---

## Contributing

1. Fork the repository.
2. Create a feature branch: git checkout -b feat/short-description
3. Commit changes: git commit -m "Add short-description"
4. Push and open a PR.

Before submitting:
- Run linters and tests locally.
- Keep tests deterministic where possible.
- Add or update data/examples when changing test flows.

---

## License & Contact

This project is maintained by Pratyush Jaishankar (github: @PratyushJaishankar).  
For questions or issues, please open an issue in this repository.

If you want a tailored README (for example: CI badges, exact environment variables, or a usage walkthrough with screenshots), update this repo with any missing information and I can help incorporate it.
