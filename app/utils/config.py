import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CLIENT_ID = os.getenv('CLIENT_ID')
    CLIENT_SECRET = os.getenv('CLIENT_SECRET')
    TENANT_ID = os.getenv('TENANT_ID')
    DATAVERSE_URL = os.getenv('DATAVERSE_URL')
    TARGET_ACCOUNT_ID = os.getenv('TARGET_ACCOUNT_ID')
    
    # Azure OpenAI Configuration
    GPT_MODEL = os.getenv('GPT_MODEL', 'gpt-4.1')
    
    # Humana Portal Configuration
    HUMANA_LINK = os.getenv('HUMANA_LINK')
    HUMANA_USERNAME = os.getenv('HUMANA_USERNAME')
    HUMANA_PASSWORD = os.getenv('HUMANA_PASSWORD')
    
    # Tracker Agent Configuration
    HUMANA_ID_FOR_TRACKING = os.getenv('HUMANA_ID_FOR_TRACKING')
    HUMANA_TRACKER_INTERVAL = int(os.getenv('HUMANA_TRACKER_INTERVAL', 10))
    
    # Default Values for Missing Data
    DEFAULT_MISSING_VALUE = os.getenv('DEFAULT_MISSING_VALUE')
    DEFAULT_DATE_VALUE = os.getenv('DEFAULT_DATE_VALUE')
    
    # File Upload Configuration
    IMAGE_PATH = os.getenv('IMAGE_PATH')
    PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'temp', 'short-stories-for-children.pdf')
    DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')
    
    @classmethod
    def validate(cls):
        required_vars = ['CLIENT_ID', 'CLIENT_SECRET', 'TENANT_ID', 'DATAVERSE_URL', 'TARGET_ACCOUNT_ID']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            raise ValueError(f"Missing: {', '.join(missing_vars)}")
        return True
