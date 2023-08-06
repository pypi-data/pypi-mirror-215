from azure.storage.queue import QueueServiceClient
from azure.identity import ClientSecretCredential
import requests
from typing import List
import json
from html.parser import HTMLParser  # web scraping html

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.cdc_tech_environment_service import (
    environment_file as pade_env_file
)


class GitHubSecret:

    @staticmethod
    def get_github_secret(gh_access_token, gh_owner_name, gh_repository_name, gh_secret_name):
        """
        Retrieves a secret value from a GitHub repository using the GitHub API.

        Args:
            gh_access_token (str): The GitHub personal access token with appropriate permissions.
            gh_owner_name (str): The owner or organization name of the GitHub repository.
            gh_repository_name (str): The name of the GitHub repository.
            gh_secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret.

        Raises:
            requests.exceptions.RequestException: If an error occurs while making the API request.
            KeyError: If the secret value is not found in the API response.

        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_github_secret"):

            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {gh_access_token}"
            }

            api_url = f"https://api.github.com/repos/{gh_owner_name}/{gh_repository_name}/actions/secrets/{gh_secret_name}"

            print(f"api_url:{str(api_url)}")
            headers_redacted = str(headers).replace(
                gh_access_token, "[bearer REDACTED]")
            print(f"headers:{headers_redacted}")

            try:
                response_text = str(response.text)
                data = json.loads(response_text)
                msg = f"Received credentials with length : {len(str(response_text))} when posting to : "
                msg = msg + "{url}"
                response = requests.get(api_url, headers=headers)
                response_json = response.json()

                status_code = response.status_code
                # Try to get the content of the response in JSON format, if not possible return it as text
                try:
                    response_content = response.json()
                except ValueError:
                    response_content = response.text
                    status_code = 500

                logger.info(f"response_content: {response_content}")

                secret_value = response_json.get(
                    "secret", {}).get("value", None)

                if secret_value is not None:
                    print(f"Secret Value: {secret_value}")
                else:
                    response_content = response.json()
                    status_code = 500

            except Exception as exception_object:
                f_filter = HTMLFilter()
                f_filter.feed(response.text)
                response_text = f_filter.text
                msg = f"- response : error - {exception_object}"
                msg = msg + \
                    f"Error converting response text:{response_text} to json"
                response_content = msg
                status_code = 500

            return status_code, response_content, api_url


class HTMLFilter(HTMLParser):
    """Parses HTMLData

    Args:
        HTMLParser (_type_): _description_
    """

    text = ""

    def handle_data(self, data):
        """Parses HTMLData

        Args:
            data (_type_): _description_
        """
        self.text += data
