#!/usr/bin/python3
from google.cloud import firestore


def delete_after_confirm():
    # Project ID is determined by the GCLOUD_PROJECT environment variable
    db = firestore.Client()

    users_ref = db.collection(u'mkpasswd-wordlists')
    docs = users_ref.stream()

    print("Read docs:")
    for doc in docs:
        print(f"Found document: {doc.id}")
        i = 'n'
        i = input("Delete (Y)es/ (N)o/ (A)board? ").lower()
        if i == 'y':
            db.collection(u'mkpasswd-wordlists').document(doc.id).delete()
            print ("File deleted!")
        elif i == 'a':
            break
        else:
            print ("File skipped!")


if __name__ == "__main__":
    delete_after_confirm()
