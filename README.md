# LeadGen-Challenge
A plug-and-play toolset to help sales and growth teams find, verify, and prioritize leads faster by automating repetitive tasks like domain lookup, email guessing, and CSV cleanup.

# 🔍 LeadGen Challenge Tools – Internship Task

This mini toolkit replicates and improves upon core functionalities of tools like [SaaSquatch Leads](https://www.saasquatchleads.com/), enabling smarter, faster B2B lead generation workflows.

## 📦 Tools Included

### 1. `hunter.py` – Email Discovery + Verifier (Hunter Lite)
- Predicts email formats using name + domain
- Verifies using SMTP and MX record logic

### 2. `lead_scorer.py` – Smart Lead Prioritizer
- Assigns scores based on title, domain, and email verification status
- Helps sales teams prioritize better leads

### 3. `domain_finder.py` – Domain Detection via DuckDuckGo
- Finds company domains using scraped search engine results
- Works on single input or CSV batch

### 4. `lead_formatter.py` – Data Cleaner
- Normalizes name, email, and title formats for better consistency

---

## 🚀 How to Run

1. Install dependencies
2. Run any tool
3. Input/output is via CSV or CLI prompts.

## ✅ Why This Matters

These tools automate repetitive tasks like email discovery, domain lookup, and lead cleaning. They are ideal for SDRs, growth teams, or any outbound pipeline that needs to scale fast with quality.

📊 Lead Scoring Model (lead_scoring_model.py)
This tool uses a machine learning model to score leads based on key features such as title seniority, domain reputation, email verification confidence, and LinkedIn presence. It helps prioritize high-quality leads for outreach.

🔧 Features
Trains a regression model (GradientBoostingRegressor) on labeled lead data.

Predicts lead quality score (0–100) for new entries.

Supports both interactive prediction and batch training via CSV.

