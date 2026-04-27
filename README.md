# 10 Academy Week 0 Challenge - Climate Trend Analysis

This repository contains the work for the **10 Academy Week 0 Challenge**: Artificial Intelligence Mastery, focusing on African Climate Trend Analysis (Ethiopia, Kenya, Sudan, Tanzania, Nigeria).

## Project Structure

├── .github/
│ └── workflows/
│ └── ci.yml
├── notebooks/
├── scripts/
├── src/
├── tests/
├── data/ # ← ignored (contains raw & cleaned CSVs)
├── venv/ # ← ignored
├── .gitignore
├── requirements.txt
└── README.md

## How to Reproduce the Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/qalindan/climate-challenge-week0.git
   cd climate-challenge-week-0
   ```
2, Activate the virtual environment (Windows):
   ```bash
   venv\Scripts\activate
   ```
3, Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4, Launch Jupyter Notebook:
   ```bash
   jupyter notebook
   ```

## CI/CD Status
GitHub Actions CI workflow is set up and will run on every push to main.
Submitted as part of Task 1 - Git & Environment Setup (April 2026)

#### 2. Commit the README.md

After saving the README, run these commands:

```bash
git add README.md
git commit -m "docs: add README with setup instructions"
