from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from json import dumps
import pprint

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic = 'email_requests'
email_responses_topic = 'email_responses'

# MongoDB configuration
mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_database = 'email_db'
mongodb_collection = 'emails'


def process_email_requests(consumer, producer):
    client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))
    db = client[mongodb_database]
    collection = db[mongodb_collection]

    for message in consumer:
        email_request = message.value.decode('utf-8')  # Decode the message value
        email_request = eval(email_request)  # Convert the string representation to a dictionary
        email_to = email_request['emailTo']
        print("Request for: " + email_to)

        # Query email details from MongoDB
        query = {"emailto": email_to}
        email_document = collection.find_one(query)
        pprint.pprint(email_document)

        if email_document:
            print("Record found from the DB..")
            # for email_doc in email_document:
            #     print("Record found..." + email_doc)
            email_from = email_document['emailfrom']
            message = email_document['emailbody']
            email_response = {
                'emailFrom': email_from,
                'emailTo': email_to,
                'message': message
            }
            # pprint.pprint(email_document['emailFrom'])
            # email_response = {
            #     'emailFrom': 'email_from',
            #     'emailTo': 'email_to',
            #     'message': 'message'
            # }
            producer.send(email_responses_topic, value=email_response)  # Encode the response as bytes

        else:
            print("Record NOT found...")
            email_response = {
                'error': 'Email not found.'
            }
            producer.send(email_responses_topic, value=email_response)  # Encode the response as bytes

        producer.flush()


def run():
    consumer = KafkaConsumer(email_requests_topic, bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    process_email_requests(consumer, producer)


if __name__ == '__main__':
    run()
