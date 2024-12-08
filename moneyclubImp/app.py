from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import subprocess
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'output/'

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Reset variables on each request
processed_data = None  # Reset to initial state

# Helper function to delete files in a folder
def clear_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route('/')
def index():
    # Reset processed data and clear files in the upload/output directories
    global processed_data
    processed_data = None
    clear_files(UPLOAD_FOLDER)  # Clear uploaded files
    clear_files(OUTPUT_FOLDER)  # Clear output files
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if files are uploaded
    if 'screenshot' not in request.files or 'statement' not in request.files:
        return "Missing file upload. Please upload both files."

    # Save files to the uploads directory
    screenshot = request.files['screenshot']
    statement = request.files['statement']

    screenshot_path = os.path.join(UPLOAD_FOLDER, screenshot.filename)
    statement_path = os.path.join(UPLOAD_FOLDER, statement.filename)

    screenshot.save(screenshot_path)
    statement.save(statement_path)

    # Run the moneyclub.py script
    subprocess.run(['python', 'code/moneyclub.py', screenshot_path, statement_path], check=True)

    # Assuming moneyclub.py generates 'output/result.csv'
    output_csv = os.path.join(OUTPUT_FOLDER, 'result.csv')

    if not os.path.exists(output_csv):
        return "Processing failed. CSV file not generated."

    # Read the CSV file and send its contents to the template
    csv_data = pd.read_csv(output_csv)
    table_data = csv_data.to_dict(orient='records')  # Convert DataFrame to list of dictionaries
    columns = csv_data.columns.tolist()  # Get column names
    return render_template('result.html', table_data=table_data, columns=columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
