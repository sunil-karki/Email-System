from kafka import KafkaConsumer, KafkaProducer
from json import dumps

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic = 'email_requests'
email_responses_topic = 'email_responses'


def process_email_requests(consumer, producer):
    print("Processing email requests...")
    for message in consumer:
        email_request = message.value.decode('utf-8')  # Decode the message value
        email_request = eval(email_request)
        print(email_request)
        email_from = email_request['emailFrom']
        email_to = email_request['emailTo']
        message = email_request['message']

        # Process email request

        # Send acknowledgement
        email_response = {'acknowledgement': 'Email received.'}
        producer.send(email_responses_topic, value=email_response)
        producer.flush()


def run():
    consumer = KafkaConsumer(email_requests_topic, bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    process_email_requests(consumer, producer)


if __name__ == '__main__':
    run()
