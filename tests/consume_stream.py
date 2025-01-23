"""
Copyright 2022 Roy Williams

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
-------------
   Consumes a stream from Lasair kafka.
   The stream corresponds to a Lasair query that has the checkbox where it says
   "Convert to Filter and produce Kafka and log".
   There will then be a log file like
   https://lasair-ztf.lsst.ac.uk/streams/lasair_2crossmatchCVcatalogue/
"""
import json, sys
import lasair
import settings, time
from datetime import datetime
from random import randrange
import mag

def get_alert(consumer, L, alert_handler):
    msg = consumer.poll(timeout=20)
    if msg is None:
        return False
    if msg.error():
        print(str(msg.error()))
        return False
    jmsg = json.loads(msg.value())

    # The only thing we want from the message is the objectId
    objectId = jmsg['objectId']
    alert_handler(L, objectId)

    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_string, objectId)
    return True

def get_dc_lightcurve(L, objectId):
    # Fetch the lightcurve and convert to dc magnitudes
    lc = L.lightcurves([objectId])[0]

    # just keep detections, forget non-detections
    lc_detections = [c for c in lc if 'candid' in c]

    for lcd in lc_detections:
        dc = mag.dc_mag_dict(
            lcd['fid'], 
            lcd['magpsf'],
            lcd['sigmapsf'], 
            lcd['magnr'],
            lcd['sigmagnr'], 
            lcd['magzpsci'], 
            lcd['isdiffpos']
        )
        print('%10.2f %d %6.2f %6.2f' % (lcd['jd']-2459000, lcd['fid'], dc['dc_mag'], dc['dc_sigmag']))

    # remove this for actual operation
    # time.sleep(3)

def fetch_em(consumer, L, alert_handler, nalert=20):
    if nalert == -1:
        while 1:
            get_alert(consumer, L, alert_handler)
    elif nalert > 0:
        for ialert in range(20):
            get_alert(consumer, L, alert_handler)

####################################
# See "Get your Token"
# in https://lasair-ztf.lsst.ac.uk/api
token = settings.API_TOKEN
L = lasair.lasair_client(token)

# For actual operation, use a FIXED group_id!
# server remembers which alerts you have already seen
# use group_id = 'CVS001' for daemon
if len(sys.argv) > 1:
    group_id = sys.argv[1]
else:
    # A random group_id starts from the beginning every time.
    group_id = 'test{}'.format(randrange(1000))
print('Using group_id', group_id)

# This query https://lasair-ztf.lsst.ac.uk/query/365/
# matches ZTF alerts with the Downes catalog of CVs
# https://lasair-ztf.lsst.ac.uk/watchlist/26/
topic_in = 'lasair_2crossmatchCVcatalogue'

# Connect to the Lasair kafka service
consumer = lasair.lasair_consumer('kafka.lsst.ac.uk:9092', group_id, topic_in)

# Get the alerts
fetch_em(consumer, L, get_dc_lightcurve)
