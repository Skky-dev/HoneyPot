import os
import sys
import math
import folium
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skypot.settings")
django.setup()

from pot.models import Database
from django.conf import settings

def generate_attack_map():
    
    map = folium.Map(location=[20.5937, 78.9629], zoom_start=3, tiles=None)

    folium.TileLayer('CartoDB dark_matter', name='Dark Map', control=True).add_to(map)
    folium.TileLayer('CartoDB positron', name="Light Map", control=True).add_to(map)

    ip_data = Database.objects.values("lat", "lon", "country", "region", "hit_count", "src_ip")

    if not ip_data:
        print("No Data in Database")
        return

    low_attacks = folium.FeatureGroup(name='Low Activity (1-20 hits)', show=True)
    medium_attacks = folium.FeatureGroup(name='Medium Activity (21-100 hits)', show=True)
    high_attacks = folium.FeatureGroup(name='High Activity (101+ hits)', show=True)

    for data in ip_data:
        hit_count = data['hit_count']
        radius = min(math.sqrt(hit_count) * 4, 35)

        if hit_count <= 20:
            color, feature_group = "green", low_attacks
        elif hit_count <= 100:
            color, feature_group = "orange", medium_attacks
        else:
            color, feature_group = "red", high_attacks

        tooltip = f"""
        <div>
            <b style="color: blue;">IP:</b> {data['src_ip']}<br>
            <b style="color: limegreen;">Country:</b> {data['country']}<br>
            <b>Region:</b> {data['region']}<br>
            <b style="color: red;">Attack Attempts:</b> {hit_count}<br>    
        </div>
        """

        folium.CircleMarker(
            location=[float(data["lat"]), float(data["lon"])],
            radius=radius,
            color=color,
            stroke=True,
            fill=True,
            fill_opacity=0.7,
            opacity=0.8,
            popup=folium.Popup(tooltip, max_width=300),
            tooltip=f"Click for details - {data['country']}"
        ).add_to(feature_group)

    low_attacks.add_to(map)
    medium_attacks.add_to(map)
    high_attacks.add_to(map)
    folium.LayerControl().add_to(map)

    # Defualt Dark Map through JavaScript
    map.get_root().html.add_child(folium.Element("""
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            document.querySelectorAll('.leaflet-control-layers-base input')[0].click();
        });
    </script>
    """))
    
    map_path = os.path.join(settings.BASE_DIR, "static", "map.html")
    map.save(map_path)
    print("Attach Map Generated")

if __name__ == "__main__":
    try:
        generate_attack_map()
    except Exception as e:
        print(f"Error Generating Map: {e}")