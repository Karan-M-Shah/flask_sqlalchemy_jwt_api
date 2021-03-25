# From allows us to initialize the build over a base image
# Alpine is a linux environment and the python version is 3.6.1
FROM python:3.6.1-alpine

# Copy the contents of your existing context into the app directory
COPY . /app

# The present working directory will be set as /app
WORKDIR /app

# Expose port 5000 of the container
EXPOSE 5000

# The run commands executes any commands needed to set up the application image
# This includes installing dependencies, editing files or changing permissions
RUN pip install -r requirements.txt

# CMD Is the command that is executed when the container is started
# There can only be 1 per Dockerfile, and this one is running the app folder
CMD ["python", "app.py"]

# Use the following command to build the image
# docker image build -t python-flask-project .

# Check for the image
# docker image ls