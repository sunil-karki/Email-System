"""
## Consumer Service 1 -
## Consumer service to send emails based on the email address and template chosen.
##
"""

# import time
# import email.message
import smtplib

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from json import dumps

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Kafka configuration
bootstrap_servers = 'localhost:9092'
email_requests_topic = 'email_requests'
email_responses_topic = 'email_responses'

# MongoDB configuration
mongodb_host = 'localhost'
mongodb_port = 27017
mongodb_database = 'email_db'
mongodb_collection = 'emails'
mongodb_collection_template = 'emailtemplate'


def loadEmailTemplate(template_flag, email_message):
    client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))
    db = client[mongodb_database]
    collection = db[mongodb_collection_template]

    # Query email details from MongoDB
    query = {"template_flag": template_flag}

    try:
        template_record = collection.find_one(query)
        if template_record:
            template_msg = template_record['template']

            template_msg.replace("<msg>", email_message)
            print('template_msg: ' + template_msg)

            return template_msg, "SUCCESS"

        else:
            print("Could not find the template specified!!!")
            return email_message, "ERROR"

    except Exception as e:
        raise Exception("Error found with Database!! " + str(e))


def insertToDB(email_to, email_from, subject, message, email_status):
    print("Inserting record to the Database ...")

    client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))
    db = client[mongodb_database]
    collection = db[mongodb_collection]

    record = {
        'subject': subject,
        'emailfrom': email_from,
        'emailto': email_to,
        'emailbody': message,
        'emailstatus': email_status
    }

    try:
        # Insert the record for Storage
        email_result = collection.insert_one(record)
        print(email_result)
        return "SUCCESS"
    except Exception as e:
        print("Insertion failed to the Database!!")
        status_msg = str(e)
        print(status_msg)
        return status_msg


def sendEmail(email_to, email_from, subject, email_message):
    print("Sending mail")
    # time.sleep(20)  # delay for 5 seconds

    try:
        sender_address = "testmailt828@gmail.com"
        sender_pass = 'Twilio123'

        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = email_to
        message['Subject'] = subject
        message.attach(MIMEText(email_message, 'plain'))

        session = smtplib.SMTP('smtp.gmail.com', 587)
        session.starttls()
        session.login(sender_address, sender_pass)
        text = message.as_string()

        session.sendmail(sender_address, email_to, text)
        session.quit()

        print("Email was sent to: " + email_to)
        return "SUCCESS"
    except Exception as e:
        print("Email NOT sent to: " + email_to)
        status_msg = str(e)
        print(status_msg)
        return status_msg


def process_email_requests(consumer, producer):
    print("Processing email requests...")
    for message in consumer:
        email_request = message.value.decode('utf-8')  # Decode the message value
        email_request = eval(email_request)
        print(email_request)
        email_from = email_request['emailFrom']
        email_to = email_request['emailTo']
        email_message = email_request['message']
        email_subject = email_request['subject']
        template_flag = email_request['templateFlag']
        # template_flag = 1

        print(template_flag)

        try:
            # Process email request
            email_template, email_template_status = loadEmailTemplate(template_flag, email_message)
            email_status = sendEmail(email_to, email_from, email_subject, email_template)
            db_status = insertToDB(email_to, email_from, email_subject, email_message, email_status)

            # Send acknowledgement
            email_response = {
                'acknowledgement': 'Email received.',
                'emailStatus': email_status,
                'dbStatus': db_status,
                'emailTemplateStatus': email_template_status
            }

            producer.send(email_responses_topic, value=email_response)
            producer.flush()
            print("response sent...")
        except Exception as e:
            print(str(e))


def run():
    consumer = KafkaConsumer(email_requests_topic, bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    process_email_requests(consumer, producer)


if __name__ == '__main__':
    run()
