
import aneel
import pandas as pd

from flask import Flask, redirect, render_template, request, url_for

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/import", methods=["GET", "POST"])
def importAneelData():
    if request.method == "POST":
        
        month_year = request.form.get("monthYear")
        
        if (month_year is None):
            return ('Bad Request', 400)
        
        year,month = month_year.split('-')
            
        data = aneel.getAneelData(month, year)

        if data is None:
            return ('Service Unavailable', 503)

        if aneel.storeAneelData(month, year, data) is None:
            return ('Internal Server Error', 500)
        
        return redirect(url_for('display', monthYear=month_year))
    else:
        return render_template("import.html")

@app.route('/selectDisplay')
def selectDisplay():
    return render_template('Selectdisplay.html')
   
@app.route('/display')
def display():
    
    month_year = request.args.get('monthYear')
    

    if (month_year is None):
            return ('Bad Request', 400)
        
    year,month = month_year.split('-')
    
    data = aneel.readAneelStoredData(month, year)
    
    if (data is None):
        return redirect('/selectDisplay')
    
    # Criar um DataFrame a partir dos dados
    df = pd.DataFrame(data)

    # Agrupar os valores pelos rótulos
    agrupado = df.groupby('DscClasseConsumo')['totalempreendimentos'].sum().to_dict()
    
    graficoClasseConsumo = {'labels' : list(agrupado.keys()), 'values': list(agrupado.values())}
    
    agrupado = df.groupby('SigUF')['totalempreendimentos'].sum().to_dict()
    
    graficoUF = {'labels' : list(agrupado.keys()), 'values' : list(agrupado.values())}
    
    return render_template('display.html', year=year,month=month, graficoClasseConsumo = graficoClasseConsumo, graficoUF = graficoUF)

app.run()