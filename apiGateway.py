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


# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic1 = 'email_requests'
email_responses_topic1 = 'email_responses'

email_requests_topic2 = 'email_requestsecond'
email_responses_topic2 = 'email_responsesecond'

app = Flask(__name__)


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
    print("producer.send1")
    producer.flush()


def get_email_details_response1(consumer):
    print("-" + str(consumer))
    # print("-" + str(consumer["acknowledgement"]))
    for message in consumer:
        print("---")
        email_response = message.value.decode('utf-8')
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

    producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                              value_serializer=lambda x:
                              dumps(x).encode('utf-8'))
    consumer1 = KafkaConsumer(email_responses_topic1, bootstrap_servers=['localhost:9092'],
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
    topic = data.get('topic')
    message = data.get('message')

    # Produce the message to Kafka
    # producer.send(topic, value=message.encode())
    # producer.flush()

    print("Message for Kafka consumer2.")

    return 'OK\n'


@app.route('/health', methods=['GET'])
def health_check():
    print("Health check")
    return 'OK\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
