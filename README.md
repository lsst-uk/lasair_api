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
       lasair_client(token, cache=None)
       
       Methods defined here:
       
       __init__(self, token, cache=None)
           Initialize self.  See help(type(self)) for accurate signature.
       
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

       stream_consumer(self, group_id, topic_in):
           Consume a Kafka stream from Lasair
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

        annotate_init(self, username, password, topic_out):
            Tell the Lasair client that you will be producing annotations
            args:
                username: as given to you by Lasair staff
                password: as given to you by Lasair staff
                topic_out: as given to you by Lasair staff
            Will fail if for some reason the confluent_kafka library cannot be imported.

        annotate_send(self, msg):
            Send an annotation to Lasair
            args:
                msg: A python dictionary that has at least the keys
                    objectId and classification, whose values are strings
            Will fail if annotate_init has not been called

        annotate_flush(self):
            Finish an annotation session and close the producer
            If not called, your annotaityons will not go through!
