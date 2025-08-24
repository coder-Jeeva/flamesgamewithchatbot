import os
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

# 1. Define your service principal credentials
TENANT_ID ="fake_tenant_id"
CLIENT_ID = "fake_client_id"
CLIENT_SECRET ="fake_client_secret" 

# 2. Key Vault URL
KEYVAULT_URL="fake_keyvault_url"

# 3. Authenticate using ClientSecretCredential
credential = ClientSecretCredential(
    tenant_id=TENANT_ID,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

# 4. Create the SecretClient
client = SecretClient(vault_url=KEYVAULT_URL, credential=credential)

# 5. Function to fetch a secret
def get_secret(name: str) -> str:
    try:
        return client.get_secret(name).value
    except Exception as e:
        print(f"Error retrieving secret {name}: {e}")
        return None

# 6. Fetch your secrets
# DIRECT_LINE_SECRET = get_secret("DIRECT-LINE-SECRET")
AZURE_OPENAI_API_KEY = get_secret("AZURE-OPENAI-API-KEY")
AZURE_OPENAI_ENDPOINT = get_secret("AZURE-OPENAI-ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = get_secret("AZURE-OPENAI-DEPLOYMENT")
CHAT_COMPLETION_NAME = get_secret("CHAT-COMPLETION-NAME")
