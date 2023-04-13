#!/usr/bin/env python3

#
# Imports
#
import sys
try:
    import requests
except ImportError as ie:
    print(ie)
    # python3 -m pip install requests
    sys.exit("Please install python-requests!")
try:
    import urllib3
except ImportError as ie:
    print(ie)
    # This comes as dependency of requests, so should always be there.
    # python3 -m pip install urllib3
    sys.exit("Please install urllib3!")
import argparse
import json

def authenticate(username, password, url, check_certs):
    auth_header = {
        "Username": username, 
        "Password": password
    }
    login_resp = requests.get(url + "/partner-api/v1/authenticate", headers=auth_header, verify=check_certs)
    if login_resp.status_code != 200:
        sys.exit(f"Invalid API access credentials! Status: {login_resp.status_code}")
    return login_resp.json()

def sanitise_input_data(input_data):
    input_data = input_data.replace(" ", "")
    input_data = input_data.replace("%", "")
    input_data = input_data.replace("&", "")
    input_data = input_data.replace("*", "")
    input_data = input_data.replace("/", "")
    if len(input_data.split(",")) > 500:
        sys.exit("ERROR: API endpoint only allows queries up to 500 elements!")
    if len(input_data.encode("utf-8")) > 31930:
        sys.exit("ERROR: API endpoint only accepts queries up to 32KB!")
    return input_data

def products(url, authorization, check_certs, products_query):
    products_resp = requests.get(url + "/partner-api/v1/products/" + products_query, headers=authorization, verify=check_certs)
    if products_resp.status_code != 200:
        sys.exit(f"Invalid API query! Status: {products_resp.status_code}")
    return products_resp.json()

def assets(url, authorization, check_certs, assets_query):
    assets_resp = requests.get(url + "/partner-api/v1/assets/" + assets_query, headers=authorization, verify=check_certs)
    if assets_resp.status_code != 200:
        sys.exit(f"Invalid API query! Status: {assets_resp.status_code}")
    return assets_resp.json()

def main():
    print("Alcatel-Lucent Enterprise MyPortal API helper by Benny Eggerstedt (2023)")

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--assets", help="The assets you want to query e.g. \"SERIALNUMBER1,SERIALNUMBER1\"", required=False)
    parser.add_argument("-p", "--products", help="The products you want to query e.g. \"OS6860N-P48M-EU,OS6465-P6-EU\"", required=False)
    parser.add_argument("-k", "--insecure", action="store_true", help="If specified the HTTPS/TLS certificate will NOT be validated", required=False)
    parser.add_argument("-u", "--url", help="If specified uses this URL, otherwise uses the default: integration.al-enterprise.com", required=False)
    args = parser.parse_args()

    # If TLS certificates should be ignored or use default "True"
    if args.insecure:
        check_certs = False
        # Ignore self-signed certificate warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    else:
        check_certs = True
    
    # Import secrets (MyPortal API authentication details)
    try:
        from mysecrets import secrets
    except ModuleNotFoundError:
        sys.exit("You need to set up mysecrets.py with your Alcatel-Lucent Enterprise MyPortal API username/password!")

    # Sanitise/Set URL endpoint
    if args.url:
        if args.url.startswith("https://"):
            url = args.url.rstrip("/")
        elif args.url.startswith("http://"):
            sys.exit("ERROR: This API only supports HTTPS!")
        else:
            url = "https://" + args.url.rstrip("/")
    else:
        url = "https://integration.al-enterprise.com"
    
    print("Using MyPortal API URL: " + url)

    if not (args.assets or args.products):
        sys.exit("ERROR: Input required either for --assets, --products or both!")

    # Login to API
    auth_token = authenticate(secrets["username"], secrets["password"], url, check_certs)

    # Build Authorization header
    authorization = {
        "Authorization": auth_token["token"]
    }

    # Query product details
    # args.products MUST be in format OS6860N-P48M-EU,OS6465-P6-EU
    # - No extra whitespace(s)
    # - No wildcard characters (*, %) and no ampersand (&)
    if args.products:
        products_query = sanitise_input_data(args.products)
        print(f"Performing products query for: {products_query}")
        products_details = products(url, authorization, check_certs, products_query)
        print(json.dumps(products_details, indent=4))

    # Query asset details
    # args.assets MUST be in format SERIALNUMBER1,SERIALNUMBER2
    # - No extra whitespace(s)
    # - No wildcard characters (*, %) and no ampersand (&)
    if args.assets:
        assets_query = sanitise_input_data(args.assets)
        print(f"Performing assets query for: {assets_query}")
        assets_details = assets(url, authorization, check_certs, assets_query)
        print(json.dumps(assets_details, indent=4))

if __name__ == "__main__":
    main()
