# firestore_upload.py

from google.cloud import firestore
import pandas as pd

def cargue_empresas():
    # Explicitly set the project ID
    db = firestore.Client(project="inversionpyp-7db7c")

    # Define the Firestore collection reference
    collection_ref = db.collection('empresas')

    # Read data from Excel file
    df = pd.read_excel('EMPRESAS.xlsx')

    # Convert DataFrame to dictionary with string keys
    data_dict = df.to_dict(orient='records')

    # Upload data to Firestore
    for data in data_dict:
        # Add a new document with an auto-generated ID
        collection_ref.add(data)

def consulta_empresas():
    db = firestore.Client(project="inversionpyp-7db7c")
    collection_ref = db.collection('empresas')
    documents = collection_ref.stream()

    # Create an empty list to store the data
    data_list = []

    # Iterate through the documents and extract data
    for doc in documents:
        data = doc.to_dict()
        data_list.append(data)

    # Convert the list of dictionaries to a Pandas DataFrame
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    cargue_empresas()