import grpc
from concurrent import futures
import time

import email_pb2
import email_pb2_grpc

from pymongo import MongoClient

# MongoDB connection details
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DATABASE = 'email_db'
MONGODB_COLLECTION = 'emails'

class EmailServicer(email_pb2_grpc.EmailServiceServicer):
    def __init__(self):
        # Connect to MongoDB
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        self.db = client[MONGODB_DATABASE]
        self.collection = self.db[MONGODB_COLLECTION]

    def QueryEmails(self, request, context):
        start_time = request.start_time
        end_time = request.end_time
        email_address = request.email_address

        # Query MongoDB based on the provided criteria
        query = {
            'timestamp': {
                '$gte': start_time,
                '$lte': end_time
            },
            'email_address': email_address
        }
        emails = self.collection.find(query)

        # Create EmailResponse messages for each matching email
        responses = []
        for email in emails:
            response = email_pb2.EmailResponse(
                subject=email['subject'],
                message=email['message'],
                emailTo=email['email_to'],
                emailFrom=email['email_from']
            )
            responses.append(response)

        # print the emails
        for response in responses:
            print(response)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    email_pb2_grpc.add_EmailServiceServicer_to_server(EmailServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started")

    try:
        while True:
            time.sleep(86400)  # 24 hours
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
