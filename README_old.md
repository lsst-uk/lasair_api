# lasair_api
Client package for Lasair

NAME
    lasair - Lasair API

DESCRIPTION
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

CLASSES
    class lasair_client(builtins.object)
       Methods defined here:
       
       __init__(self, token, cache=None, endpoint='http://192.41.108.37:8080/api')
           Initialize self.  See help(type(self)) for accurate signature.
           Args:
               cache: name of a directory where results can be cached 
               endpoint: endpoint of the Lasair API service
       
       cone(self, ra, dec, radius=5, requestType='all')
           Run a cone search on the Lasair database.
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
       
       lightcurves(self, objectIds)
           Get simple lightcurves in machine-readable form
           args:
               objectIds: list of objectIds, maximum 10
           return:
               list of dictionaries, one for each objectId. Each of these
               is a list of dictionaries, each having attributes
               candid, fid, magpsf, sigmapsf, isdiffpos, mjd
       
       objects(self, objectIds)
           Get object pages in machine-readable form
           args:
               objectIds: list of objectIds, maximum 10
           return:
               list of dictionaries, each being all the information presented
               on the Lasair object page.
       
       query(self, selected, tables, conditions, limit=1000, offset=0)
           Run a database query on the Lasair server.
           args: 
               selected (string): The attributes to be returned by the query
               tables (string): Comma-separated list of tables to be joined
               conditions (string): the "WHERE" criteria to restrict what is returned
               limit: (int) (default 1000) the maximum number of records to return
               offset: (int) (default 0) offset of record number
           return:
               a list of dictionaries, each representing a row
       
       sherlock_objects(self, objectIds, lite=True)
           Query the Sherlock database for context information about objects
               in the database.
           args:
               objectsIds: list of objectIds, maximum 10
               lite (boolean): If true, get extended information including a 
                   list of possible crossmatches.
           return:
               list of dictionaries, one for each objectId.
       
       sherlock_position(self, ra, dec, lite=True)
           Query the Sherlock database for context information about a position
               in the sky.
           args:
               ra (float): Right Ascension in decimal degrees
               dec (float): Declination in decimal degrees
               lite (boolean): If true, get extended information including a 
                   list of possible crossmatches.
           return:
               dictionary of contect information
       
       streams(self, topic, limit=1000)
           Get records from a given stream
           args:
               topic (string): Name of stream to be returned.
           return:
               list of dictionaries, each representing a row
       
       streams_topics(self, regex='.*', limit=1000)
           Get a list of available streams that match a given expression.
           args:
               regex (string, default .*): Search for stream names that match a pattern
               limit: (int, default 1000): Maximum number of stream names to return.
           return:
               List of stream names

        annotate(self, topic, objectId, classification, \
            version='0.1', explanation='', classdict={}, url='')
            Send an annotation to Lasair
            Note: Only the registered owner of this topic can send annotations to it
            args:
                topic         : the topic for which this user is authenticated
                objectId      : the object that this annotation should be attached to
                classification: short string for the classification
                version       : the version of the annotation engine
                explanation   : natural language explanation
                classdict     : dictionary with further information
                url           : url with further information about this classification
            return:
                Status message

    class lasair_consumer(builtins.object)
       Consume a Kafka stream from Lasair
       
       __init__(self, host, group_id, topic_in):
            Consume a Kafka stream from Lasair
            args:
                host:     Host name:port for consuming Kafka
                group_id: a string. If used before, the server will start from last message
                topic_in: The topic to be consumed. Example 'lasair_2SN-likecandidates'
            Imports confluent_kafka.
            Connects to Lasair public kafka to get the chosen topic.
            Once you have the returned consumer object, run it with poll() like this:
            loop:
                msg = consumer.poll(timeout=20)
                if msg is None: break  # no messages to fetch
                if msg.error(): 
                    print(str(msg.error()))
                    break
                jmsg = json.loads(msg.value())  # msg will be in json format

        poll(self, timeout = 10):
            Polls for a message on the consumer with timeout is seconds

    class lasair_producer():
        Creates a Kafka producer for Lasair annotations

        def __init__(self, host, username, password, topic_out):
            Tell the Lasair client that you will be producing annotations
            args:
                host:     Host name:port for producing Kafka
                username: as given to you by Lasair staff
                password: as given to you by Lasair staff
                topic_out: as given to you by Lasair staff
            Imports confluent_kafka.

        def produce(self, objectId, classification, \
            version=None, explanation=None, classdict=None, url=None):
            Send an annotation to Lasair
            args:
                objectId      : the object that this annotation should be attached to
                classification: short string for the classification
                version       : the version of the annotation engine
                explanation   : natural language explanation
                classdict     : dictionary with further information
    
        def flush(self):
            Finish an annotation session and close the producer
            If not called, your annotations will not go through!




Copyright 2022 The University of Edinburgh and Queen's University Belfast

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this code except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
