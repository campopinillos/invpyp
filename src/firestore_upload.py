# firestore_upload.py
from google.cloud import firestore
import pandas as pd

def cargue_empresas(proj="inversionpyp-7db7c",collect='empresas'):
    # Explicitly set the project ID
    db = firestore.Client(project=proj)

    # Define the Firestore collection reference
    collection_ref = db.collection(collect)

    # Read data from Excel file
    df = pd.read_excel('EMPRESAS.xlsx')

    # Convert DataFrame to dictionary with string keys
    data_dict = df.to_dict(orient='records')

    # Upload data to Firestore
    for data in data_dict:
        # Add a new document with an auto-generated ID
        collection_ref.add(data)

def consulta_empresas(proj="inversionpyp-7db7c",collect='empresas'):
    db = firestore.Client(project=proj)
    collection_ref = db.collection(collect)
    documents = collection_ref.stream()

    # Create an empty list to store the data
    data_list = []

    # Iterate through the documents and extract data
    for doc in documents:
        data = doc.to_dict()
        data_list.append(data)

    # Convert the list of dictionaries to a Pandas DataFrame
    return pd.DataFrame(data_list)

def cargue(proj="inversionpyp-7db7c", collect='', df=pd.DataFrame()):
    # Explicitly set the project ID
    db = firestore.Client(project=proj)

    # Define the Firestore collection reference
    collection_ref = db.collection(collect)

    # Convert DataFrame to dictionary with string keys
    data_dict = df.to_dict(orient='records')

    # Upload data to Firestore
    for data in data_dict:
        # Add a new document with an auto-generated ID
        collection_ref.add(data)

def delete_collection(proj="inversionpyp-7db7c", collect='', batch_size=500):
    # Explicitly set the project ID
    db = firestore.Client(project=proj)
    collection_ref = db.collection(collect)
    deleted_count = 0

    while True:
        docs = collection_ref.limit(batch_size).stream()
        deleted_batch = 0

        for doc in docs:
            print(f'Deleting doc {doc.id} => {doc.to_dict()}')
            doc.reference.delete()
            deleted_batch += 1

        deleted_count += deleted_batch
        if deleted_batch < batch_size:
            break

    print(f'Total {deleted_count} documents deleted from {collect} collection.')

def base_final(proj="inversionpyp-7db7c"):
    delete_collection(proj="inversionpyp-7db7c", collect='resultado_pyp', batch_size=1500)
    db = firestore.Client(project=proj)
    empresas_collection = 'empresas'
    empresas_documents = empresas_collection.stream()
    empresas_datos = [doc.to_dict() for doc in documents]
    empresas = pd.DataFrame(empresas_datos)
    
    for colecc_ref in db.collections():
        if colecc_ref != empresas_collection:
            documents = colecc_ref.stream()
            datos = [doc.to_dict() for doc in documents]
            temp_df = pd.DataFrame(datos)
            df = empresas.merge(temp_df,
                                on=['Vigencia', 'Mes', 'Sucursal', 'Tipo Documento', 'No. Documento', 'Razón Social'],
                                how='left')

    # Define the Firestore collection reference
    collection_ref = db.collection("resultado_pyp")

    # Convert DataFrame to dictionary with string keys
    data_dict = df.to_dict(orient='records')

    # Upload data to Firestore
    for data in data_dict:
        # Add a new document with an auto-generated ID
        collection_ref.add(data)





if __name__ == "__main__":
    cargue_empresas()