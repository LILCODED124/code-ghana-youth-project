from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression

app = Flask(__name__)  # ← this must come BEFORE @app.route

# Load and train model
data = pd.read_csv("data.csv")
X = data[["month"]].values
y = data["sales"].values
model = LinearRegression()
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    if request.method == 'POST':
        try:
            month = int(request.form['month'])
            if 1 <= month <= 12:
                prediction = model.predict([[month]])[0]

                # Save to prediction log
                with open("predictions.csv", "a") as f:
                    f.write(f"{month},{prediction}\n")

            else:
                prediction = "Invalid month. Enter 1–12."
        except:
            prediction = "Invalid input."

    data_pairs = list(zip(data["month"], data["sales"]))
    months = list(data["month"])
    sales = list(data["sales"])

    return render_template(
        'index.html',
        prediction=prediction,
        data=data_pairs,
        months=months,
        sales=sales
    )

if __name__ == "__main__":
    app.run(debug=True)