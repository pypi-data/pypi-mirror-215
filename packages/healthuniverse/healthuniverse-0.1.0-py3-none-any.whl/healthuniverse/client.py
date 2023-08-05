import json
import requests

class HealthUniverseClient:
    def __init__(self, base_url='https://healthuniverse.com/'):
        self.base_url = base_url

    def add_app(self, app_name, app_desc, app_category, app_sdk, gh_account, gh_repo, main_file):
        url = self.base_url + 'add_app_json/'
        headers = {'Content-Type': 'application/json'}
        data = {
            "app_name": app_name,
            "app_desc": app_desc,
            "app_category": app_category,
            "app_sdk": app_sdk,
            "gh_account": gh_account,
            "gh_repo": gh_repo,
            "main_file": main_file
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        return response.status_code, response.json()