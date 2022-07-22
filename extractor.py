import database as da
import json, requests, logging
from bs4 import BeautifulSoup as bs


def addStoretoDB(*storechain):
    stores = []
    for s in range(len(storechain)):
        for x in storechain[s]:
            stores.append(x)
    conn = da.dbconnect()
    cursor = conn.cursor()
    sql = ''' INSERT INTO store_info(store_name,street_address,pincode,city, latitude, longitude ) VALUES(?,?,?,?,?,?) '''
    for item in stores:
        cursor.execute(sql, item)
    da.dbdisconnect(conn)

def addStoptoDB(stoplist):
    conn = da.dbconnect()
    cursor = conn.cursor()
    sql = ''' INSERT INTO stop_info(stop_id,stop_name,service1,service2,city, latitude, longitude ) VALUES(?,?,?,?,?,?,?) '''
    for item in stoplist:
        cursor.execute(sql, item)
    da.dbdisconnect(conn)

def addProptoDB(*proplist):
    props = []
    for s in range(len(proplist)):
        for x in proplist[s]:
            props.append(x)
    conn = da.dbconnect()
    cursor = conn.cursor()
    sql = ''' INSERT INTO property_info (address, description, type, link, owner_type, city, latitude, longitude, new_prop) VALUES(?,?,?,?,?,?,?,?,?) '''
    for item in props:
        cursor.execute(sql, item)
    da.dbdisconnect(conn)

def updateExtracts():
    conn = da.dbconnect()
    cursor = conn.cursor()
    sql_stores = ''' DELETE FROM store_info;'''
    sql_stops = ''' DELETE FROM store_info;'''
    sql_props = ''' DELETE FROM property_info;'''
    cursor.execute(sql_stores)
    cursor.execute(sql_stops)
    cursor.execute(sql_props)
    da.dbdisconnect(conn)
    addStoretoDB(coopAddressExtractor(), jokerKiwiMenySparAddressExtractor(), bunprissAddressExtractor(), remaAddressExtractor())
    addStoptoDB(transportStopAddressExtractor())
    addProptoDB(finnNewPropertyExtractor())

def coopAddressExtractor():
    try:
        url = "https://coop.no/StoreService/SearchStores?searchInput=bergen&chainId=999"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.e("Error occurred in coopAddressExtractor")

    json_response = json.loads(response.text)
    store_details = json_response["Stores"]
    coop_loc = []
    for l in range(len(store_details)):
        if ((store_details[l])["City"]).lower() == "bergen":
            each_store_loc = ((store_details[l])["Address"]).lower()
            street_addr = each_store_loc.split(", ")[0]
            pincode = (each_store_loc.split(", ")[1]).replace("bergen", "")
            store_name = "COOP - "+((store_details[l])["Name"]).lower()
            city = "bergen"
            latitude = ((store_details[l])["Lat"])
            longitude = ((store_details[l])["Lng"])
            r = (store_name, street_addr, pincode, city, latitude, longitude)
            coop_loc.append(r)
    return coop_loc


def jokerKiwiMenySparAddressExtractor():
    try:
        url = "https://api.ngdata.no/sylinder/stores/v1/extended-info/"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.e("Error occurred in jokerKiwiMenySparAddressExtractor")
    json_response = json.loads(response.text)
    store_loc = []
    for x in range(len(json_response)):
        if "bergen" in (((json_response[x])["storeDetails"])["municipality"]).lower():
            street_addr = ((((json_response[x])["storeDetails"])["organization"])["address"]).lower()
            pincode = ((((json_response[x])["storeDetails"])["organization"])["postalCode"]).lower()
            store_name = "JKMS - "+(((json_response[x])["storeDetails"])["storeName"]).lower()
            city = "bergen"
            latitude = ((((json_response[x])["storeDetails"])["position"])["lat"])
            longitude = ((((json_response[x])["storeDetails"])["position"])["lng"])
            r = (store_name, street_addr, pincode, city, latitude, longitude)
            store_loc.append(r)
    return store_loc

def bunprissAddressExtractor():
    try:
        url = "https://bunnpris.no/alle-butikker"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.e("Error occurred in bunprissAddressExtractor")
    json_response = json.loads(response.text)
    bunn_loc = []
    for x in range(len(json_response)):
        if "bergen" in ((json_response[x])["town"]).lower():
            street_addr = ((json_response[x])["address"]).lower()
            pincode = ((json_response[x])["postal_code"]).lower()
            store_name = "BUNNPRISS - "+((json_response[x])["title"]).lower()
            city = "bergen"
            latitude = ((json_response[x])["latitude"])
            longitude = ((json_response[x])["longitude"])
            r = (store_name, street_addr, pincode, city, latitude, longitude)
            bunn_loc.append(r)
    return bunn_loc

def remaAddressExtractor():
    try:
        url =  "https://www.rema.no/butikker/vestland/bergen/"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.e("Error occurred in remaAddressExtractor")
    soup = bs(response.text, 'html.parser')
    rema_loc = []
    for store in soup.find_all('script'):
        if "storeFinderConfig" in store.text:
            block = str(store.text)
            start_index = block.find("stores:")
            end_index = block.find("counties:")
            data_str = (((block[start_index:end_index]).strip())[:-1])[8:]
            json_data = json.loads(data_str)
            for s in range(len(json_data)):
                if "bergen" in ((json_data[s])["municipalityName"]).lower():
                    street_addr = ((json_data[s])["visitAddress"]).lower()
                    pincode = ((json_data[s])["visitPostCode"]).lower()
                    store_name = "REMA - "+((json_data[s])["name"]).lower()
                    city = "bergen"
                    latitude = ((json_data[s])["latitude"])
                    longitude = ((json_data[s])["longitude"])
                    r = (store_name, street_addr, pincode, city, latitude, longitude)
                    rema_loc.append(r)
    return rema_loc
    

def transportStopAddressExtractor():
    try:
        url = "https://skyss-reise.giantleap.no/v3/stopgroups"
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.e("Error occurred in transportStopAddressExtractor")
    json_response = json.loads(response.text)
    stop_loc = []
    stops_data = json_response["StopGroups"]
    for x in range(len(stops_data)):
        if "bergen" in (stops_data[x]["Municipality"]).lower():
            city = (stops_data[x]["Municipality"]).lower()
            stop_id = (stops_data[x]["Identifier"]).lower()
            stop_name = (stops_data[x]["Description"]).lower()
            service1 = (stops_data[x]["ServiceModes"][0]).lower()
            service2 = (stops_data[x]["ServiceModes2"][0]).lower()
            latitude = ((stops_data[x]["Location"]).split(","))[0]
            longitude =((stops_data[x]["Location"]).split(","))[1]
            r = (stop_id, stop_name, service1, service2, city, latitude, longitude )
            stop_loc.append(r)
    return stop_loc

            
def finnNewPropertyExtractor():

    prop_loc = []

    prop_search_keys = ["SEARCH_ID_REALESTATE_NEWBUILDINGS","SEARCH_ID_REALESTATE_HOMES"]
    for key in prop_search_keys:
        for page in range(20):
            try:
                u = "https://www.finn.no/api/search-qf?searchkey="+key+"&page="+str(page)+"&sort=PUBLISHED_DESC&location=1.22046.20220&vertical=realestate"

                response = requests.get(u)
            except requests.exceptions.RequestException as e:
                logging.e("Error occurred in finnNewPropertyExtractor")
            if response.status_code == 200:
                json_response = json.loads(response.text)

                for p in json_response["docs"]:
                    address = (p["location"]).lower()
                    description = (p["heading"]).lower()
                    property_type = (p["property_type_description"]).lower()
                    link = (p["ad_link"]).lower()
                    owner_type = (p["owner_type_description"]).lower()
                    city = "bergen"
                    latitude = (p["coordinates"]["lat"])
                    longitude = (p["coordinates"]["lon"])
                    if prop_search_keys[0] in u:
                        new_prop = "yes"
                    else:
                        new_prop = "no"
                    r = (address, description, property_type, link, owner_type, city, latitude, longitude, new_prop)
                    prop_loc.append(r)
    return prop_loc
