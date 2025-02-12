import os
import sys
import django 
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skypot.settings")
django.setup()

from django.conf import settings
from pot.models import Database, Credentials
from scripts.geolocation import get_batch_geolocation

log_file = os.path.join(settings.BASE_DIR, "..", "cowrie.json.2022-11-15")

def parse_log_and_store_data(log_file_path):
    
    ip_map={}
    new_ips=set()
    credentials_list=[]
    
    existing_ips = set(Database.objects.values_list('src_ip', flat=True))

    with open(log_file_path, 'r',encoding="utf-8") as file:
        for line in file:
            try:
                log_data = json.loads(line)  
                src_ip = log_data.get('src_ip')
                username = log_data.get('username')
                password = log_data.get('password')

                if not src_ip:
                    continue  
                if src_ip not in existing_ips:
                    new_ips.add(src_ip)
                if username and password:
                    credentials_list.append({
                        "src_ip":src_ip,
                        "username": username,
                        "password": password,
                    })

            except json.JSONDecodeError:
                continue
    
    new_entries=[]
    if new_ips:
        geo_data_dict = get_batch_geolocation(list(new_ips))

        new_entries = [
            Database(
                src_ip=ip,
                lat=geo_data.get('lat',''),
                lon=geo_data.get('lon',''),
                country=geo_data.get('country', ''),
                region=geo_data.get('region', '')
            )
            for ip , geo_data in geo_data_dict.items() if geo_data
        ]
            
        Database.objects.bulk_create(new_entries)

        ip_map.update(Database.objects.in_bulk(new_ips, field_name="src_ip"))
        
    credentials_objects=[]
    if credentials_list:
        credentials_objects = [
            Credentials(
                ip=ip_map.get(entry["src_ip"]) or Database.objects.filter(src_ip=entry["src_ip"]).first(),
                username = entry["username"],
                password=entry["password"],
            )
            for entry in credentials_list
        ]
        if credentials_objects:
            Credentials.objects.bulk_create(credentials_objects)
    
    print(f"Inserted {len(new_entries)} new IPS and {len(credentials_objects)} credentials. ")

if __name__ ==  "__main__":
    parse_log_and_store_data(log_file)