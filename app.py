from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'hola'

API_KEY = "f6b36cb84f3b46fab7d19b28bcb4c681"
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/alcohol", methods=["GET", "POST"])
def alcohol():
    if request.method == "POST":
        max_alcohol = request.form.get("max_alcohol", "").strip()

        if not max_alcohol.isdigit():
            flash("Ingresa un número válido para maxAlcohol.", "error")
            return redirect(url_for("alcohol"))

        try:
            url = (
                f"{BASE_URL}?apiKey={API_KEY}"
                f"&number=10"
                f"&addRecipeNutrition=true"
                f"&maxAlcohol={max_alcohol}"
            )

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                recipes = data.get("results", [])

                return render_template(
                    "alcohol.html",
                    recipes=recipes,
                    max_alcohol=max_alcohol
                )
            else:
                flash(f"Error en la API (código {response.status_code}).", "error")
                return redirect(url_for("alcohol"))

        except requests.exceptions.RequestException as e:
            flash(f"Error al conectar: {e}", "error")
            return redirect(url_for("alcohol"))

    # GET
    return render_template("alcohol.html", recipes=[], max_alcohol=None)


if __name__ == "__main__":
    app.run(debug=True)
