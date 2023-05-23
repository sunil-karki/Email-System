import grpc

import email_pb2
import email_pb2_grpc

def send_email(subject, message, email_to, email_from):
    channel = grpc.insecure_channel('localhost:50051')  # Update with the server address
    stub = email_pb2_grpc.EmailServiceStub(channel)

    # Create an EmailRequest message
    request = email_pb2.EmailRequest(
        subject=subject,
        message=message,
        emailTo=email_to,
        emailFrom=email_from
    )

    response = stub.SendEmail(request)

    # Process the response
    if response.success:
        print("Email sent successfully!")
    else:
        print("Failed to send email.")
        print("Error message:", response.message)

if __name__ == '__main__':
    subject = "Hello"
    message = "This is a test email."
    email_to = "recipient@example.com"
    email_from = "sender@example.com"

    send_email(subject, message, email_to, email_from)
