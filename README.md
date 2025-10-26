# 🧩 Order Data Processing Pipeline

This is a modular **data processing pipeline** built in Python to clean, validate, transform, analyze, and export a  sample order data.  
This project is designed for **test-driven development (TDD)** with **pytest**, ensuring each step in the pipeline performs accurately and reliably.

---

## 📂 Project Structure
```
├── orderpipeline/
│ ├── init.py
│ ├── reader.py
│ ├── validator.py
│ ├── transformer.py
│ ├── analyzer.py
│ ├── exporter.py
│ └── pipeline.py
│
├── tests/
│ ├── test_reader.py
│ ├── test_validator.py
│ ├── test_transformer.py
│ ├── test_analyzer.py
│ ├── test_exporter.py
│ └── test_pipeline.py
│
├── data/
│ ├── shoplink_orders.json
│ └── cleaned_shoplink.json
│
├── main.py
├── uv.lock
├── pyproject.toml
└── README.md
```

---

## ⚙️ Pipeline Workflow

The pipeline is composed of **five core classes**, each handling a specific stage of data processing:

| Step | Class | Description |
|------|--------|-------------|
| 1️⃣ | `ReadJson` | Reads and loads JSON order data into memory. |
| 2️⃣ | `Validator` | Ensures required fields exist and filters out invalid rows. |
| 3️⃣ | `Transformer` | Converts data types, normalizes payment status, and cleans text. |
| 4️⃣ | `Analyzer` | Computes key metrics such as total revenue, average order value, and payment distribution. |
| 5️⃣ | `Exporter` | Writes the cleaned and analyzed results to a JSON output file. |


The **`pipeline.py`** script orchestrates all these components, while **`main.py`** serves as the pipeline’s entry point.

---

## 🚀 Running the Pipeline

Run the main script directly from the terminal:

```bash
uv run main.py
```

If you’re not using uv, simply run:

```bash
python main.py
```

This executes the full workflow — reading raw data, validating, transforming, analyzing, and exporting to a new file (cleaned_shoplink.json).

## 🧪 Running Tests
This project is built with pytest for modular unit testing.

Run all tests:
``` bash
pytest -v
```

To generate a coverage report:
```bash
pytest --cov=order_pipeline
```

## 🧰 Tech Stack

* Language: Python 3.11+

* Testing: Pytest, pytest-cov

* Environment: uv / venv

* Format: JSON-based data input/output


# 🪪 Author

Ebuka Obobo
Data & Pharmacy Analytics Enthusiast
Built as part of an advanced testing and data engineering practice project.