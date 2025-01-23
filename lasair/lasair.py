""" Lasair API

This class enables programmatic access to the Lasair database and Sherlock service, 
as described at http://lasair-ztf.lsst.ac.uk/api/.

Args:
    token (string): The Calls are throttled by the lasair server, by use of an 
    'authorization token', as described in the api documentation above. 
    There is a free token listed there, but it is throttled at 10 calls per hour. 
    Once a user has an account at the Lasair webserver, they can get their own token
    allowing 100 calls per hour, or request to be a power user, with infinite usage.

    cache (string): Results can be cached on local filesystem, by providing 
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
    def __init__(self, token, cache=None, endpoint='https://lasair-ztf.lsst.ac.uk/api', timeout=60.0):
        self.headers = { 'Authorization': 'Token %s' % token }
        self.endpoint = endpoint
        self.timeout = timeout
        self.cache = cache
        if cache and not os.path.isdir(cache):
            message = 'Cache directory "%s" does not exist' % cache
            raise LasairError(message)

    def fetch_from_server(self, method, input):
        url = '%s/%s/' % (self.endpoint, method)
        try:
            r = requests.post(url, data=input, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.ReadTimeout:
            raise LasairError('Request timed out')

        if r.status_code == 200:
            try:
                result = r.json()
            except:
                result = {'error': 'Cannot parse Json %s' % r.text}
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
            message = 'HTTP return code %d for\n' % r.status_code
            message += url
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

    def objects(self, objectIds):
        """ Get object pages in machine-readable form
        args:
            objectIds: list of objectIds
        return:
            list of dictionaries, each being all the information presented
            on the Lasair object page.
        """

        input = {'objectIds':objectIds}
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
        if len(objectIds) > 10:
            raise LasairError('Method can only handle 10 or less objectIds')

        objectIds = [str(obj) for obj in objectIds]
        input = {'objectIds':','.join(objectIds)}
        result = self.fetch('lightcurves', input)
        return result

    def sherlock_object(self, objectId, lite=True):
        """ Query the Sherlock database for context information about an object
            in the database.
        args:
            objectsId: objectId
            lite (boolean): If true, get extended information including a 
                list of possible crossmatches.
        return:
            dictionary
        """
        try:
            input = {'objectId':objectId, 'lite':lite}
            result = self.fetch('sherlock/object', input)
        except:
            input = {'objectIds':[objectId], 'lite':lite}
            result = self.fetch('sherlock/objects', input)
        return result

    def sherlock_objects(self, objectIds, lite=True):
        """ DEPRECATED """
        input = {'objectIds':objectIds, 'lite':lite}
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

    def annotate(self, topic, objectId, classification, \
            version='0.1', explanation='', classdict={}, url=''):
        """ Send an annotation to Lasair
        args:
            topic         : the topic for which this user is authenticated
            objectId      : the object that this annotation should be attached to
            classification: short string for the classification
            version       : the version of the annotation engine
            explanation   : natural language explanation
            classdict     : dictionary with further information
            url           : url with further information about this classification
        """

        if not classification or len(classification) == 0:
            raise LasairError('Classification must be a short nontrivial string')
        if len(version) > 16:
            raise LasairError('Version must be 16 characters or less')

        msg = {
            'objectId'      : objectId, 
            'topic'         : topic,
            'classification': classification,
            'version'       : version,
            'explanation'   : explanation,
            'classdict'     : json.dumps(classdict),
            'url'           : url,
        }

        result = self.fetch_from_server('annotate', msg)
        return result

class lasair_consumer():
    """ Creates a Kafka consumer for Lasair streams """
    def __init__(self, host, group_id, topic_in):
        """ Consume a Kafka stream from Lasair
        args:
            host:     Host name:port for consuming Kafka
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
        settings = { 
          'bootstrap.servers': host,
          'group.id': group_id,
          'default.topic.config': {'auto.offset.reset': 'smallest'}
        }
        try:
            from confluent_kafka import Consumer
            self.consumer = Consumer(settings)
            self.consumer.subscribe([topic_in])
        except:
            self.consumer = None
            raise LasairError('Failed to import confluent_kafka. Try "pip install confluent_kafka"')

    def poll(self, timeout = 10):
        """ Polls for a message on the consumer with timeout is seconds
        """
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

class lasair_producer():
    """ Creates a Kafka producer for Lasair annotations """
    def __init__(self, host, username, password, topic_out):
        """ Tell the Lasair client that you will be producing annotations
        args:
            host:     Host name:port for producing Kafka
            username: as given to you by Lasair staff
            password: as given to you by Lasair staff
            topic_out: as given to you by Lasair staff
        Will fail if for some reason the confluent_kafka library cannot be imported.
        """
        conf = { 
            'bootstrap.servers': host,
            'security.protocol': 'SASL_PLAINTEXT',
            'sasl.mechanisms': 'SCRAM-SHA-256',
            'sasl.username': username,
            'sasl.password': password
        }
        self.topic_out = topic_out
        try:
            from confluent_kafka import Producer
            self.producer = Producer(conf)
        except Exception as e:
            self.producer = None
            raise LasairError('Failed to make kafka producer.' + str(e))

    def produce(self, objectId, classification, \
            version=None, explanation=None, classdict=None, url=None):
        """ Send an annotation to Lasair
        args:
            objectId      : the object that this annotation should be attached to
            classification: short string for the classification
            version       : the version of the annotation engine
            explanation   : natural language explanation
            classdict     : dictionary with further information
        """

        if self.producer == None:
            raise LasairError('No valid producer')
        if not classification or len(classification) == 0:
            raise LasairError('Classification must be a short nontrivial string')

        msg = {
            'objectId'      : objectId, 
            'topic'         : self.topic_out,
            'classification': classification,
        }

        if version    : msg['version']     = version
        if explanation: msg['explanation'] = explanation
        if classdict  : msg['classdict']   = classdict
        if url        : msg['url']         = url

        self.producer.produce(self.topic_out, json.dumps(msg))

    def flush(self):
        """ Finish an annotation session and close the producer
            If not called, your annotations will not go through!
        """
        if self.producer != None:
            self.producer.flush()

