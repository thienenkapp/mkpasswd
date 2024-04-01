#
# Based on https://www.artefact.com/blog/how-to-deploy-and-secure-your-streamlit-app-on-gcp/
#
FROM python:3.11-slim

# Expose port you want your app on
EXPOSE 8080

#WORKDIR .
WORKDIR /app

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY app.py app.py

# Run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
