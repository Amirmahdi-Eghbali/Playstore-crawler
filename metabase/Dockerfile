# Use an ARM64 compatible base image with Java
FROM arm64v8/openjdk:11-jre-slim

# Set environment variable for Metabase DB file location
ENV MB_DB_FILE=/metabase.db

# Expose the port Metabase uses
EXPOSE 3000

# Copy the Metabase JAR file into the container
COPY metabase.jar /app/metabase.jar

# Set the working directory
WORKDIR /app

# Command to run the Metabase application
CMD ["java", "-jar", "metabase.jar"]