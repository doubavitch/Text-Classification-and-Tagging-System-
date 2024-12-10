import joblib
from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import numpy as np

# Load the model and vectorizer
model = joblib.load('Model_MLP.joblib')
vectorizer = joblib.load('1_vectorizer_Logistic_one_hot.joblib')

app = Flask(__name__)

# Database setup function (run this once to initialize)
def setup_database():
    conn = sqlite3.connect('submissions.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abstract TEXT NOT NULL,
            prediction TEXT NOT NULL,
            corrected TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

@app.route('/reset_database', methods=['POST'])
def reset_database():
    with sqlite3.connect('submissions.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM submissions")  # Deletes all rows from the table
        conn.commit()
    return redirect(url_for('admin'))  # Redirect to the admin panel after reset


@app.route('/', methods=['GET', 'POST'])
def home():
    category = None
    abstract_text = None  # Store the input text

    if request.method == 'POST':
        # Get the text input from the form
        abstract_text = request.form['abstract']

        # Preprocess the text using the vectorizer
        vectorized_text = vectorizer.transform([abstract_text])

        # Make prediction using the loaded model
        category = model.predict(vectorized_text)[0]

        # Save submission to the database
        conn = sqlite3.connect('submissions.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO submissions (abstract, prediction) VALUES (?, ?)', (abstract_text, category))
        conn.commit()
        conn.close()

    # Render the home page with the input text and prediction
    return render_template('home.html', category=category, abstract_text=abstract_text)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Handle the update logic for corrections
        submission_id = request.form['id']
        new_tag = request.form['corrected_category']

        # Append the new tag to the existing tags
        with sqlite3.connect('submissions.db') as conn:
            cursor = conn.cursor()
            # Fetch the current corrected tags
            cursor.execute("SELECT corrected FROM submissions WHERE id = ?", (submission_id,))
            current_tags = cursor.fetchone()[0]

            # Append the new tag if there are existing tags
            if current_tags:
                updated_tags = f"{current_tags}, {new_tag}"
            else:
                updated_tags = new_tag

            # Update the database with the new tags
            cursor.execute(
                "UPDATE submissions SET corrected = ? WHERE id = ?",
                (updated_tags, submission_id)
            )
            conn.commit()

    # Fetch submissions in descending order of ID
    with sqlite3.connect('submissions.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM submissions ORDER BY id DESC")
        submissions = cursor.fetchall()

    # Pass the submissions to the template
    return render_template('admin.html', submissions=submissions)



@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

