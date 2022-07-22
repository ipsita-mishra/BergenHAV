  
import folium
import re

def allPlotter(megaDataList, k):
    pl = megaDataList[0]
    storel = megaDataList[1]
    stopl = megaDataList[2]
    metres = k * 1000
    my_map = folium.Map(location = [60.3913, 5.3221], zoom_start = 12, min_zoom=12 )
    for m in range(len(pl)):
        area = (str(pl[m][0]).rsplit(",",1))[1]
        street = (str(pl[m][0]).rsplit(",",1))[0]
        addr = re.sub(r'[^A-Za-z0-9 -]+', '', street) + " " + area
        if "leilighet" in pl[m][1]:
            property_color = "darkpurple"
        elif "rekkehus" in pl[m][1]:
            property_color = "pink"
        elif "enebolig" in pl[m][1]:
            property_color = "orange"
        else:
            property_color = "blue"

        house_marker = folium.Marker([pl[m][-2], pl[m][-1]],icon= folium.Icon(color=property_color,icon="home"),tooltip = "Property", popup = "<div style=\"width:200px;\"><h4>Address : "+ addr +"</h4><h5>Type : "+pl[m][1]+"</h5><h5>New or Planned Property : "+pl[m][3]+"</h5><h5>URL : <a href=" +pl[m][2]+ "> Link to advertisement</a></h5></div>")
        house_marker.add_to(my_map)
        circle_marker = folium.Circle([pl[m][-2], pl[m][-1]],radius = metres, color="cyan", fill="true", fill_opacity=0.05)
        circle_marker.add_to(my_map)
    for n in range(len(storel)):
        store_marker = folium.Marker([storel[n][-2], storel[n][-1]],icon= folium.Icon(color="lightred", icon="shopping-basket", prefix="fa"),tooltip = "Grocery Store",popup = "<div style=\"width:200px;\"><h4> Name : "+storel[n][0]+"</h4></div>")
        store_marker.add_to(my_map)
    for o in range(len(stopl)):
        stop_marker = folium.Marker([stopl[o][-2], stopl[o][-1]],icon= folium.Icon(color="green", icon="bus", prefix="fa"),tooltip = "Transport", popup = "<div style=\"width:200px;\"><h4> Name : "+stopl[o][0]+"</h4><h5>Services : "+stopl[o][1]+", "+stopl[o][2]+"</h5></div>")
        stop_marker.add_to(my_map)
    my_map.save("docs/index.html")  