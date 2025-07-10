from flask import Flask, render_template, request
import pandas as pd
import os
import webbrowser
from threading import Timer

app = Flask(__name__)

# Load Excel file
file_path = 'hospitals_data.xlsx'
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
df = pd.read_excel(file_path)

@app.route('/hospitals-status')  # new default route
def home():
    return render_template('search.html', hospital_info=None, step="initial")

@app.route('/search', methods=['GET'])
def search():
    name = request.args.get('hospital_name', '').strip().lower()
    hospital = df[df['Hospital Name'].str.lower().str.contains(name)]

    if hospital.empty:
        return render_template('search.html', hospital_info=None, step="initial", error="No hospital found with that name.")

    info = hospital.iloc[0].to_dict()
    return render_template('search.html', hospital_info=info, step="details")

def open_browser():
    # Opens the browser to the new route: hospitals-status
    webbrowser.open_new("http://127.0.0.1:5000/hospitals-status")

if __name__ == "__main__":
    Timer(1.25, open_browser).start()
    app.run(debug=True) 