import random
import os
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient

credential = AzureCliCredential()

subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
# subscription_id = 'f4c81b7b-69e0-4649-a892-7bc659153e3a'

RESOURCE_GROUP_NAME = 'DataScience'
LOCATION = 'uksouth'

#Step 1: Provision the resource group (not needed)
# resource_client = ResourceManagementClient(credential, subscription_id)

# rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
#     {"location": LOCATION})

# print(f"Provisioned resource group {rg_result.name}")

#Step 2: Provision the App Service plan, which defines the underlying VM for the web app
SERVICE_PLAN_NAME = 'PythonAzureExample-WebApp-plan'
WEB_APP_NAME = os.environ.get("WEB_APP_NAME", f"PythonAzureExample-WebApp-{random.randint(1,100000):05}")
# WEB_APP_NAME = 'PythonAzureExample-WebApp-52961'

#obtain client object
app_service_client = WebSiteManagementClient(credential, subscription_id)

# provision the plan; linux is the default
poller = app_service_client.app_service_plans.begin_create_or_update(RESOURCE_GROUP_NAME, 
    SERVICE_PLAN_NAME,
    {
        "location": LOCATION,
        "reserved": True,
        "sku": {"name": "B1"}
    }
)

plan_result = poller.result()

print(f"Provisioned App Service plan {plan_result.name}")

#Step 3: with the plan in place, provision the web app itself, which is the process that can host whatever code we want to deploy to it.
poller = app_service_client.web_apps.begin_create_or_update(RESOURCE_GROUP_NAME,
    WEB_APP_NAME,
    {
        "location": LOCATION,
        "server_farm_id": plan_result.id,
        "site_config": {
            "linux_fx_version": "python|3.8"
        }
    }
)

web_app_result = poller.result()

print(f"Provisioned web app {web_app_result.name} at {web_app_result.default_host_name}")

#Step 4: deploy code from a GitHub repository. For Python code, App Service on Linux runs
#the code inside a container that makes certain assumptions about the structure of the code.
#For more information, see How to configure Python apps,
#https://docs.microsoft.com/azure/app-service/containers/how-to-configure-python
#
#The create_or_update_source_control method doesn't provision a web app. It only sets the
#source control configuration for the app. In this case we're simply pointing to
#a GitHub repository

REPO_URL = os.environ["REPO_URL"]
# REPO_URL = 'https://github.com/jsnake789/storage-blob-upload-from-webapp'

poller = app_service_client.web_apps.begin_create_or_update_source_control(RESOURCE_GROUP_NAME,
    WEB_APP_NAME,
    {
        "kind": "GitHub",
        "repo_url": REPO_URL,
        "branch": "master"
    })

sc_result = poller.result()

print(f"Set source control on web app to {sc_result.branch} branch of {sc_result.repo_url}")