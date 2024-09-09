"""
Rate limited consumer. Reads messages from Kafka that have an objectId,
but the poll method returns only those where the object 
has not been seen in given interval.
Keeps track of when a given objectId was last passed through ('accepted'), 
and only accepts those that have not been accepted during interval 'interval'.
Also keeps track of number of rejects per objectId since last time 
it was accepted.

"""
import sys
import time
import json
import random
import datetime
import sqlite3

def now():
    # time since 1970 in days
    return float(time.time())/(24*60*60) 

def now_human():
    return str(datetime.datetime.now())

class lasair_RL_consumer():
    def __init__(self, host, group_id, topic_in, filename, interval=30, verbose=None):
        """ Consume a Kafka stream from Lasair but restricted 
        to objectId that has not been seen in time "interval".
        args:
            host:     Host name:port for consuming Kafka
            group_id: a string. If used before, the server will start from last message
            topic_in: The topic to be consumed. Example 'lasair_2SN-likecandidates'
            filename: where to keep the sqlite database
            interval: days to wait before sending same objectId
        """
        self.conn = sqlite3.connect(filename)
        self.topic_in = topic_in
        self.interval = interval
        self.verbose = verbose
        self.createTable()
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
        while 1:
            msg = self.consumer.poll(timeout=timeout)
            if msg is None:
                break
            if msg.error():
                print(str(msg.error()))
                break
            objectId = json.loads(msg.value())['objectId']
            if self.verbose:
                print('consume: %s' % objectId)
            if self.ago(objectId) < self.interval:
                self.reject(objectId)
                if self.verbose:
                    print('consume: %s rejected' % objectId)
            else:
                self.accept(objectId)
                if self.verbose:
                    print('%s accepted' % objectId)
                return msg

    def createTable(self):
    # Shows the sqlite table used by this program.
    # Idempotent because create table if not exists
        create = """
          CREATE TABLE IF NOT EXISTS obj (
          objectId text,
          lastSent float,
          reject integer,
          PRIMARY KEY (objectId)
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(create)
        self.conn.commit()
        if self.verbose:
            print('Created table')
    
    def reject(self, objectId):
        # objectId already sent within interval, dont send, 
        # just increment the number of times seen since last accept
        nw = now()
        queryfmt = """
            UPDATE obj SET reject=reject+1 WHERE objectId='%s';
        """
        query = queryfmt % objectId
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        if self.verbose:
            print('%s rejected' % objectId)
    
    def accept(self, objectId):
        # objectId not present or not sent since interval, 
        # so update or create record in database
        nw = now()
        queryfmt = """
            INSERT OR IGNORE INTO obj (objectId, lastSent, reject) 
                VALUES ('%s', %f, 0)
            ON CONFLICT(objectId) DO UPDATE SET 
                lastSent=%f, reject = 0
        """
        query = queryfmt % (objectId, nw, nw)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        if self.verbose:
            print('accept: %s at %.3f' % (objectId, nw))
    
    def ago(self, objectId):
        # How many days since we saw this objectId
        query = """
          SELECT lastSent FROM obj
          WHERE objectId='%s'
        """
        query = query % objectId
        cursor = self.conn.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        if row and len(row) > 0:
            ago = now() - row[0]
            if self.verbose:
                print('ago: %s at %.3f ago' % (objectId, ago))
            return ago
        else:
            if self.verbose:
                print('ago: %s not found' % objectId)
            return 1000000  # infinity

    def delete(self, objectId):
        # delete objectId from database
        queryfmt = """
            DELETE FROM obj WHERE objectId='%s'
        """
        query = queryfmt % (objectId)
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        if self.verbose:
            print('delete: %s' % objectId)
    
    def printall(self):
        print(self.topic_in)
        print('At', now_human())
        query = """
          SELECT * FROM obj
          ORDER BY lastSent DESC
        """
        cursor = self.conn.cursor()
        nw = now()
        cursor.execute(query)
        for row in cursor.fetchall():
            print('%s accepted %.3f days ago, rejected %d times' \
            % (row[0], nw-row[1], row[2]))
