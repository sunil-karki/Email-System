"""
## API Gateway - Producer
## Producer service
## - First request: Gets emails to be sent
## - Second request: Gets request for querying the mails
## - Produces kafka messages for First request and Second request
## - Checks health of the services
## - Consume responses for the kafka messages made
##
"""

from flask import Flask, request
from kafka import KafkaProducer, KafkaConsumer
from json import dumps
from json import loads
import sys

# Kafka configuration
# bootstrap_servers=['localhost:9092']
bootstrap_servers = 'localhost:9092'
email_requests_topic1 = 'email_requests'
email_responses_topic1 = 'email_responses'

email_requests_topic2 = 'email_requestsecond'
email_responses_topic2 = 'email_responsesecond'

app = Flask(__name__)
flask_port = 8000


# Function to send email send request to consumers
def send_email_request1(producer, email_from, email_to, message, subject, template_flag):
    email_request = {
        'emailFrom': email_from,
        'emailTo': email_to,
        'message': message,
        'subject': subject,
        'templateFlag': template_flag
    }

    # Produce the message to Kafka
    producer.send(email_requests_topic1, value=email_request)
    print("message.producer.1.send")
    producer.flush()


# Function to send request to query email records to the consumers
def send_email_request2(producer, email_from, email_to, start_time, end_time):
    email_request = {
        'emailFrom': email_from,
        'emailTo': email_to,
        'startTime': start_time,
        'endTime': end_time
    }
    producer.send(email_requests_topic2, value=email_request)
    print("message.producer.2.send")
    producer.flush()


# Function to get response from consumers regarding email sent
def get_email_details_response1(consumer):
    print("-" + str(consumer))
    # print("-" + str(consumer["acknowledgement"]))
    for message in consumer:
        print("---")
        email_response = message.value.decode('utf-8')
        # email_response = message.value.decode('utf-8')
        # email_response = eval(email_response)
        print(email_response)


# Function to get response from consumers regarding the query on email records
def get_email_details_response2(consumer):
    for message in consumer:
        email_response = message.value
        # email_response = message.value.decode('utf-8')
        # email_response = eval(email_response)
        print(email_response)


@app.route('/sendMail', methods=['POST'])
def produce_message1():
    data = request.json

    # Extract the necessary information from the request
    email_from = data.get('emailFrom')
    email_to = data.get('emailTo')
    email_message = data.get('message')
    email_subject = data.get('subject')
    template_flag = data.get('templateFlag')

    producer1 = KafkaProducer(bootstrap_servers=bootstrap_servers,
                              value_serializer=lambda x:
                              dumps(x).encode('utf-8'))
    consumer1 = KafkaConsumer(email_responses_topic1, bootstrap_servers=bootstrap_servers,
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              # group_id='my-group',
                              value_deserializer=lambda x: loads(x.decode('utf-8'))
                              )

    send_email_request1(producer1, email_from, email_to, email_message, email_subject, template_flag)
    # get_email_details_response1(consumer1)

    print("Message for Kafka consumer1.")

    return 'Message sent to consumer1\n'


@app.route('/queryMail', methods=['POST'])
def produce_message2():
    data = request.json

    # Extract the necessary information from the request
    email_address = data.get('emailAddress')
    start_time_mail = data.get('startTime')
    start_end_mail = data.get('endTime')

    producer2 = KafkaProducer(bootstrap_servers=bootstrap_servers,
                              value_serializer=lambda x:
                              dumps(x).encode('utf-8'))
    consumer2 = KafkaConsumer(email_responses_topic2, bootstrap_servers=bootstrap_servers,
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              # group_id='my-group',
                              value_deserializer=lambda x: loads(x.decode('utf-8'))
                              )

    send_email_request2(producer2, "", email_address, start_time_mail, start_end_mail)
    # get_email_details_response2(consumer2)

    print("Message for Kafka consumer2.")

    return 'Message sent to consumer2'


@app.route('/health', methods=['GET'])
def health_check():
    print("Health check")
    return 'OK\n'


if __name__ == '__main__':
    if len(sys.argv) == 3:
        bootstrap_servers = sys.argv[1] + ":" + sys.argv[2]

    print("Looking for kafka broker on " + bootstrap_servers)
    app.run(host='0.0.0.0', port=flask_port)
