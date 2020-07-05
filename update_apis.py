#!/usr/bin/env python3
import json
import requests
from requests.auth import HTTPBasicAuth

token_url = 'https://localhost:9443/oauth2/token'
api_url = 'https://localhost:9443/api/am/publisher/v0.11'
username = 'admin'
password = 'admin'
client_id = 'zBEN3SnAhk5h0hpOaxUfo7ST5Uwa'
client_secret = 'glab_keJZ1VEWWtxzeI0KIm7chka'
new_endpoint_config = {"suspendErrorCode": "101504", "suspendDuration": "1000",
                       "suspendMaxDuration": "5000", "factor": "2",
                       "retryErroCode": ["101504", "101505"], "retryTimeOut": "3",
                       "retryDelay": "1000", "actionSelect": "fault", "actionDuration": "909090"}

get_apis_context = '/apis'
apim_view_scope = 'apim:api_view'
apim_create_scope = 'apim:api_create'

def get_access_token(scope):
    token_req = {'grant_type': 'password', 'username': username, 'password': password,
                 'scope': scope}
    resp = requests.post(token_url, auth=HTTPBasicAuth(client_id, client_secret), data=token_req,
                         verify=False)
    if resp.status_code == 200:
        print('[INFO] A token retrieved')
        return resp.json()["access_token"]
    else:
        print('[ERROR] Error while retrieving the access token')
        return None

def update_api(api_id, api_update_payload):
    updated_payload = api_update_payload.json();
    returned_endpoint_config = updated_payload["endpointConfig"]
    ep_config = json.loads(returned_endpoint_config)
    ep_config["production_endpoints"]["config"] = new_endpoint_config
    updated_payload["endpointConfig"] = json.dumps(ep_config)

    access_token = get_access_token(apim_create_scope)
    if (access_token is not None):

        resp = requests.put(api_url + get_apis_context + '/' + api_id, data=json.dumps(updated_payload),
                                          verify=False,
                                          headers={'Authorization': 'Bearer ' + access_token,
                                     'Content-Type': 'application/json'})
        if resp.status_code == 401:
            # handling the case where token is expired after token call, try with new token
            access_token = get_access_token(apim_create_scope)
            resp = requests.put(api_url + get_apis_context + '/' + api_id, data=updated_payload,
                                              verify=False,
                                              headers={'Authorization': 'Bearer ' + access_token,
                                         'Content-Type': 'application/json'})
        if api_update_payload.status_code == 200:
            print('[INFO] API updated successfully')

    else:
        print('[ERROR] Not able to get access token for updating API')

def get_api(api_id):

    access_token = get_access_token(apim_view_scope)
    if (access_token is not None):
        resp = requests.get(api_url + get_apis_context + '/' + api_id, verify=False,
                            headers={'Authorization': 'Bearer ' + access_token})
        return resp
    else:
        return None

# getting api list and updaing one by one
access_token = get_access_token(apim_view_scope)
if (access_token is not None):
    print('[INFO] Token is ready for API retrieval')
    resp = requests.get(api_url + get_apis_context, verify=False,
                        headers={'Authorization': 'Bearer ' + access_token})

    if resp.status_code == 401:
        # handling the case where token is expired after token call, try with new token
        access_token = get_access_token(apim_view_scope)
        resp = requests.get(api_url + get_apis_context, verify=False,
                            headers={'Authorization': 'Bearer ' + access_token})
    if resp.status_code == 200:
        for api in resp.json()["list"]:
            resp = get_api(api["id"])
            if (resp is not None):
                update_api(api["id"], resp)
else:
    print('[ERROR] Not able to get access token for retrieving API list')
