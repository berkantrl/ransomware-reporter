# Ransomware Reporter

**Ransomware Reporter** is a Python application that automatically fetches, analyzes, and reports the latest ransomware incidents. It can generate detailed reports in both JSON and Word formats, visualize statistics, and optionally send reports via email. The tool supports both English and Turkish and can be scheduled for periodic reporting.

---

## Features

- Fetches recent ransomware victim data from a public API.
- Generates detailed JSON and Word reports.
- Provides sector, group, country, and continent-based statistics and charts.
- Supports both English and Turkish languages.
- Can send reports via email (Gmail or Outlook).
- Supports periodic (scheduled) reporting.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/berkantrl/ransomware-reporter.git
cd ransomware-reporter
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install the main dependencies manually:

```bash
pip install requests googletrans==4.0.0-rc1 pycountry-convert python-docx matplotlib seaborn python-dateutil
```

### 3. Configure Email Settings

Create a file at `config/email_config.json` with your email credentials:

```json
{
  "sender_email": "your_email@example.com",
  "password": "your_email_password",
  "receiver_email": "receiver@example.com",
  "service": "google"  // or "outlook"
}
```

---

## Usage

### Basic Usage

```bash
python report.py -d 7 -l en -r
```

- `-d`, `--day`: Number of days to include in the report (1-40)
- `-l`, `--lang`: Report language (`en` or `tr`)
- `-r`, `--report`: Generate a Word report
- `-m`, `--mail`: Send the report via email periodically

### Examples

- **Generate only a JSON report:**
  ```bash
  python report.py -d 10
  ```

- **Generate a Word report:**
  ```bash
  python report.py -d 7 -r
  ```

- **Generate and email a Word report periodically:**
  ```bash
  python report.py -d 7 -r -m
  ```

---

## Project Structure

```
ransomware-reporter/
│
├── report.py
├── utils/
│   ├── fetcher.py
│   ├── reporter.py
│   ├── send.py
│   └── config/
│       └── email_config.json
├── data/
├── reports/
├── charts/
└── README.md
```

- **report.py:** Main entry point.
- **utils/fetcher.py:** Fetches and processes data from the API.
- **utils/reporter.py:** Generates Word reports and charts.
- **utils/send.py:** Sends reports via email.
- **data/**: Stores JSON data files.
- **reports/**: Stores generated Word reports.
- **charts/**: Stores generated chart images.

---

## Notes

- For email sending, you may need to enable "less secure app access" on your email account.
- Make sure the `data`, `reports`, and `charts` folders exist, or create them before running the script.

---

## Contact

For questions or suggestions, please contact
