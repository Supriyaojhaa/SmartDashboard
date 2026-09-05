# Smart Data Processing & Validation Dashboard

A full-stack Python web application that performs data validation, processing, analysis, and visualization using advanced Python concepts.

---

## Project Structure

```
smart_data_system/
│
├── backend/
│   ├── app.py
│   ├── data/
│   │   └── datasets.json
│   ├── modules/
│   │   ├── base_processor.py
│   │   ├── processing.py
│   │   ├── validation.py
│   │   ├── serialization.py
│   │   ├── threading_tasks.py
│   │   └── multiprocessing_tasks.py
│   └── utils/
│       ├── decorators.py
│       ├── generators.py
│       ├── iterators.py
│       └── mixins.py
│
├── frontend/
│   ├── templates/
│   │   ├── index.html
│   │   └── dashboard.html
│   └── static/
│       ├── style.css
│       └── charts/
│
├── requirements.txt
└── README.md
```

---

## Installation

**1. Clone or download the project**

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the application**
```bash
cd backend
python app.py
```

**5. Open in browser**
```
http://127.0.0.1:5000
```

---

## How to Use

1. Open the app in your browser
2. Fill in your Name, Email, Phone Number, and Password
3. Upload a CSV or JSON dataset file
4. Click **Analyze Dataset**
5. On the dashboard, select which columns to analyze using the sidebar checkboxes
6. Click **Apply** to display stats and charts for selected columns
7. Use the **X Axis dropdown** on each chart to change the X axis instantly

---

## Features

- User input validation using Regular Expressions
- CSV and JSON dataset upload and processing
- Column statistics — Mean, Median, Standard Deviation
- Data visualization — Line Graph, Bar Graph, Histogram
- Filter panel — select which columns to display
- Custom X axis selection per chart (updates instantly)
- Full dataset preview with scroll
- JSON storage of processed results
- Concurrent processing using Threading and Multiprocessing

---

## Python Concepts Implemented

| Concept | Where Used |
|---|---|
| Abstract Class (ABC) | `base_processor.py` — `BaseProcessor` |
| Multiple Inheritance | `processing.py` — `AdvancedProcessor(BaseProcessor, LoggingMixin, ExportMixin)` |
| Mixin Classes | `mixins.py` — `LoggingMixin`, `ExportMixin` |
| Custom Iterator | `iterators.py` — `DatasetIterator` with `__iter__`, `__next__`, `__len__`, `__str__`, `__add__` |
| Generator | `generators.py` — `data_generator()` |
| Closure | `generators.py` — `multiplier()` returns inner function |
| Decorators | `decorators.py` — `@log_function`, `@timer` |
| Regular Expressions | `validation.py` — validates name, email, phone, password |
| Multithreading | `threading_tasks.py` — `run_threading()` called in `app.py` |
| Multiprocessing | `multiprocessing_tasks.py` — `run_process()` called in `app.py` |
| JSON Serialization | `serialization.py` — `save_results()` stores stats to `datasets.json` |
| Operator Overloading | `iterators.py` — `__len__`, `__str__`, `__add__` |
| Core Libraries | `os`, `sys`, `datetime`, `math`, `re`, `json` used throughout |
| External Libraries | `pandas`, `numpy`, `matplotlib` for data processing and visualization |

---

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Libraries:** pandas, numpy, matplotlib
- **Storage:** JSON

---

## Requirements

```
flask
pandas
numpy
matplotlib
```

---

## Notes

- Upload CSV or JSON files only
- Password must contain letters and numbers, minimum 6 characters
- Phone number must be exactly 10 digits
- Charts are generated automatically for all numeric columns