from flask import Flask, render_template, request
import joblib
from datetime import date
import pickle

model = joblib.load('Water_Quality_ML_trained_model.save')
app = Flask(__name__)
year = date.today().year

@app.route("/")
def home():
    return render_template('home.html', current_year=year)




@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        try:
            ph = float(request.form['ph'])
            if 0 <= ph <= 14:
                dummy_input = [[ph, 0, 0, 0, 0, 0, 0, 0, 0]]
                predictions = model.predict(dummy_input)
                output = int(predictions[0])
                if ph <= 7:
                    purity = "pure"
                    prediction_text = "The water with given details is pure and potable enough to drink and meets the federal standards for domestic consumption."
                else:
                    purity = "impure"
                    prediction_text = "The water with given details is impure and may not be suitable for domestic consumption."
                return render_template('home.html', ph=ph, purity=purity, prediction_text=prediction_text)
            else:
                return render_template('home.html', error="Invalid pH value. Please enter a value between 0 and 14.")
        except ValueError:
            return render_template('home.html', error="Invalid input. Please enter a valid number for pH.")
    return render_template('home.html')


#         if output == 1:
#             return render_template('home.html', current_year=year, prediction_text="The water with given details is pure and potable enough to drink and meets the federal standards for domestic consumption.")
#         else:
#             return render_template('home.html', current_year=year, prediction_text="The water with specified details is impure, contaminated and non-potable. It may not be suitable for domestic consumption.")
if __name__ == "__main__":
        app.run(port=8080)
