import joblib
from flask import Flask, request, render_template
import numpy as np

# Load the model and vectorizer
model = joblib.load('2_Model_Logistic_MultiDiscipline.joblib')
vectorizer = joblib.load('1_vectorizer_Logistic_one_hot.joblib')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    category = None  # Initialize category as None

    if request.method == 'POST':
        # Get the text input from the form
        abstract_text = request.form['abstract']

        # Preprocess the text using the vectorizer
        vectorized_text = vectorizer.transform([abstract_text])

        # Make prediction using the loaded model
        category = model.predict(vectorized_text)[0]  # The predicted category

    # Render the home page with the prediction (or None if no prediction)
    return render_template('home.html', category=category)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
