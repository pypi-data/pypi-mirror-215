# Health Universe Python Client

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/requests)

This Python package provides a simple way to interact with the healthuniverse.com API. Specifically, it allows you to add applications to HealthUniverse through a simple python interface.

# Installation

You can install the package via pip:
`pip install healthuniverse`

# Quick Start

```
from healthuniverse.client import HealthUniverseClient

client = HealthUniverseClient()
response_status, response_data = client.create_app(
    app_name='My App', 
    app_desc='An awesome app', 
    app_category='0', 
    app_sdk='SL', 
    gh_account='<github_account>', 
    gh_repo='<github_repo>', 
    main_file='main.py'
    )

```

# Documentation

## HealthUniverseClient

`client = HealthUniverseClient(base_url='https://healthuniverse.com/')`

This creates a new HealthUniverse client. The base_url parameter is optional and defaults to 'https://healthuniverse.com/'.

create_app

```
status, response = client.create_app(
    app_name, 
    app_desc, 
    app_category, 
    app_sdk, 
    gh_account, 
    gh_repo, 
    main_file)
```

This sends a POST request to the HealthUniverse API to add a new app. Returns the HTTP status code and the JSON response.

# Parameters:

- app_name (str): The name of the app.
- app_desc (str): The description of the app.
- app_category (str): The category of the app. (0-10)
- app_sdk (str): The SDK version used by the app: 'SL' or 'FA' are acceptable.
- gh_account (str): The GitHub account where the app's source code is hosted.
- gh_repo (str): The GitHub repository where the app's source code is hosted.
- main_file (str): The main file of the app in the repository.

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.