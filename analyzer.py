import database as da
from geopy.distance import distance

def getPropertyCoordinates():
    sql = ''' select address, type, link, new_prop, latitude, longitude from property_info '''
    prop_set = set()
    conn = da.dbconnect()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        prop_set.add(row)
    da.dbdisconnect(conn)
    return list(prop_set)

def getStoreCoordinates():
    sql = ''' select store_name, latitude, longitude from store_info '''
    store_set = set()
    conn = da.dbconnect()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        store_set.add(row)
    da.dbdisconnect(conn)
    return list(store_set)

def getStopCoordinates():
    sql = ''' select stop_name, service1, service2, latitude, longitude from stop_info '''
    stop_set = set()
    conn = da.dbconnect()
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        stop_set.add(row)
    da.dbdisconnect(conn)
    return list(stop_set)


def measure(pco,storeco,stopco, kms):
    prepco = set()
    prestoreco = set()
    prestopco = set()
    megalist = []
    for p in pco:
        pll = (p[-2],p[-1])
        for store in storeco:
            storell = (store[-2],store[-1])
            if (distance(pll,storell).km) <= kms:
                prepco.add(p)
                prestoreco.add(store)  
    for q in pco:
        qll = (q[-2],q[-1])
        for stop in stopco:
            stopll = (stop[-2],stop[-1])
            if (distance(qll,stopll).km) <= kms:
                prepco.add(q)
                prestopco.add(stop) 

    megalist.append(list(prepco))
    megalist.append(list(prestoreco))
    megalist.append(list(prestopco)) 
    return megalist
