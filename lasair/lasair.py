""" Lasair API

This class enables programmatic access to the Lasair database and Sherlock service, 
as described at http://lasair-iris.roe.ac.uk/api/.

Args:
    token (string): The Calls are throttled by the lasair server, by use of an 
    'authorization token', as described in the api documentation above. 
    There is a free token listed there, but it is throttled at 10 calls per hour. 
    Once a user has an account at the Lasair webserver, they can get their own token
    allowing 100 calls per hour, or request to be a power user, with infinite usage.

    cache (string): Results can be cached on a local filesystem, by providing 
    the name of a writable directory. If the same calls are made repeatedly, 
    this will be much more efficient.
"""
import os, sys
import requests
import json
import hashlib

class LasairError(Exception):
    def __init__(self, message):
        self.message = message

class lasair_client():
    def __init__(self, token, cache=None):
        self.headers = { 'Authorization': 'Token %s' % token }
        self.server = 'https://lasair-iris.roe.ac.uk/api'
        self.cache = cache
        self.kafka_producer = None
        if cache and not os.path.isdir(cache):
            message = 'Cache directory "%s" does not exist' % cache
            raise LasairError(message)

    def fetch_from_server(self, method, input):
        url = '%s/%s/' % (self.server, method)
        r = requests.post(url, data=input, headers=self.headers)
        if r.status_code == 200:
            try:
                result = r.json()
            except:
                result = {'error': 'Cannot parse Json'}
        elif r.status_code == 400:
            message = 'Bad Request:' + r.text
            raise LasairError(message)
        elif r.status_code == 401:
            message = 'Unauthorized'
            raise LasairError(message)
        elif r.status_code == 429:
            message = 'Request limit exceeded. Either wait an hour, or see API documentation to increase your limits.'
            raise LasairError(message)
        elif r.status_code == 500:
            message = 'Internal Server Error' + r.text
            raise LasairError(message)
        else:
            message = 'HTTP return code %d' % r.status_code
            raise LasairError(message)
        return result

    def hash_it(self, input):
        s = json.dumps(input)
        h = hashlib.md5(s.encode())
        return h.hexdigest()

    def fetch(self, method, input):
        if self.cache:
            cached_file = '%s/%s.json' % (self.cache, self.hash_it(method +'/'+ str(input)))
            try:
                result_txt = open(cached_file).read()
                result = json.loads(result_txt)
                return result
            except:
                pass

        result = self.fetch_from_server(method, input)

        if 'error' in result:
            return result

        if self.cache:
            f = open(cached_file, 'w')
            result_txt = json.dumps(result, indent=2)
            f.write(result_txt)
            f.close()

        return result

    def cone(self, ra, dec, radius=5, requestType='all'):
        """ Run a cone search on the Lasair database.
        Args:
            ra (float): Right Ascension in decimal degrees
            dec (float): Declination in decimal degrees
            radius (float): cone radius in arcseconds (default is 5)
            requestType: Can be 'all' to return all objects in the cone
                Can be 'nearest', only the nearest object within the cone
                Can be 'count', the number of objects within the cone

        Returns a dictionary with:
            objectId: The ID of the nearest object
            separation: the separation in arcseconds
        """
        input = {'ra':ra, 'dec':dec, 'radius':radius, 'requestType':requestType}
        result = self.fetch('cone', input)
        return result

    def query(self, selected, tables, conditions, limit=1000, offset=0):
        """ Run a database query on the Lasair server.
        args: 
            selected (string): The attributes to be returned by the query
            tables (string): Comma-separated list of tables to be joined
            conditions (string): the "WHERE" criteria to restrict what is returned
            limit: (int) (default 1000) the maximum number of records to return
            offset: (int) (default 0) offset of record number
        return:
            a list of dictionaries, each representing a row
        """
        
        input = {'selected':selected, 'tables':tables, 'conditions':conditions, 
            'limit':limit, 'offset':offset}
        result = self.fetch('query', input)
        return result

    def streams_topics(self, regex='.*', limit=1000):
        """ Get a list of available streams that match a given expression.
        args:
            regex (string, default .*): Search for stream names that match a pattern
            limit: (int, default 1000): Maximum number of stream names to return.
        return:
            List of stream names
        """
        input = {'regex':regex, 'limit':limit}
        result = self.fetch('streams', input)
        return result

    def streams(self, topic, limit=1000):
        """ Get records from a given stream
        args:
            topic (string): Name of stream to be returned.
        return:
            list of dictionaries, each representing a row
        """
        input = {'limit':limit}
        result = self.fetch('streams/%s/'%topic, input)
        return result

    def objects(self, objectIds):
        """ Get object pages in machine-readable form
        args:
            objectIds: list of objectIds, maximum 10
        return:
            list of dictionaries, each being all the information presented
            on the Lasair object page.
        """
        input = {'objectIds':','.join(objectIds)}
        result = self.fetch('objects', input)
        return result

    def lightcurves(self, objectIds):
        """ Get simple lightcurves in machine-readable form
        args:
            objectIds: list of objectIds, maximum 10
        return:
            list of dictionaries, one for each objectId. Each of these
            is a list of dictionaries, each having attributes
            candid, fid, magpsf, sigmapsf, isdiffpos, mjd
        """
        input = {'objectIds':','.join(objectIds)}
        result = self.fetch('lightcurves', input)
        return result

    def sherlock_objects(self, objectIds, lite=True):
        """ Query the Sherlock database for context information about objects
            in the database.
        args:
            objectsIds: list of objectIds, maximum 10
            lite (boolean): If true, get extended information including a 
                list of possible crossmatches.
        return:
            list of dictionaries, one for each objectId.
        """
        input = {'objectIds':','.join(objectIds), 'lite':lite}
        result = self.fetch('sherlock/objects', input)
        return result

    def sherlock_position(self, ra, dec, lite=True):
        """ Query the Sherlock database for context information about a position
            in the sky.
        args:
            ra (float): Right Ascension in decimal degrees
            dec (float): Declination in decimal degrees
            lite (boolean): If true, get extended information including a 
                list of possible crossmatches.
        return:
            dictionary of contect information
        """
        input = {'ra':ra, 'dec':dec, 'lite':lite}
        result = self.fetch('sherlock/position', input)
        return result

    try:
        from confluent_kafka import Consumer, Producer
        imported_kafka = True
    except ImportError:
        imported_kafka = False
 
    def stream_consumer(self, group_id, topic_in):
        """ Consume a Kafka stream from Lasair
        args:
            group_id: a string. If used before, the server will start from last message
            topic_in: The topic to be consumed. Example 'lasair_2SN-likecandidates'
        Will fail if for some reason the confluent_kafka library cannot be imported.
        Connects to Lasair public kafka to get the chosen topic.
        Once you have the returned consumer object, run it with poll() like this:
        loop:
            msg = consumer.poll(timeout=20)
            if msg is None: break  # no messages to fetch
            if msg.error(): 
                print(str(msg.error()))
                break
            jmsg = json.loads(msg.value())  # msg will be in json format
        """
        if not imported_kafka:
            message = 'Cannot import confluent_kafka'
            raise LasairError(message)

        settings = { 
          'bootstrap.servers': 'kafka.lsst.ac.uk:9092',
          'group.id': group_id,
          'default.topic.config': {'auto.offset.reset': 'smallest'}
        }
        c = Consumer(settings)
        c = consumer.subscribe([topic_in])
        return c

    def annotate_init(self, username, password, topic_out):
        """ Tell the Lasair client that you will be producing annotations
        args:
            username: as given to you by Lasair staff
            password: as given to you by Lasair staff
            topic_out: as given to you by Lasair staff
        Will fail if for some reason the confluent_kafka library cannot be imported.
        """
        if not imported_kafka:
            message = 'Cannot import confluent_kafka'
            raise LasairError(message)
        conf = { 
            'bootstrap.servers': 'kafka-pub:29092',
            'security.protocol': 'SASL_PLAINTEXT',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': username,
            'sasl.password': password
        }
        self.topic_out = topic_out
        self.kafka_producer = Producer(conf)
        return

    def annotate_send(self, msg):
        """ Send an annotation to Lasair
        args:
            msg: A python dictionary that has at least the keys
                objectId and classification, whose values are strings
        Will fail if annotate_init has not been called
        """
        if not self.kafka_producer:
            raise LasairError('Must call annotate_init first')
        if not type(msg) is dict :
            raise LasairError('Only a dictionary can be sent as annotation message')
        if not 'objectId' in msg:
            raise LasairError('objectId must be present in annotation message')
        if not 'classification' in msg:
            raise LasairError('classification must be present in annotation message')
        msg['topic'] = topic_out
        self.kafka_producer.produce(self.topic_out, json.dumps(msg))

    def annotate_flush(self):
        """ Finish an annotation session and close the producer
            If not called, your annotaityons will not go through!
        """
        if self.kafka_producer:
            self.kafka_producer.flush()

