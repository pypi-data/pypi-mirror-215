from google.cloud import bigquery
from google.oauth2 import service_account

class profileBQ():
    def __init__(self, gcp_key_path) : 
        self.gcp_key_path = gcp_key_path

    def set_up_connection_to_bq(self) : 
        bq_credentials = service_account.Credentials.from_service_account_file(
            self.gcp_key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        return bq_credentials