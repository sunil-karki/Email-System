"""
## Consumer Service 1 -
## Consumer service to send emails based on the email address and template chosen.
##
"""

# import time
# import email.message
import smtplib
import sys

from kafka import KafkaConsumer, KafkaProducer
from pymongo import MongoClient
from json import dumps

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

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
client = ""


# Function to load email template
def loadEmailTemplate(template_flag, email_message):
    db = client[mongodb_database]
    collection = db[mongodb_collection_template]

    # Query email details from MongoDB
    query = {"template_flag": template_flag}

    try:
        template_record = collection.find_one(query)
        if template_record:
            template_msg = template_record['template']

            template_msg = template_msg.replace("<msg>", email_message)
            print('Template msg: ' + template_msg)

            return template_msg, "SUCCESS"

        else:
            print("Could not find the template specified!!!")
            return email_message, "ERROR"

    except Exception as e:
        raise Exception("Error found with Database!! " + str(e))


# Function to insert document/record to the Database
def insertToDB(email_to, email_from, subject, message, email_status, email_status_desc, email_sent_time):
    print("Inserting record to the Database ...")

    # client = MongoClient("mongodb://" + mongodb_host + ":" + str(mongodb_port))
    db = client[mongodb_database]
    collection = db[mongodb_collection]

    record = {
        'subject': subject,
        'emailfrom': email_from,
        'emailto': email_to,
        'emailbody': message,
        'emailstatus': email_status,
        'emailstatusdesc': email_status_desc,
        'emailtimestamp': email_sent_time
    }

    try:
        # Insert the record for Storage
        email_result = collection.insert_one(record)
        print(email_result)
        return "SUCCESS", ""
    except Exception as e:
        print("Insertion failed to the Database!!")
        status_msg = str(e)
        print(status_msg)
        return "ERROR", status_msg


# Function to send mail
def sendEmail(email_to, email_from, subject, email_message):
    print("Sending mail ...")
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
        return "SUCCESS", ""
    except Exception as e:
        print("Email NOT sent to: " + email_to)
        status_msg = str(e)
        print(status_msg)
        return "ERROR", status_msg


# Function to process email request from the producer
def process_email_requests(consumer, producer):
    print("Processing email requests...")
    print("----------------------------------------------------")
    for message in consumer:
        email_request = message.value.decode('utf-8')  # Decode the message value
        email_request = eval(email_request)
        print(email_request)
        email_from = email_request['emailFrom']
        email_to = email_request['emailTo']
        email_message = email_request['message']
        email_subject = email_request['subject']
        template_flag = email_request['templateFlag']

        try:
            # Process email request
            email_template, email_template_status = loadEmailTemplate(template_flag, email_message)
            email_status, email_status_desc = sendEmail(email_to, email_from, email_subject, email_template)
            email_sent_time = datetime.utcnow()  # DateTime email has been sent
            db_status, db_status_desc = insertToDB(email_to, email_from, email_subject, email_message, email_status,
                                                   email_status_desc, email_sent_time)

            # Send acknowledgement
            email_response = {
                'acknowledgement': 'Email received.',
                'emailStatus': email_status,
                'dbStatus': db_status,
                'dbStatusDesc': db_status_desc,
                'emailTemplateStatus': email_template_status
            }

            producer.send(email_responses_topic, value=email_response)
            producer.flush()
            print("Response sent...")
        except Exception as e:
            print(str(e))

        print("----------------------------------------------------")


def run():
    consumer = KafkaConsumer(email_requests_topic, bootstrap_servers=bootstrap_servers)
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))
    process_email_requests(consumer, producer)


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
