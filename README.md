# MOHU Waste Collection to Google Calendar Automation

## 🎯 Goal

My goal is to **automatically see MOHU (MOL Hulladékgazdálkodási Zrt.) waste collection dates in Google Calendar**.

Currently, the official [MOHU website](https://mohubudapest.hu/hulladeknaptar) only shows pickup dates **one month in advance**, which makes manual calendar maintenance inconvenient.  
Therefore, I want to **automate the creation and update of calendar events** using **Google Apps Script**.


---

## 🧩 Implementation Steps

### Python – Fetch MOHU Dates
Use a Python script to query the waste collection dates from the MOHU website.  
Python is my primary programming language, so I implemented the web-scraping logic here.

### [Google Apps Script](https://script.google.com/home)

There are three separate Google Apps Script demos, each serving a different purpose:

#### 🗓️ **1. Calendar Demo**
- Creates a Google Calendar event based on a string-defined date and event name.  
- Includes a separate script for deleting those events.

#### ♻️ **2. MOHU Demo**
- Retrieves the MOHU waste collection dates from the website and prints them to the console for verification.

#### 🔄 **3. MohuToCalendar**
- Fetches waste collection dates from the MOHU website  
- Updates or recreates the corresponding events in Google Calendar automatically

---
## 📂 Project Structure

- Each implementation step is a **standalone script**, runnable independently  
- Scripts are organized into **separate folders** for clarity  
- Each folder contains its **own `README.md`** explaining how to use that specific component

---

## ⚙️ Usage Notes

- For **beginner Google Apps Script users**, it is highly recommended to test each demo script individually before running the final combined script.  
- The **final script runs only once** by default — automation (e.g., daily or monthly trigger) must be configured manually within **Google Apps Script**.

The final combined script can be found here:  
📁 `TBD…`

---

## 🧠 Summary

| Component                        | Purpose                                                     |
|----------------------------------|-------------------------------------------------------------|
| **Python Script**                | Fetches MOHU waste collection dates via HTTP + HTML parsing |
| **Calendar Demo (Apps Script)**  | Creates/deletes calendar events manually                    |
| **MOHU Demo (Apps Script)**      | Verifies that MOHU data can be fetched successfully         |
| **MohuToCalendar (Apps Script)** | Full automation: fetch + calendar sync                      |

---

## 📜 License

This project is free to use and modify for personal automation and learning purposes.  
If you publish derived work, please include a reference to this repository.

---

**Author:** Kiki   
**Created:** November 2025