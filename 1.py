from flask import Flask, request, jsonify
import psycopg2
import logging

# Set up Flask app
app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASSWORD = "Sa123"
DB_NAME = "demo12"

def check_database_health():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        cursor = conn.cursor()
        # Execute a test query
        cursor.execute("SELECT 1;")
        conn.close()
        return "Database is healthy."
    except Exception as e:
        return f"Database connection error: {e}"

@app.route("/webhook", methods=["POST"])
def webhook():
    logging.debug("Received request: %s", request.get_data(as_text=True))  # Log incoming requests
    data = request.get_json()
    intent = data.get("queryResult", {}).get("intent", {}).get("displayName", "")
    if intent == "CheckDatabaseHealth":
        response_text = check_database_health()
    else:
        response_text = "Unknown intent received."
    return jsonify({"fulfillmentText": response_text})

if __name__ == "__main__":
    # Enable Flask debug mode
    app.run(debug=True)
