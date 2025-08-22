# Humana Form Filling Agent

FastAPI service with automated form filling and tracking agents.

## Setup

```bash
git clone https://github.com/mubashir-quisitive/humana.git
cd humana
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Environment

Create `.env` with:
```env
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_KEY=your_key
GPT_MODEL=gpt-4.1-mini

# Dataverse Configuration
CLIENT_ID=your_client_id
CLIENT_SECRET=your_secret
TENANT_ID=your_tenant
DATAVERSE_URL=your_dataverse_url
TARGET_ACCOUNT_ID=your_account_id

# Humana Portal Configuration
HUMANA_LINK=your_portal_url
HUMANA_USERNAME=your_username
HUMANA_PASSWORD=your_password

# Tracker Agent Configuration
HUMANA_ID_FOR_TRACKING=PA-130810002
HUMANA_TRACKER_INTERVAL=10

# Default Values for Missing Data
DEFAULT_MISSING_VALUE=Not Available
DEFAULT_DATE_VALUE=01/01/1999

# File Upload Configuration
PDF_PATH=C:\path\to\humana\temp
```

## Run

```bash
python main.py
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## Endpoints

- `POST /api/v1/form/submit-form` - Submit PA form