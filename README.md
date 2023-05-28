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

   Start your Kafka server by running the appropriate command based on your installation. This typically involves starting the ZooKeeper server and then starting the Kafka broker. You can refer to the Kafka documentation for detailed setup.<br>
   <br>
   After the setup, start the ZooKeeper for Kafka
   ```shell
   .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
   ```
   <br>

   Start the Kafka broker
   ```shell
   .\bin\windows\kafka-server-start.bat .\config\server.properties
   ```
   <br>

2. **Set Up MongoDB Database**

   In your preferred terminal or command prompt:
   
    ```shell
   docker pull mongo
   ```
   _This will pull image file of the MongoDB database_
   <br><br>
   Then, run the container _(27017 is port for MongoDB)_
    
   ```shell
   docker run --name mongodb -d -p 27017:27017 mongo
    ```
   <br>
   
3. **Start the Consumer Service**

   Run the following command to start the EmailService (consumer 1): _(You can skip this if to run in Docker)_

   ```shell
   python kafkaServerService.py
    ```
   
    Run the following command to start the next consumer service (consumer 2): _(You can skip this if to run in Docker)_

   ```shell
   python kafkaDBService.py
    ```
   <br>

   **_To run it on Docker, execute the following four commands below:_** <br> 
   **Note:** In files _'serverServiceDockerfile'_ and _'dbServiceDockerfile'_, add IP address/port 
   where kafka server runs and also IP address/port for MongoDB. IP address could be found with _ipconfig_ 
   or _ifconfig_. <br><br>
   For EmailService (consumer 1):

   ```shell
   docker build -t email-service -f serverServiceDockerfile .
    ```
   
   ```shell
   docker run --name email-service-container2 -d email-service
    ```
   
   Then, for DBService (consumer 2):
   
   ```shell
   docker build -t db-service -f dbServiceDockerfile .
    ```
   
   ```shell
   docker run --name db-service-container3 -d db-service
    ```
   <br>

4. **Start the Producer Service**

   Run the following command to start the ApiGateway service (producer): _(You can skip this if to run in Docker)_

   ```shell
   python apiGateway.py
    ```
   <br>
   
   **_To run it on Docker, execute the following two commands:_** <br> **Note:** In _apiGatewayDockerfile_, add IP address/port where kafka server runs.

   ```shell
   docker build -t api-gateway -f apiGatewayDockerfile .
    ```
   Then,
      ```shell
   docker run --name api-gateway-container -d -p 8000:8000 api-gateway
    ```
   <br>
   
5. **Interact with the Services**
   
   Run the following command to send the email:
   ```shell
   curl --header "Content-Type: application/json" --request POST --data "{\"emailFrom\": \"tese320@gmail.com\", \"emailTo\": \"test1@gmail.com\", \"message\": \"Message from gateway\", \"subject\": \"apigateway.\", \"templateFlag\": \"1\"}"  http://localhost:8000/sendMail
   ```

   Run the following command to query the email records/documents:
   ```shell
   curl --header "Content-Type: application/json" --request POST --data "{\"emailAddress\": \"tese320@gmail.com\", \"startTime\": \"2022-08-15\", \"endTime\": \"2022-10-15\"}" http://localhost:8000/queryMail
   ```
