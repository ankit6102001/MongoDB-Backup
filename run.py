import streamlit as st
from pymongo import MongoClient
import os
import datetime
import tarfile

def create_folder_backup(dbname):
    dt = datetime.datetime.now()
    directory = (f'backups/bk_{dbname}_{dt.month}-{dt.day}-{dt.year}__{dt.hour}_{dt.minute}')
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def run_backup(mongoUri, dbname):
    client = MongoClient(mongoUri)
    db = client[dbname]
    collections = db.list_collection_names()
    files_to_compress = []
    directory = create_folder_backup(dbname)
    
    for collection in collections:
        db_collection = db[collection]
        cursor = db_collection.find({})
        filename = (f'{directory}/{collection}.json')
        files_to_compress.append(filename)
        
        with open(filename, 'w') as file:
            file.write('[')
            first = True
            for document in cursor:
                if not first:
                    file.write(',')
                file.write(str(document))
                first = False
            file.write(']')

    output_filename = f'{directory}.tar.gz'
    make_tarfile(output_filename, files_to_compress)
    return output_filename

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        for filename in source_dir:
            tar.add(filename)
    
    return output_filename

def streamlit_ui():
    st.title("MongoDB Backup Tool")

    st.sidebar.header("Database Connection")
    connection_type = st.sidebar.selectbox("Connection Type", ["localhost", "srv", "manual"])

    mongoUri = ""
    dbname = ""
    
    if connection_type == "localhost":
        host = st.sidebar.text_input("Host", "localhost")
        port = st.sidebar.number_input("Port", min_value=1, max_value=65535, value=27017)
        dbname = st.sidebar.text_input("Database Name", "")
        mongoUri = f'mongodb://{host}:{port}/{dbname}'

    elif connection_type == "srv":
        mongoUri = st.sidebar.text_input("MongoDB URI (SRV Format)", "")
        dbname = mongoUri.split('/')[-1].split('?')[0] if "/" in mongoUri else ""

    elif connection_type == "manual":
        host = st.sidebar.text_input("Host", "localhost")
        port = st.sidebar.number_input("Port", min_value=1, max_value=65535, value=27017)
        dbname = st.sidebar.text_input("Database Name", "")
        username = st.sidebar.text_input("Username", "")
        password = st.sidebar.text_input("Password", type="password")
        mongoUri = f'mongodb://{username}:{password}@{host}:{port}/{dbname}'

    if mongoUri and dbname:
        if st.sidebar.button("Run Backup"):
            with st.spinner("Performing Backup..."):
                try:
                    backup_file = run_backup(mongoUri, dbname)
                    st.success("Backup Completed Successfully!")
                    with open(backup_file, "rb") as f:
                        st.download_button(
                            label="Download Backup",
                            data=f,
                            file_name=os.path.basename(backup_file),
                            mime="application/gzip"
                        )
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.stop()

        st.header("Collection Preview")
        client = MongoClient(mongoUri)
        db = client[dbname]
        collections = db.list_collection_names()
        
        selected_collection = st.selectbox("Select a Collection", collections)
        
        collection_data = db[selected_collection].find().limit(5)
        st.write(f"Preview of {selected_collection}:")
        for doc in collection_data:
            st.json(doc)

    else:
        st.error("Please provide a valid MongoDB connection string and database name.")

if __name__ == "__main__":
    streamlit_ui()
