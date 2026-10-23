# Python Projects

A portfolio of small, practical Python applications built to practice software development, automated testing, data handling, and Streamlit interfaces.

## Projects

| Project | Description | Tests |
|---|---|---:|
| [FinTrack Lite](fintrack-lite/) | Personal finance tracker with CSV import/export and dashboard | 4 |
| [TaskFlow Python](taskflow-python/) | Task manager with SQLite persistence | 5 |
| [QuizLab](quizlab/) | Multiple-choice quiz engine with scoring and JSON question data | 5 |
| [DataClean Mini](dataclean-mini/) | CSV cleaning and preview tool using pandas and Streamlit | 5 |
| [FileOrganizer](fileorganizer/) | Organizes files by extension with preview and confirmation before moving | 6 |

**Initial automated test status:** 25 tests passed across the five projects in local validation. This is a baseline validation, not a claim of production readiness.

## Run a project

Each project has its own dependencies, README, and tests. Example:

```bash
cd fintrack-lite
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Repeat the commands inside the directory of the project you want to run. Use Python 3.9 or newer where supported by the individual project's dependencies; check each project README for details.

## Repository structure

Each top-level folder is an independent project. Runtime data, virtual environments, and local test files should remain local and not be committed unless specifically documented by a project.

## About

This repository is dedicated to Python development projects. The NEXA Studio brand, institutional website, and other business materials remain in [NEXA-Studio](https://github.com/sayjinblackbelt/NEXA-Studio).
