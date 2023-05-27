# Email-System
System that handles a large number of email requests


### Design diagram for the system
_To be added here_


### Starting the Services for Email System

This guide will walk you through the process of starting three services in Python: a producer service, a consumer service, and Kafka servers. These services will communicate with each other using Apache Kafka as the messaging system.

### Prerequisites

Before you start, ensure that you have the following installed on your system, except MongoDB:

- Python (version _3.9.7_ or higher)
- Kafka (version __ or higher)
- Flask (version __ or higher)
- MongoDB

------------

_**Note**: The services has not been dockerized yet. When it is done, the .md file will be updated._

------------

### Steps To Follow

Follow these steps to start the three services:

1. **Start Kafka**

   Start your Kafka server by running the appropriate command based on your installation. This typically involves starting the ZooKeeper server and then starting the Kafka broker. You can refer to the Kafka documentation for detailed setup.

   After the setup, start the ZooKeeper for Kafka
   ```shell
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
   ```
   _This will pull image file of the MongoDB database_

   Start the Kafka broker
   ```shell
   .\bin\windows\kafka-server-start.bat .\config\server.properties
   ```

2. **Set Up MongoDB Database**

   In your preferred terminal or command prompt
   
    ```shell
   docker pull mongo
   ```
   _This will pull image file of the MongoDB database_

    Then, run the container
    
   ```shell
   docker run --name mongodb -p 27017:27017 mongo
    ```
    
3. **Start the Consumer Service**

   Run the following command to start the consumer service (consumer 1):

   ```shell
   python kafkaServerService.py
    ```
   
    Run the following command to start the next consumer service (consumer 2):

   ```shell
   python kafkaDBService.py
    ```

4. **Start the Producer Service**

   Run the following command to start the producer service: _(You can skip this if to run in Docker)_

   ```shell
   python apiGateway.py
    ```
   
   **_To run it on Docker, execute the following two commands:_**
   ```shell
   docker build -t api-gateway -f apiGatewayDockerfile .
    ```
   Then,
      ```shell
   docker run --name api-gateway-container -d -p 8000:8000 api-gateway
    ```
   
5. **Interact with the Services**
   
   Run the following command to send the email:
   ```shell
   curl --header "Content-Type: application/json" --request POST --data "{\"emailFrom\": \"tese320@gmail.com\", \"emailTo\": \"test1@gmail.com\", \"message\": \"Message from gateway\", \"subject\": \"apigateway.\", \"templateFlag\": \"1\"}"  http://localhost:8000/sendMail
   ```

   Run the following command to query the email records:
   ```shell
   curl --header "Content-Type: application/json" --request POST --data "{\"emailAddress\": \"tese320@gmail.com\", \"startTime\": \"2022-08-15\", \"endTime\": \"2022-10-15\"}" http://localhost:8000/queryMail
   ```
