import os
import sys
import django 
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skypot.settings")
django.setup()

from django.conf import settings
from pot.models import Database
from scripts.geolocation import get_batch_geolocation

log_file = os.path.join(settings.BASE_DIR, "..", "cowrie.json.2022-11-15")

def parse_log_and_store_data(log_file_path):
    log_entries = [] 
    ip_set = set() 

    existing_ips = set(Database.objects.values_list('src_ip', flat=True))

    with open(log_file_path, 'r') as file:
        for line in file:
            try:
                log_data = json.loads(line)  
                src_ip = log_data.get('src_ip')

                if not src_ip or src_ip in existing_ips or src_ip in ip_set:
                    continue  

                log_entries.append({'src_ip': src_ip})
                ip_set.add(src_ip) 

            except json.JSONDecodeError as e:
                continue

    if not log_entries:
        print("No new unique IPs to process.")
        return

    geo_data_dict = get_batch_geolocation(list(ip_set))

    new_entries = []
    for entry in log_entries:
        geo_data = geo_data_dict.get(entry['src_ip'], {})
        new_entries.append(Database(
            src_ip=entry['src_ip'],
            lat=geo_data.get('lat'),
            lon=geo_data.get('lon'),
            country=geo_data.get('country'),
            region=geo_data.get('region')
        ))

    Database.objects.bulk_create(new_entries) 
    print(f"Inserted {len(new_entries)} new unique records.")

if __name__ ==  "__main__":
    parse_log_and_store_data(log_file)