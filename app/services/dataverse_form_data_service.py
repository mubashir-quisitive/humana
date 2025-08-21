import requests
from app.utils.config import Config
from app.utils.logger import logger

class DataverseFormDataService:
    def __init__(self):
        self.base_url = Config.DATAVERSE_URL
        self.client_id = Config.CLIENT_ID
        self.client_secret = Config.CLIENT_SECRET
        self.tenant_id = Config.TENANT_ID
        self.access_token = None
    
    def get_access_token(self):
        """Get OAuth access token from Azure AD"""
        if self.access_token:
            return self.access_token
            
        token_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': f'{self.base_url}/.default',
            'grant_type': 'client_credentials'
        }
        
        try:
            response = requests.post(token_url, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to get access token: {e}")
            raise
    
    def fetch_form_data_by_account_id(self, account_id=None):
        """Fetch form data by account ID from Dataverse"""
        if not account_id:
            account_id = Config.TARGET_ACCOUNT_ID
            
        try:
            token = self.get_access_token()
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # Fetch account details
            account_url = f"{self.base_url}/api/data/v9.2/accounts({account_id})"
            response = requests.get(account_url, headers=headers)
            response.raise_for_status()
            
            account_data = response.json()
            
            # Fetch related contacts
            contacts_url = f"{self.base_url}/api/data/v9.2/accounts({account_id})/contact_customer_accounts"
            contacts_response = requests.get(contacts_url, headers=headers)
            
            contacts_data = []
            if contacts_response.status_code == 200:
                contacts_data = contacts_response.json().get('value', [])
            
            # Combine account and contacts data
            combined_data = {
                'account': account_data,
                'contacts': contacts_data,
                'account_id': account_id
            }
            
            return combined_data
            
        except Exception as e:
            logger.error(f"Failed to fetch form data: {e}")
            return None
    
    def display_form_data(self, data):
        """Display form data information in a formatted way"""
        if not data:
            logger.error("No form data to display")
            return
            
        account = data.get('account', {})
        contacts = data.get('contacts', [])
        
        logger.info(f"Account Name: {account.get('name', 'N/A')}")
        logger.info(f"Account ID: {account.get('accountid', 'N/A')}")
        logger.info(f"Phone: {account.get('telephone1', 'N/A')}")
        logger.info(f"Email: {account.get('emailaddress1', 'N/A')}")
        logger.info(f"Address: {account.get('address1_city', 'N/A')}, {account.get('address1_stateorprovince', 'N/A')}")
        
        if contacts:
            logger.info(f"Number of Contacts: {len(contacts)}")
            for i, contact in enumerate(contacts[:3], 1):  # Show first 3 contacts
                logger.info(f"Contact {i}: {contact.get('firstname', '')} {contact.get('lastname', '')}")
        else:
            logger.info("No contacts found")
