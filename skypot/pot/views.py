from django.shortcuts import render



def pot_map(request):    
    map_path = "static/map.html"
    return render(request, "dashboard.html", {"static_map": map_path})
    