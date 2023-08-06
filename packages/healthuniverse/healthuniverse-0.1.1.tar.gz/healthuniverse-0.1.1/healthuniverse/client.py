import requests
import json

class HealthUniverseClient:
    def __init__(self, api_key, base_url="http://healthuniverse.com/api/v1"):
        """
        Initializes a HealthUniverseClient.

        :param api_key: The API key provided by Health Universe.
        :param base_url: The base URL for the Health Universe API.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "application/json"
        }

    def create_app(self, app_data):
        """
        Creates a new app.

        :param app_data: A dictionary containing the app details.
        :returns: The server response as a JSON object.

        data = {
            "app_name": app_name,
            "app_desc": app_desc,
            "app_category": app_category,
            "app_sdk": app_sdk,
            "gh_account": gh_account,
            "gh_repo": gh_repo,
            "main_file": main_file
        }

        """
        response = requests.post(
            url=f'{self.base_url}/apps', 
            headers=self.headers, 
            data=json.dumps(app_data)
        )
        return response.json()

    def update_app(self, app_slug, app_data):
        """
        Updates an existing app.

        :param app_slug: The slug of the app to update.
        :param app_data: A dictionary containing the updated app details.
        :returns: The server response as a JSON object.
        """
        response = requests.put(
            url=f'{self.base_url}/apps/{app_slug}', 
            headers=self.headers, 
            data=json.dumps(app_data)
        )
        return response.json()

    def get_app(self, app_slug):
        """
        Retrieves an app's details.

        :param app_slug: The slug of the app to retrieve.
        :returns: The server response as a JSON object.
        """
        response = requests.get(
            url=f'{self.base_url}/apps/{app_slug}', 
            headers=self.headers
        )
        return response.json()

    def delete_app(self, app_slug):
        """
        Deletes an app.

        :param app_slug: The slug of the app to delete.
        :returns: The server response status code.
        """
        response = requests.delete(
            url=f'{self.base_url}/apps/{app_slug}', 
            headers=self.headers
        )
        return response.status_code

    def get_apps(self):
        """
        Retrieves all apps.

        :returns: The server response as a JSON object.
        """
        response = requests.get(
            url=f'{self.base_url}/apps', 
            headers=self.headers
        )
        return response.json()