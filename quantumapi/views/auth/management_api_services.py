import http.client
import requests as req
from quantumapp.settings import MANAGEMENT_API_PAYLOAD, MANAGEMENT_API_AUTHORIZATION_CODE

# For servers to directly request a token with the client credentials
def management_api_oath_endpoint(domain):
    conn = http.client.HTTPSConnection(domain)
    payload = MANAGEMENT_API_PAYLOAD
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# For web apps to exchange an authorization code for a token
def management_api_openid_authorization_codes(domain):
    conn = http.client.HTTPSConnection(domain)
    payload = MANAGEMENT_API_AUTHORIZATION_CODE
    headers = {'content-type': "application/json"}
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# def openid_connect_authorize_endpoint(domain):
#     conn = http.client.HTTPSConnection(domain)
#     payload = AUTHORIZATION_PAYLOAD
#     headers = {'content-type': "application/json"}
#     conn.request("GET", "/authorize", payload, headers)
#     res = conn.getresponse()
#     data = res.read()
#     return data.decode("utf-8")

def get_open_id_config(domain, token):
    URL = "https://" + domain + "/.well-known/openid-configuration"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_logs(domain, token):
    URL = "https://" + domain + "/api/v2/logs"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def retrieve_user_logs(domain, token, uid):
    URL = "https://" + domain + "/api/v2/users/" + uid + "/logs"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_connections(domain, token):
    URL = "https://" + domain + "/api/v2/connections"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_retrieve_connection(domain, token, id):
    URL = "https://" + domain + "/api/v2/connections/" + id
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_grants(domain, token):
    URL = "https://" + domain + "/api/v2/grants"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_client_grants(domain, token):
    URL = "https://" + domain + "/api/v2/client-grants"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def get_management_api_user(domain, bearer_token, uid):
    URL = "https://" + domain + "/api/v2/users/" + uid
    headers = {'authorization': 'Bearer ' + bearer_token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def jwks_endpoint(domain, token):
    URL = "https://" + domain + "/.well-known/jwks.json/"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def device_credentials(domain, token):
    URL = "https://" + domain + "/api/v2/device-credentials"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def resource_servers(domain, token):
    URL = "https://" + domain + "/api/v2/resource-servers"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def management_api_keys(domain, token):
    URL = "https://" + domain + "/api/v2/keys/signing"
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data

def management_api_retrieve_key(domain, token, kid):
    URL = "https://" + domain + "/api/v2/keys/signing/" + kid
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def user_info(token):
    URL = 'https://dev-405n1e6w.auth0.com/userinfo'
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def management_tenant_settings(domain, token):
    URL = "https://" + domain + '/api/v2/tenants/settings'
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data


def management_api_jobs(domain, token, job_id):
    URL = "https://" + domain + '/api/v2/jobs/' + job_id
    headers = {'authorization': 'Bearer ' + token}
    r = req.get(url=URL, headers=headers)
    data = r.json()
    return data
