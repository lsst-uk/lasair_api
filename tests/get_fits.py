import json, sys
from lasair import lasair_client
import settings

objectIds = ['ZTF22aafnqfz']

L = lasair_client(settings.API_TOKEN, endpoint='https://lasair-ztf.lsst.ac.uk/api')

for objectId in objectIds:
    print(objectId)
    lcs = L.objects([objectId])
    print(json.dumps(lcs, indent=2))
