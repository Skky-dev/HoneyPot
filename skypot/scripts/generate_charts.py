import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skypot.settings")
django.setup()

import plotly.express as px
from django.conf import settings
from django.db.models import Count, Sum
from pot.models import Database, Credentials

STATIC_GRAPH_PATH = os.path.join(settings.BASE_DIR, "static", "graphs")

def save_plotly_chart(fig, filename):
    filepath = os.path.join(STATIC_GRAPH_PATH, filename)
    fig.write_html(filepath, full_html=False, config={'displayModeBar': False})
    print(f"{filename} Saved")
    return f"/static/graphs/{filename}"

def create_attack_plot():
    country_data = list(Database.objects.values('country')
                        .annotate(attacks=Sum('hit_count'))
                        .order_by('-attacks')[:15])

    if not country_data:
        print("No Database Found")
        return

    fig = px.pie(
        names=[d['country'] for d in country_data],
        values=[d['attacks'] for d in country_data],
        title='Top 15 Attacking Countries',
        template='plotly_dark',
        hole=.7,
    )
    return save_plotly_chart(fig, "attack_plot.html")

def create_credentials_plot():
    cred_data = list(Credentials.objects.values('username')
                     .annotate(attempts=Count('id'))
                     .order_by('-attempts')[:10])

    if not cred_data:
        print("No Credential Data Found")
        return

    fig = px.pie(
        names=[d['username'] for d in cred_data],
        values=[d['attempts'] for d in cred_data],
        title='Most Common Usernames',
        template='plotly_dark',
        hole=.7,
    )
    return save_plotly_chart(fig, "cred_plot.html")

def generate_all_charts():
    create_attack_plot()
    create_credentials_plot()

if __name__ == "__main__":
    generate_all_charts()
