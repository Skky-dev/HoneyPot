import requests
import time

BATCH_SIZE=100
API_URL = "http://ip-api.com/batch"

def get_batch_geolocation(ip_list):
    geo_data_dict={}

    for i in range(0, len(ip_list), BATCH_SIZE):
        batch = ip_list[i : i + BATCH_SIZE]
        for attempt in range(3):    
            try:
                
                response=requests.post(API_URL,json=batch)
                if response.status_code == 200:
                    
                    data_list=response.json()
                    
                    for data in data_list:
                        if data.get("status") == 'fail':
                            continue

                        ip = data.get("query")
                        if ip:
                            geo_data_dict[ip]={
                                'lat':data.get('lat'),
                                'lon':data.get('lon'),
                                'country':data.get('country'),
                                'region':data.get('regionName'),
                            }
                    break
                else:
                    print(f"API return status code {response.status_code}, retrying {attempt + 1} time")
                    time.sleep(3)        
            except requests.RequestException as e:
                print(f"Error fetching geolocation: {e}")
                time.sleep(3)
        time.sleep(1)    
            
    return geo_data_dict      