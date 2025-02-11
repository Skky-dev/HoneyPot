import folium
from django.shortcuts import render
from django.http import HttpResponse
from .models import Database


def pot_map(request):
    map = folium.Map(location=[20.5937, 78.9629], tiles="Cartodb dark_matter", zoom_start=3)

    ip_data = Database.objects.values("lat","lon","country","region")

    if not ip_data:
        return HttpResponse("No Geolocation Data Available | Error Occured")
    
    for data in ip_data:
        folium.CircleMarker(
            location=[data["lat"],data["lon"]],
            radius=20,
            color="green",
            stroke=True,
            fill=True,
            fill_opacity=0.5,
            opacity=0.7,
            tooltip=f"Country: <b>{data['country']}</b><br>Region: <b>{data['region']}</b>",
        ).add_to(map)

    map_path="static/map.html"
    map.save(map_path)

    return render(request, "dashboard.html", {"static_map":map_path})
    