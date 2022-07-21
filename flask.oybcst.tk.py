from flask import Flask, render_template
from folium.plugins import MarkerCluster
import folium
import pandas as pd

app = Flask(__name__)
app.config['TESTING'] = True
app.testing = True

@app.route("/")
def hello():
    #return "<h1 style='color:red'>Hello There!</h1>"
    station_file = "RESTORE-Station-List-2020.csv"
    station_data = pd.read_csv(station_file)
    locations = station_data[['Lat', 'Lon']]
    locationlist = locations.values.tolist()
    Colors = ["white"]*len(locationlist)
    Icons = [""]*len(locationlist)
    for point in range(0, len(locationlist)):
        if station_data["Water Station 2020 Restore"][point] == 'x':
            Colors[point]=("blue")
        elif type(station_data["Fishery Station Names"][point]) != float:
            Colors[point]=("lightgreen")
        if type(station_data["Site Landmarks"][point]) != float:
            Icons[point]=("institution")
        if station_data["Water Station 2020 Restore"][point] == 'x' and type(station_data["Fishery Station Names"][point]) != float:
            Colors[point]=("darkgreen")
    water = station_data['Water Station 2020 Restore'].fillna("")
    fish = station_data["Fishery Station Names"].fillna("")
    Landmarks = station_data["Site Landmarks"].fillna("")
    m = folium.Map(location=[30.50355, -87.98733], zoom_start=10)
#    marker_cluster = MarkerCluster().add_to(m)
    folium.TileLayer('openstreetmap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    station_group = folium.FeatureGroup(name="Stations")
    for point in range(0, len(locationlist)):
        station_group.add_child(folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))
    m.add_child(station_group)
    folium.LayerControl().add_to(m)

#    for point in range(0, len(locationlist)):
#        folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')).add_to(m)
#    for point in range(0, len(locationlist)):
#        info = station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point] + ",icon=folium.Icon(color=" + Colors[point] + r",icon_color='red', icon=" + Icons[point] +", angle=0, prefix='fa')"
#        folium.RegularPolygonMarker(locationlist[point], popup=info).add_to(marker_cluster)

    m.save('templates/map.html')
    return render_template('index.html') 

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
