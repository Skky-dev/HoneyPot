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
from django.db.models import F

log_file = os.path.join(settings.BASE_DIR, "..", "cowrie.json.2022-11-15")

def parse_log_and_store_data(log_file_path):
    
    ip_map={}
    new_ips=set()
    credentials_list=[]
    hit_count_updates={}

    existing_ips = set(Database.objects.values_list('src_ip', flat=True))
    existing_credentials = set(Credentials.objects.values_list('username', 'password'))

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
                else:
                    hit_count_updates[src_ip] = hit_count_updates.get(src_ip, 0) + 1
                if username and password:
                    credentials_list.append({
                        "src_ip":src_ip,
                        "username": username,
                        "password": password,
                    })

            except json.JSONDecodeError:
                continue
    for ip, count in hit_count_updates.items():
        Database.objects.filter(src_ip=ip).update(hit_count=F("hit_count") + count)
    
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

        ip_map.update({entry.src_ip: entry for entry in Database.objects.filter(src_ip__in=new_ips)})

    new_cred_count = 0
    updated_cred_count=0
    credentials_objects = []
    if credentials_list:
        for entry in credentials_list:
            ip_obj = ip_map.get(entry["src_ip"]) or Database.objects.filter(src_ip=entry["src_ip"]).first()
            if not ip_obj:
                continue 

            credentials_obj, created = Credentials.objects.get_or_create(
                ip=ip_obj,
                username=entry["username"],
                password=entry["password"],
                defaults={"frequency": 1}
            )

            if created:
                new_cred_count += 1
            else:
                updated_cred_count += 1
                credentials_obj.frequency = F("frequency") + 1
                credentials_obj.save(update_fields=["frequency"])

            credentials_objects.append(credentials_obj)    
    
    print(f"Inserted {len(new_entries)} new IPs.")
    print(f"Inserted {new_cred_count} new credentials.")
    print(f"Updated {updated_cred_count} existing credentials.")

if __name__ ==  "__main__":
    parse_log_and_store_data(log_file)