# Use the official MySQL image as the base image
FROM mysql:latest

# Set the MySQL root password
ENV MYSQL_ROOT_PASSWORD=toto

# Create a new user 'sql' with password 'Mili482b'
ENV MYSQL_USER=gab
ENV MYSQL_PASSWORD=toto

# Create a new database 'mqtt'
ENV MYSQL_DATABASE=makarov_airport

# Copy the database dump file to the container
COPY mqtt.sql /docker-entrypoint-initdb.d/

# Run the MySQL server
CMD ["mysqld"]