import folium
from flask import Flask, render_template,url_for
import data_trip 



app = Flask(__name__)
@app.route('/')
def index ():
    trip_time = str(data_trip.get_time())
    trip_co2 = str(data_trip.get_co2())

    return '<img  src = "'+url_for('static', filename='demo-screen-1.jpg') +'"></br> <a href="'+ url_for("faster")+'"><h3> Faster Route:'+trip_time+'</h3> </a> </br> <a href="'+ url_for("greener")+'"><h3>Greener Route: '+trip_co2+' (gEC)</h3> </a>'


@app.route('/faster')
def faster():
    return render_template ('faster.html')
@app.route('/greener')
def greener():
    return render_template ('greener.html')
    
    

if __name__ == "__main__":
    app.run(debug=True,host='localhost', port= 8000)


