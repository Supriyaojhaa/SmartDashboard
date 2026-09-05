from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd

from modules.validation import validate_user
from modules.processing import process_dataset, generate_column_chart 
from modules.threading_tasks import run_threading
from modules.multiprocessing_tasks import run_process, sample_task

app = Flask(__name__,
            template_folder="../frontend/templates",
            static_folder="../frontend/static")

UPLOAD_FOLDER = "data"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sample-dataset")
def sample_dataset():
    """Serves the sample dataset for quick testing and demo loading."""
    sample_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample_dataset.csv")
    if os.path.exists(sample_path):
        return send_file(sample_path, as_attachment=True, download_name="sample_dataset.csv", mimetype="text/csv")
    return jsonify({"error": "Sample dataset not found"}), 404


@app.route("/download-results")
def download_results():
    """Serves the latest processed JSON results."""
    results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "datasets.json")
    if os.path.exists(results_path):
        return send_file(results_path, as_attachment=True, download_name="analyzed_results.json", mimetype="application/json")
    return jsonify({"error": "No results available yet"}), 404


@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")

    # validation
    validation_result = validate_user(name, email, phone, password)

    if validation_result != "Valid":
        return validation_result, 400

    file = request.files.get("dataset")

    stats = None
    preview = None
    filepath = None
    all_columns = []
    row_count = 0
    col_count = 0
    numeric_count = 0
    filename = "Uploaded Dataset"

    if file and file.filename != "":
        filename = file.filename
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        filepath = os.path.abspath(filepath)
        file.save(filepath)

        # dataset preview
        filepath_lower = filepath.lower()
        try:
            if filepath_lower.endswith(".csv"):
                try:
                    df = pd.read_csv(filepath)
                except pd.errors.ParserError:
                    df = pd.read_csv(filepath, on_bad_lines="skip")
            elif filepath_lower.endswith(".json"):
                df = pd.read_json(filepath)
            else:
                return "Invalid file format. Please upload a CSV or JSON file.", 400
        except Exception as e:
            return f"Error reading file: {str(e)}", 400

        if df.empty or len(df) == 0:
            return "Uploaded dataset contains no data rows. (Note: datasets.json is the system output summary file, not an input dataset. Please upload sample_dataset.csv or a tabular JSON/CSV file.)", 400

        preview = df.to_html(classes="preview-table", index=False)

        # all columns for X axis dropdown
        all_columns = list(df.columns)
        row_count = len(df)
        col_count = len(df.columns)

        # MULTITHREADING (working)
        run_threading(process_dataset, filepath)

        # MULTIPROCESSING (working)
        run_process(sample_task, df.values.tolist())

        # MAIN PROCESSING (for dashboard)
        stats = process_dataset(filepath)
        numeric_count = len(stats.keys()) if stats else 0
    else:
        return "Please upload a CSV or JSON dataset file.", 400

    if filepath:
        filepath = filepath.replace("\\", "/") 

    return render_template("dashboard.html", 
                           stats=stats, 
                           preview=preview,
                           filepath=filepath,
                           all_columns=all_columns,
                           row_count=row_count,
                           col_count=col_count,
                           numeric_count=numeric_count,
                           filename=filename)


# generates custom charts based on user selected axes

@app.route("/update_column_chart", methods=["POST"])
def update_column_chart():
    data = request.get_json()
    x_col = data.get("x_col")
    y_col = data.get("y_col")
    filepath = data.get("filepath")

    result = generate_column_chart(filepath, x_col, y_col)

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Failed"}), 400


if __name__ == "__main__":
    app.run(debug=True)