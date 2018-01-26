from elasticsearch import Elasticsearch
import time, json, simplejson, urllib, random



# The id min-max for spain is: 39960000 - 40001797
RangeMin = 39960000
RangeMax = 40001797

#URL wallapop
url = 'http://pro2.wallapop.com/shnm-portlet/api/v1/user.json/'

#Proxies
proxies = {
    'http': 'socks5://127.0.0.1:9150',
    'https': 'socks5://127.0.0.1:9150'
}

#Elasticsearch
elastic_host = "localhost"
elastic_port = 9200



if __name__ == "__main__":

    # Start elastic_host
    es = Elasticsearch()
    profile = {
        "mappings": {
            "wallapop": {
                "properties": {
                    "date": {
                        "type": "date",
                        "format": "epoch_second"
                    },
                    "geopoint": {
                        "type": "geo_point",
                    },
                }
            },
        }
    }

    es.indices.create(index="wallapop", ignore=400, body=profile)
    elastic = Elasticsearch([{'host': elastic_host, 'port': elastic_port}])


    # Start Scraper
    for uid in range(RangeMin, RangeMax):
        try:
            request = (urllib.request.urlopen(url + str(uid) + "?").read()).decode('utf-8')
            jsonitem = json.loads(request)

            try:
                Lat = jsonitem['location']['approximatedLatitude']
                Lon = jsonitem['location']['approximatedLongitude']
                jsonitem['geopoint'] = str(str(Lat)+','+str(Lon))
            except:
                pass

            jsonitem['date'] = int(time.time())
            elastic.index(index='wallapop', doc_type='doc', body=simplejson.dumps(jsonitem))
            print(request)

        except:
            print(str(uid) + " does not exist")

        time.sleep(random.randint(0, 1))





