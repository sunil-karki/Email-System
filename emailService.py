import grpc
import time
import email.message
import smtplib
from concurrent import futures
import email_pb2
import email_pb2_grpc

class EmailService(email_pb2_grpc.EmailService):
    def SendEmail(self, request, context):
        # Extract email details from the gRPC request
        subject = request.subject
        message = request.message
        email_to = request.emailTo
        email_from = request.emailFrom

        print("SendEmail")
        time.sleep(50)  # delay for 5 seconds

        email_msg = email.message.EmailMessage()
        email_msg['Subject'] = subject
        email_msg['From'] = email_from
        email_msg['To'] = email_to
        email_msg.set_content(message)

        try:
            # Send the email using an SMTP server
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'your_smtp_username'
            smtp_password = 'your_smtp_password'

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                print("Sending mail..")
                server.send_message(email_msg)
                server.quit()

            # Return a gRPC response indicating success
            return email_pb2.EmailResponse(success=True, message='Email sent successfully')
        except Exception as e:
            # Return a gRPC response indicating failure and the error message
            return email_pb2.EmailResponse(success=False, message=str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    email_pb2_grpc.add_EmailServiceServicer_to_server(EmailService(), server)
    server.add_insecure_port('[::]:50051')  # Replace with your desired server port
    server.start()
    print("Server started. Listening on port 50051...")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
