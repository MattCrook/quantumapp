import http.client
import requests as req

def get_management_api_config(domain):
    conn = http.client.HTTPSConnection(domain)
    payload = "{\"client_id\":\"rXCAbUgNjWCbflgAiUU97Uux1eiXUNZu\",\"client_secret\":\"Xttgkp1Z99NSFJow7Jp2_RNO_MixGlGnwtJhY821KQ7MpVy9DslCddEb_uQamsu7\",\"audience\":\"https://dev-405n1e6w.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_open_id_config(token):
    conn = http.client.HTTPConnection("https://dev-405n1e6w.auth0.com/.well-known/openid-configuration")
    headers = { 'authorization': f'Bearer {token}'}
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_management_api_user_logs(domain, token):
    conn = http.client.HTTPConnection(domain + "/logs")
    headers = { 'authorization': f'Bearer {token}'}
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")


def get_management_api_connections(domain, token):
    conn = http.client.HTTPConnection(domain + "/connections")
    headers = { 'authorization': f'Bearer {token}'}
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_management_api_grants(domain, token):
    conn = http.client.HTTPConnection(domain + "/grants")
    headers = { 'authorization': f'Bearer {token}'}
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# def get_management_api_user(domain, token, uid):
#     conn = http.client.HTTPConnection(domain + "/users/" + uid )
#     headers = { 'authorization': f'Bearer {token}'}
#     conn.request("GET", "/", headers=headers)
#     res = conn.getresponse()
#     data = res.read()
#     return data.decode("utf-8")

def get_management_api_user(domain, bearer_token, uid):
    URL = "https://" + domain + "/api/v2/users/" + uid
    PARAMS = {'Authorization': 'Bearer ' + bearer_token}
    r = req.get(url=URL, params=PARAMS)
    data = r.json()
    return data

def get_management_api_user_logs(domain, token, uid):
    conn = http.client.HTTPConnection(domain + "/users/" + uid + "/logs")
    headers = { 'authorization': f'Bearer {token}'}
    conn.request("GET", "/", headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_management_api_config(domain):
    conn = http.client.HTTPSConnection(domain)
    payload = "{\"client_id\":\"rXCAbUgNjWCbflgAiUU97Uux1eiXUNZu\",\"client_secret\":\"Xttgkp1Z99NSFJow7Jp2_RNO_MixGlGnwtJhY821KQ7MpVy9DslCddEb_uQamsu7\",\"audience\":\"https://dev-405n1e6w.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")
