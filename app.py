import folium
from flask import Flask, render_template,url_for




app = Flask(__name__)
@app.route('/')
def index ():
    return '<img  src = "'+url_for('static', filename='demo-screen-1.jpg') +'" alt= "logo sncf"></br> <a href="'+ url_for("shortest")+'"><h3> Fast Route</h3> </a></br><a href="'+ url_for("co2_emission")+'"><<h3> Co2 Emission</h3> </a>'


@app.route('/shortest')
def shortest():
    return render_template ('shortestpath.html')
@app.route('/Co2')
def co2_emission():
    return render_template ('co2_emission.html')
    
    

if __name__ == "__main__":
    app.run(debug=True,host='localhost', port= 8000)


