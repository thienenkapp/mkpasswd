# mkpasswd
Make a password based on word lists.
mkpasswd run on Google Cloud Platform - GCP
This project is used as a learning exercise.

# Word list configuration
User defined word lists files are the input for the password generator. Word list must have a language and a category.
Word lists are store in Cloud Firestore service.

# Password generation
Cloud Function are created and made avaiable a REST API calls.

# Frontend application
Based on the Streamlit framework the frontend was easy to write. The application is deploy in Cloud Run
