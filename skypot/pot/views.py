from .models import Credentials, Database
from django.shortcuts import render
from django.db.models import Sum

def pot_map(request):
    static_map_path = "/static/map.html"
    attack_plot_path = '/static/graphs/attack_plot.html'
    cred_plot_path = '/static/graphs/cred_plot.html'

    
    top_attackers = Database.objects.order_by('-hit_count')[:10]

    top_credentials = (
        Credentials.objects
        .values('username', 'password')
        .annotate(frequency=Sum('frequency')) 
        .order_by('-frequency')[:10]  
    )
    
    context = {
        "top_attackers": top_attackers,
        "top_credentials":top_credentials,
        "static_map": static_map_path,
        "attack_plot": attack_plot_path,
        "cred_plot": cred_plot_path
    }

    return render(request, "dashboard.html", context)
