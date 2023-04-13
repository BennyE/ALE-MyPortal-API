# ALE-MyPortal-API

This script allows you to interact with the Alcatel-Lucent Enterprise MyPortal API for the Service & Asset Manager, initially limited to the capability that the ProActive Lifecycle Management (PALM) API provided.
You'll need a username/password specifically enabled for MyPortal API access, contact your Alcatel-Lucent Enterprise Channel Sales Manager for details.

## Usage (-h)

```
$ % python3 ale-myportal-api.py -h                                                                             
Alcatel-Lucent Enterprise MyPortal API helper by Benny Eggerstedt (2023)
usage: ale-myportal-api.py [-h] [-a ASSETS] [-p PRODUCTS] [-k] [-u URL]

options:
  -h, --help            show this help message and exit
  -a ASSETS, --assets ASSETS
                        The assets you want to query e.g. "SERIALNUMBER1,SERIALNUMBER1"
  -p PRODUCTS, --products PRODUCTS
                        The products you want to query e.g. "OS6860N-P48M-EU,OS6465-P6-EU"
  -k, --insecure        If specified the HTTPS/TLS certificate will NOT be validated
  -u URL, --url URL     If specified uses this URL, otherwise uses the default: integration.al-enterprise.com
```

## Example

```
$ % python3 ale-myportal-api.py -a EXAMPLE-SN1 -p OS6860N-P48M-EU,OS6465-P6-EU
Alcatel-Lucent Enterprise MyPortal API helper by Benny Eggerstedt (2023)
Using MyPortal API URL: https://integration.al-enterprise.com
Performing products query for: OS6860N-P48M-EU,OS6465-P6-EU
[
    {
        "productReference": "OS6465-P6-EU",
        "productDescription": "OS6465-P6 Switch,75W AC PSU and EU Cord",
        "family": "OS6465",
        "productLine": "Network Products"
    },
    {
        "productReference": "OS6860N-P48M-EU",
        "productDescription": "OS6860N-P48M switch,920W AC PSU,EU Cord",
        "family": "OS6860/E",
        "productLine": "Network Products"
    }
]
Performing assets query for: EXAMPLE-SN1
[
    {
        "assetReference": "EXAMPLE-SN1",
        "soldTo": "EXAMPLEsoldTo12345",
        "salesOrderDate": "2020-09-23",
        "shippingDate": "2020-10-07",
        "salesOrder": "EXAMPLEsalesOrder12345",
        "partNumber": "903778-90",
        "description": "OS6450-P24",
        "productLine": "Network Services",
        "isMaster": "Yes",
        "productReference": "903778-90",
        "productDescription": "OS6450-P24",
        "purchaseOrder": "EXAMPLEpurchaseOrder12345",
        "currentSubscriptionStatus": "None",
        "latestSubscriptionStatus": "None",
        "endUserCompanyName": "End-Customer Detail 123",
        "managingPartner": "End User Asset Company 28",
        "accountName": "End User Asset Company 28",
        "status": "Active"
    }
]
```
