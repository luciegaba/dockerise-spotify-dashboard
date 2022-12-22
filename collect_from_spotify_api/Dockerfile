FROM python:3.11
#!/bin/bash
# Any working directory can be chosen as per choice like '/' or '/home' etc

# Create a working directory.
RUN mkdir wd
WORKDIR wd

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY . ./


CMD [ "python", "main.py"]
