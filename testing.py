from flask import Flask, render_template
from folium.plugins import MarkerCluster
import folium
import pandas as pd
import branca

app = Flask(__name__)
app.config['TESTING'] = True
app.testing = True

@app.route("/")
def hello():

# Initialize map
    m = folium.Map(location=[30.50355, -87.98733], zoom_start=10)

#ReadData and Define vars
    station_file = "RESTORE-Station-List-2020.csv"
    station_data = pd.read_csv(station_file)
    water_group = folium.FeatureGroup(name="Water Stations")
    fish_group = folium.FeatureGroup(name="Fisheries Stations")
    both_group = folium.FeatureGroup(name="Water and Fisheries Stations")
    none_group = folium.FeatureGroup(name="Stations",show=False)

#popup = folium.Popup(iframe, max_width=2650)

# locations and colors
    locations = station_data[['Lat', 'Lon']]
    locationlist = locations.values.tolist()
    Colors = ["white"]*len(locationlist)
    Icons = [""]*len(locationlist)
    for point in range(0, len(locationlist)):
        if station_data["Water Station 2020 Restore"][point] == 'x':
            Colors[point]=("blue")
        elif type(station_data["Fishery Station Names"][point]) != float:
            Colors[point]=("lightgreen")
        else:
            Colors[point]=("white")
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
    for point in range(0, len(locationlist)):
        html="Station" + station_data['StationName'][point]+"/n"
        iframe = branca.element.IFrame(html=html, width=200, height=80)

        if Colors[point] == "blue": 
            water_group.add_child(folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))
        elif Colors[point] == "lightgreen":
            fish_group.add_child(folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))
#        elif Colors[point] == "darkgreen":
#            both_group.add_child(folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))
        elif Colors[point] == "darkgreen":
            both_group.add_child(folium.Marker(locationlist[point], popup=folium.Popup(iframe,max_width=1000),icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))
        else: 
            none_group.add_child(folium.Marker(locationlist[point], popup=station_data['StationName'][point] + "\n" + fish[point] + "\n" + Landmarks[point],icon=folium.Icon(color=Colors[point],icon_color="red", icon=Icons[point], angle=0, prefix='fa')))

    m.add_child(water_group)
    m.add_child(fish_group)
    m.add_child(both_group)
    m.add_child(none_group)
    folium.LayerControl().add_to(m)


    m.save('templates/map.html')
    return render_template('index.html') 

@app.route('/map')
def map():
    return render_template('map.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
