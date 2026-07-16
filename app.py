"""
Flask entry point.

Pipeline:
    XML file -> modules/xml_parser.py -> pandas DataFrame
             -> modules/data_processing.py -> cleaned DataFrame
             -> modules/db.py -> sqlite
             -> Flask route -> JSON / HTML response
"""
from flask import Flask, jsonify, request, render_template
import os
from modules import db, xml_parser, data_processing

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "mydata.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    """Simple sanity check route."""
    return jsonify(status="ok")


@app.route("/import-xml", methods=["POST"])
def import_xml():
    """
    Expects a POST with an uploaded XML file under form field 'file'.
    Parses it, cleans it with pandas, and stores it in sqlite.
    """
    if "file" not in request.files:
        return jsonify(error="No file uploaded, expected form field 'file'"), 400

    xml_file = request.files["file"]
    xml_bytes = xml_file.read()

    # 1. Parse XML -> list of dicts
    records = xml_parser.parse_xml(xml_bytes)

    # 2. Load into DataFrame and clean
    df = data_processing.records_to_dataframe(records)
    df = data_processing.clean_dataframe(df)

    # 3. Persist to sqlite
    conn = db.get_connection(DB_PATH)
    db.save_dataframe(conn, df, table_name="items")
    conn.close()

    return jsonify(rows_imported=len(df))


@app.route("/items")
def list_items():
    """Return everything currently stored in sqlite as JSON."""
    conn = db.get_connection(DB_PATH)
    df = db.read_table(conn, table_name="items")
    conn.close()
    return jsonify(df.to_dict(orient="records"))


if __name__ == "__main__":
    db.init_db(DB_PATH)
    app.run(debug=True)