"""
## Consumer Service 2 -
## Consumer service to handle request to query emails based on the parameters provided.
##
"""

import json
import pprint
import sys

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from json import dumps
from bson import json_util
from datetime import datetime

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic = 'email_requestsecond'
email_responses_topic = 'email_responsesecond'

# MongoDB configuration
mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_database = 'email_db'
mongodb_collection = 'emails'
client = ""


# Create query for MongoDB for email recordsQuery email details from MongoDB
def createQueryForDatabase(email_to, start_time, end_time):
    query = {}

    if not (email_to is None or email_to == ""):
        query["emailto"] = email_to

    if not ((start_time is None or start_time == "") and (end_time is None or end_time == "")):
        query['emailtimestamp'] = {}
        if not (start_time is None or start_time == ""):
            query['emailtimestamp']['$gte'] = datetime.strptime(start_time, '%Y-%m-%d')

        if not (end_time is None or end_time == ""):
            query['emailtimestamp']['$lte'] = datetime.strptime(end_time, '%Y-%m-%d')

    return query


# Function to query records of Emails.
def queryEmailRecord(email_request):
    # MongoDB details
    # client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))
    db = client[mongodb_database]
    collection = db[mongodb_collection]

    # Request provided by the producer
    email_to = email_request['emailTo']
    start_time = email_request['startTime']  # Starting Time Range to query
    end_time = email_request['endTime']  # Ending Time Range to query

    print("Request for: " + email_to + " " + start_time + " " + end_time)

    # Create query for request provided by the producer.
    query = createQueryForDatabase(email_to, start_time, end_time)
    print("query: " + str(query))

    # Executing query for requests.
    try:
        email_document = collection.find(query)

        if email_document:
            # pprint.pprint(email_document)
            return json.loads(json_util.dumps(email_document))
        else:
            print("Email not found")
            email_response = "{'msg': 'Email not found.'}"
            return json.loads(email_response)

    except Exception as e:
        print("Failed to the Query Database!!")
        raise Exception("Failed to the Query Database!! " + str(e))


# Function to process queries/request from the producer.
def processProducerRequests(consumer, producer):
    print("Processing email requests to query emails ...")
    print("----------------------------------------------------")

    for message in consumer:
        email_request = message.value.decode('utf-8')  # Decode the message value
        email_request = eval(email_request)  # Convert the string to a dictionary

        try:
            list_of_emails = queryEmailRecord(email_request)

            # for email_response in list_of_emails['records']:
            pprint.pprint(list_of_emails)
            producer.send(email_responses_topic, value=list_of_emails)
            producer.flush()

        except Exception as e:
            print(str(e))

        print("----------------------------------------------------")


def run():
    consumer = KafkaConsumer(email_requests_topic, bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    processProducerRequests(consumer, producer)


if __name__ == '__main__':
    if len(sys.argv) == 5:
        bootstrap_servers = sys.argv[1] + ":" + sys.argv[2]
        mongodb_host = sys.argv[3]
        mongodb_port = sys.argv[4]

    print("Looking for Kafka broker on " + bootstrap_servers)
    print("Looking for MongoDB on " + mongodb_host + ":" + str(mongodb_port))
    client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))

    try:
        # Test the MongoDB connection
        client.admin.command('ismaster')
        print("MongoDB connection successful!")

        run()

    except Exception as e:
        print("Failed to connect: ", str(e))
    finally:
        # Close the connection
        client.close()
