import os
import json
import requests
import folium
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def pot_map(request):
    map = folium.Map(location=[20.5937, 78.9629], tiles="Cartodb dark_matter", zoom_start=3)

    ip_list= []
    log_file = os.path.join(settings.BASE_DIR,".." ,'cowrie.json.2022-11-15')

    if not os.path.exists(log_file):
        return HttpResponse("Log File Path is incorrect")

    try:
        with  open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    ip_list.append(data["src_ip"])
                except (json.JSONDecodeError, KeyError):
                    continue
    except FileNotFoundError:
        return HttpResponse("Log File Not Found")

    ip_list = list(set(ip_list))
    flag= True
    batch_size = 100
    for i in range(0, len(ip_list), batch_size):
        batch = ip_list[i : i + batch_size]

        response = requests.post("http://ip-api.com/batch", json=batch)

        if response.status_code == 200:
            results = response.json()
            for res in results:
                if res["status"] == "success":
                    folium.CircleMarker(
                        location=[res["lat"], res["lon"]],
                        radius=25,
                        color="green",
                        stroke=True,
                        fill=True,
                        fill_opacity=0.5,
                        opacity=0.7,
                        tooltip=f"Country:<b>{res['country']} </b><br>Region:<b>{res['regionName']}</b>",
                    ).add_to(map)
        else:
            return HttpResponse("Rate limit reached or error occurred")
            
    
    map_path = 'static/map.html'
    map.save(map_path)
    return render(request, "dashboard.html", {"static_map": map_path})