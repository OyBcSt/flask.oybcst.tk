""" app.py
    Start the flask server by running:
        $ python app.py
    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask

import folium

app = Flask(__name__)


@app.route('/')

def index():
    import pandas as pd
    station_file = "CastFile_0322-OB20220317.csv"
    station_data = pd.read_csv(station_file)
    locations = station_data[['Lat', 'Lon']]
    locationlist = locations.values.tolist()
    import branca
    import branca.colormap as cm
    colormap = cm.LinearColormap(colors=['darkred','red','orange','yellow','green','darkblue','purple'], index=[1,2,3,4,5,6,20],vmin=1,vmax=20)
    m = folium.Map(location=[30.50355, -87.98733], zoom_start=9)
    for point in range(0, len(locationlist)):
        folium.Marker(locationlist[point], popup=station_data['Station'][point] + "\n" + station_data['Date'][point] + "\n" + station_data['Time'][point],icon=folium.Icon(color="white",icon_color=colormap(station_data['Depth (m)'][point]), icon='tint', angle=0, prefix='fa')).add_to(m)
#ogr2ogr -t_srs EPSG:4326 -f GeoJSON subs1.json subs1.shp
#https://shallowsky.com/blog/mapping/folium-with-shapefiles.html
    folium.GeoJson("subs1.json").add_to(m)
    folium.LayerControl().add_to(m)
    m.add_child(colormap)

    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)
