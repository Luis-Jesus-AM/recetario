from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'hola'

API_KEY = "f6b36cb84f3b46fab7d19b28bcb4c681" 
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/receta", methods=["GET", "POST"])
def receta():
    if request.method == "POST":
        search_term = request.form.get('search_term', '').strip().lower()
        
        if not search_term:
            flash('Por favor, ingresa un término de búsqueda válido', 'error')
            return redirect(url_for('receta'))
        
        try:
            url = f"{BASE_URL}?query={search_term}&apiKey={API_KEY}&number=10&cuisine=any"
            response = requests.get(url)

            if response.status_code == 200:
                recipes = response.json().get("results", [])
                if recipes:
                    return render_template('receta.html', recipes=recipes, search_term=search_term)
                else:
                    flash(f'No se encontraron recetas para "{search_term}"', 'error')
                    return redirect(url_for('receta'))
            else:
                flash(f'Error al consultar la API de Spoonacular. Código de estado: {response.status_code}', 'error')
                return redirect(url_for('receta'))
        
        except requests.exceptions.RequestException as e:
            flash(f'Hubo un error al conectarse con la API: {e}', 'error')
            return redirect(url_for('receta'))

    return render_template("receta.html", recipes=[], search_term=None)


if __name__ == "__main__":
    app.run(debug=True)

