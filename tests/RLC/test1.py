import sys
import json
sys.path.insert(0, '../..')
from lasair import RL_consumer

topic = 'lasair_2NEEDLESLSNroycandidates'
rc = RL_consumer.lasair_RL_consumer(
    'kafka.lsst.ac.uk',
    'LASAIR9',
    topic,
    './%s.sql' % topic,
    interval=1,
    verbose=True
)

while 1:
    msg = rc.poll()
    if msg is None:
        break;
    objectId = json.loads(msg.value())['objectId']
    print('---> object %s found at %s' % (objectId, RL_consumer.now_human()))
#rc.printall()

