# MOHU Budapest Selective Waste Calendar Scraper

This Python script allows you to **automatically query selective waste collection dates** from the official [MOHU Budapest Waste Calendar](https://mohubudapest.hu/hulladeknaptar) website.

The site provides collection dates via **AJAX requests** that depend on district, street, and house number selections.  
This tool automates those interactions, parses the returned HTML fragments, and extracts the relevant **selective collection days**.

---

## 🧩 Features

- Queries the live MOHU Budapest waste calendar through the same AJAX mechanism the website uses  
- Automatically navigates:
  1. District →  
  2. Street →  
  3. House number →  
  4. Result table extraction
- Returns a clean list of upcoming **selective collection dates**
- Includes robust parsing with **BeautifulSoup**
- Logs activity using Python’s built-in **logging** module

---

## 🗂️ File Overview

### `mohu.py`
Main Python file containing:
- `pick_option()` — Finds matching `<option>` values from a select menu  
- `extract_dates()` — Extracts selective waste dates from AJAX response HTML  
- `fetch_garbage()` — Performs the full query process and returns date list  
- Example usage in `__main__`

Each function is documented with English docstrings for clarity and reusability.

---

## ⚙️ Installation

You can use `start.bat`, which    
creates a virtualenv,   
installs dependencies,    
updates the github project,   
and starts the `mohu.py` project.

## 🚀 Usage

In the `__main__` function of `mohu.py`, **overwrite** the default address and then **run** `mohu.py`.

By default, it will query the following example address:

District: 1062  
Street:   Andrássy  
House:    57

You should see **output** similar to:

Szelektív napok: ['2025.01.12.', '2025.02.09.', '2025.03.09.', ...]


## 📜 Logging

The script uses Python’s logging module to print info-level logs to the console when loaded or run directly:

2025-11-03 14:12:10 INFO [__main__] Loaded MOHU Budapest waste calendar scraper module.  
2025-11-03 14:12:11 INFO [__main__] Running example query for selective collection dates...  
2025-11-03 14:12:12 INFO [__main__] Found 6 selective dates for the sample address.

## 📦 Dependencies

requests — for handling HTTP sessions and AJAX POST requests  
beautifulsoup4 — for parsing returned HTML fragments  
json, logging — Python standard library modules


## ⚖️ License

You may use and modify this script freely under the MIT License.

Author: Krisztián Bársony  
File: mohu.py  
Created: November 2025  