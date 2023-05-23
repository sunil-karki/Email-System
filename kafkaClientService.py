from kafka import KafkaProducer, KafkaConsumer
from json import dumps
from json import loads

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic = 'email_requests'
email_responses_topic = 'email_responses'


def send_email_request(producer, email_from, email_to, message):
    email_request = {
        'emailFrom': email_from,
        'emailTo': email_to,
        'message': message
    }
    producer.send(email_requests_topic, value=email_request)
    print("producer.send")
    producer.flush()


def get_email_details_response(consumer):
    for message in consumer:
        email_response = message.value
        # email_response = message.value.decode('utf-8')
        # email_response = eval(email_response)
        print(email_response)
        # first_key = list(email_response.keys())[0]
        # if first_key == "acknowledgement":
        #     email_ack = email_response['acknowledgement']
        #     print(email_ack)
        # else:
        #     # email_ack = email_response['acknowledgement']
        #     print(email_ack)
        # return email_from, email_to, message


def run():
    print("Client")
    # producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    consumer = KafkaConsumer(email_responses_topic, bootstrap_servers=['localhost:9092'],
                             # auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             # group_id='my-group',
                             value_deserializer=lambda x: loads(x.decode('utf-8'))
                             )

    email_from = "sender@example.com"
    email_to = "recipient@example.com"
    message = "Hello, this is a test email."
    send_email_request(producer, email_from, email_to, message)
    print("Email sent.")

    # Request 2: Get email details
    email_address = "test2@gmail.com"
    send_email_request(producer, "", email_address, "")
    email_from, email_to, message = get_email_details_response(consumer)
    print("Email details for", email_address)
    print("From:", email_from)
    print("To:", email_to)
    print("Message:", message)


if __name__ == '__main__':
    run()
