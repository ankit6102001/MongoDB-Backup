# MongoDB Backup with Streamlit

A simple web tool built with **Streamlit** that helps you perform backups of MongoDB databases. The tool connects to a MongoDB database (localhost, SRV, or manual connection), backs up all collections in the database, and allows you to download the backup as a `.tar.gz` file. It also provides a preview of the collections and allows you to select individual collections to preview the data.

## Features

- **Backup MongoDB Database**: Back up all collections within the selected database.
- **Preview MongoDB Collections**: View a preview of documents in any collection.
- **Download Backup**: Download the backup as a `.tar.gz` file after completion.
- **Connection Support**: Supports `localhost`, `srv`, and `manual` MongoDB connection formats.

## Installation

To set up the project locally, follow these steps:

1. **Clone the Repository**:

    git clone https://github.com/yourusername/mongodb-backup-tool.git
    cd mongodb-backup-tool


2. **Create and Activate a Virtual Environment**:

    - For **Windows**:
      python -m venv venv
      .\venv\Scripts\activate

    - For **Linux/Mac**:
      python3 -m venv venv
      source venv/bin/activate

3. **Install Dependencies**:

    Use `requirements.txt` to install all the required libraries:

    pip install -r requirements.txt


## Usage

1. After installing the dependencies, run the Streamlit app:

    streamlit run app.py

2. The app will be accessible at `http://localhost:8501/` in your browser.

3. **Provide Connection Details**:
   - Choose the connection type: `localhost`, `srv`, or `manual`.
   - Enter the appropriate MongoDB connection string or host/port details.
   
4. **Perform Backup**:
   - Click **Run Backup** to start backing up the selected database and its collections.

5. **Download Backup**:
   - After the backup is complete, a **Download Backup** button will appear to download the `.tar.gz` backup file.

6. **Preview Collections**:
   - Once connected, you can select any collection from the dropdown to preview the first 5 documents.



