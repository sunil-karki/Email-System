from kafka import KafkaProducer, KafkaConsumer
from json import dumps
from json import loads

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic1 = 'email_requests'
email_responses_topic1 = 'email_responses'

email_requests_topic2 = 'email_requestsecond'
email_responses_topic2 = 'email_responsesecond'


def send_email_request1(producer, email_from, email_to, message, subject, template_flag):
    email_request = {
        'emailFrom': email_from,
        'emailTo': email_to,
        'message': message,
        'subject': subject,
        'templateFlag': template_flag
    }
    producer.send(email_requests_topic1, value=email_request)
    print("producer.send1")
    producer.flush()


def send_email_request2(producer, email_from, email_to, message):
    email_request = {
        'emailFrom': email_from,
        'emailTo': email_to,
        'message': message
    }
    producer.send(email_requests_topic2, value=email_request)
    print("producer.send2")
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


def get_email_details_response2(consumer):
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
    producer1 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                              value_serializer=lambda x:
                              dumps(x).encode('utf-8'))
    consumer1 = KafkaConsumer(email_responses_topic1, bootstrap_servers=['localhost:9092'],
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              # group_id='my-group',
                              value_deserializer=lambda x: loads(x.decode('utf-8'))
                              )

    producer2 = KafkaProducer(bootstrap_servers=['localhost:9092'],
                              value_serializer=lambda x:
                              dumps(x).encode('utf-8'))
    consumer2 = KafkaConsumer(email_responses_topic2, bootstrap_servers=['localhost:9092'],
                              auto_offset_reset='earliest',
                              enable_auto_commit=True,
                              # group_id='my-group',
                              value_deserializer=lambda x: loads(x.decode('utf-8'))
                              )

    email_from = "sunilkarki320@gmail.com"
    email_to = "sunilkarki520@gmail.com"
    message = "Hello, this is a test email."
    subject = "test email."
    template_flag = "1"
    send_email_request1(producer1, email_from, email_to, message, subject, template_flag)
    print("Email sent to first topic")
    # get_email_details_response1(consumer1)

    print("---------------")

    # Request 2: Get email details
    email_address = "test2@gmail.com"
    send_email_request2(producer2, "", email_address, "")
    get_email_details_response2(consumer2)
    print("Response fetched from second topic")


if __name__ == '__main__':
    run()
