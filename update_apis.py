#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth

print('hello world')
token_url = 'https://localhost:9443/oauth2/token'
api_url = 'https://localhost:9443/api/am/publisher/v0.11'
get_apis_context = '/apis'
username = 'admin'
password = 'admin'
apim_view_scope = 'apim:api_view'
apim_create_scope = 'apim:api_create'
client_id = 'zBEN3SnAhk5h0hpOaxUfo7ST5Uwa'
client_secret = 'glab_keJZ1VEWWtxzeI0KIm7chka'
new_endpoint_config = {
    "suspendDuration": "1000",
    "suspendMaxDuration": "5000",
    "factor": "1",
    "retryErroCode": "101504",
    "retryTimeOut": "3",
    "retryDelay": "1000",
    "actionSelect": "fault",
    "actionDuration": "12345"
}


def get_access_token(scope):
    token_req = {'grant_type': 'password', 'username': username, 'password': password,
                 'scope': scope}
    resp = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=token_req,
                         verify=False)

    if resp.status_code == 200:
        print('Token is ready for API retrieval')
        return resp.json()["access_token"]
    else:
        print('Error while retrieving the access token')
        return None


def update_api(api_id, resp):
    access_token = get_access_token(apim_create_scope)
    update_payload = resp
    resp = requests.put(api_url + get_apis_context + '/' + api_id, data=update_payload, verify=False,
                        headers={'Authorization': 'Bearer ' + access_token})
    if resp.status_code == 401:
        # handling the case where token is expired after token call, try with new token
        access_token = get_access_token(apim_create_scope)
        resp = requests.put(api_url + get_apis_context + '/' + api_id, data=update_payload, verify=False,
                            headers={'Authorization': 'Bearer ' + access_token})
    if resp.status_code == 200:
        print('API updated successfully')

access_token = get_access_token(apim_view_scope)
if (access_token is not None):
    print('Token is ready for API retrieval')
    resp = requests.get(api_url + get_apis_context, verify=False,
                        headers={'Authorization': 'Bearer ' + access_token})

    if resp.status_code == 401:
        # handling the case where token is expired after token call, try with new token
        access_token = get_access_token(apim_view_scope)
        resp = requests.get(api_url + get_apis_context, verify=False,
                            headers={'Authorization': 'Bearer ' + access_token})
    if resp.status_code == 200:
        for api in resp.json()["list"]:
            resp = requests.get(api_url + get_apis_context + '/' + api["id"], verify=False,
                                headers={'Authorization': 'Bearer ' + access_token})
            returned_endpoint_config = resp.json()["endpointConfig"]
            print(returned_endpoint_config["production_endpoints"])
            update_api(api["id"], resp)
