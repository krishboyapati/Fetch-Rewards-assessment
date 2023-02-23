# Fetch-Rewards-assessment
To run the project, you will need:

You will need the following installed on your local machine
a. docker -- docker install guide
b. docker-compose
c. pip install awscli-local
d. Psql - install

Requirements:
1.Docker (https://www.docker.com/)
2.Python 3.7 or later (https://www.python.org/downloads/)
3.Git (https://git-scm.com/)
4.Python packages: psycopg2
4.Psql
5.awscli


Clone the repository to your local machine:
  $ git clone https://github.com/krishboyapati/Fetch-Rewards-assessment

  $ cd Fetch-Rewards-assessment
  $ docker-compose up
  $ python SQS_POSTGRESS.py


### Application Deployment

To deploy the application in production, we will need to do the following:

- Set up an AWS SQS Queue and grant the appropriate permissions to the application to read messages from the queue.
- Set up a Postgres database and create the `user_logins` table.
- Store the database credentials and SQS Queue URL securely.
- Configure the application to read from the SQS Queue and write to the Postgres database.

### Making the Application Production Ready

To make the application production ready, we could do the following:

- Implement logging to track errors and usage.
- Use a configuration management tool like Ansible or Puppet to automate deployment and configuration.
- Use a container orchestration tool like Kubernetes or Docker Swarm to manage containers and scale the application.
- Implement load balancing to distribute traffic across multiple instances of the application.
- Implement data backups and disaster recovery measures.

### Scaling the Application

To scale the application with a growing dataset, we could do the following:

- Use a distributed message queue like Apache Kafka to handle larger volumes of data.
- Use a distributed database like Apache Cassandra or Amazon Aurora to handle larger volumes of data.
- Use a caching layer like Redis or Memcached to cache frequently accessed data and reduce load on the database.

### Recovering PII Data

To recover PII data, we would need to store the original values of the `device_id` and `ip` fields in a separate table or database that is encrypted and secured. We could then use this table to look up the original values of the `masked_device_id` and `masked_ip` fields.

### Assumptions

The assumptions we made while developing this solution are:

- The JSON objects received from the SQS Queue have the same structure as the sample data provided.
- The `user_id` field in the JSON objects is unique.
- The `device_id` and `ip` fields contain sensitive PII data that need to be masked before storing in the database.
- We are only interested in the `create_date` field for each JSON object.
- The application will be run on a Unix-based operating system.
- The database credentials and SQS Queue URL will be stored securely.

## Next Steps

If we had more time, we would do the following:

- Implement unit tests to ensure the application works as expected.
- Implement error handling to gracefully handle errors and prevent data loss.
- Implement rate limiting to prevent the application from overwhelming the database or message queue.
- Implement a dashboard to monitor the application's performance and usage.
- Implement a data retention policy to delete older data from the database.
- Implement a security audit to identify and address security vulnerabilities in the application and infrastructure.
- Implement a CI/CD pipeline to automate building, testing, and deploying the application.

## Conclusion

In this project, we demonstrated how to read JSON data from an AWS SQS Queue, mask sensitive PII data, and write the data to a Postgres database. We also discussed how to deploy the application in production, make the application production ready, scale the application, and recover PII data. We made several assumptions and outlined next steps for further development.
