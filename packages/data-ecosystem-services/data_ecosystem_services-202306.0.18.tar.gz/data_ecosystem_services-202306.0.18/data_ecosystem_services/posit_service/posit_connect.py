from azure.storage.queue import QueueServiceClient
from azure.identity import ClientSecretCredential
import requests

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

class PositConnect:
    
    
@staticmethod
def verify_api_key(api_key, url):
    """
    Verifies the validity of an API key by making a request to a specified URL.

    Args:
        api_key (str): The API key to be verified.
        url (str): The URL of the API endpoint to which the request will be sent.
        
    Examples:
        url: 'https://dev.rconnect.edav.cdc.gov:8080"'  # replace with the actual API endpoint
        
    Returns:
        tuple: A tuple containing the status code and response_content from the server.
    """
    
    import requests

    headers = {
        'Authorization': 'Bearer ' + api_key,
    }

    response = requests.get(url, headers=headers)

    # If the request was successful, status_code will be 200
    status_code = response.status_code
    
    # If the request was successful, status_code will be 200
    print(response.status_code)

    # This will print the content of the response
    print(response.json())
    
     # Try to get the content of the response in JSON format, if not possible return it as text
    try:
        response_content = response.json()
    except ValueError:
        response_content = response.text

    return status_code, response_content
 