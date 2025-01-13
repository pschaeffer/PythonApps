from   HDLmAwsUtility import *
import datetime
import json
import requests
import time    

# Use the Admin API
def adminAPI(userStr, passStr, storeStr, typeStr):
  responseTextStr = None
  headers = { 'Content-type': 'application/json'}
  # Build the request string
  reqStr = 'https://{}:{}@{}.myshopify.com/admin/{}.json'.format(userStr, passStr, storeStr, typeStr)
  # Code for obtaining a specific event by id
  # reqStr = 'https://{}:{}@{}.myshopify.com/admin/{}/11092713635953.json'.format(userStr, passStr, storeStr, typeStr)
  response = requests.get(reqStr, headers=headers)
  responseRequestCode = response.status_code
  if responseRequestCode == 200:
    responseTextStr = response.text
  return responseRequestCode, responseTextStr

# Use the Storefront API
def storeAPI(storeStr, tokStr):
  responseTextStr = None
  data = '{ shop { collections(first: 5) { edges { node { id handle } } pageInfo { hasNextPage } } } }'
  data = '{ shop { name primaryDomain { url host } } }'
  headerKeyStr = 'X-Shopify-Storefront-Access-Token'  
  headers = { 'Content-type': 'application/graphql', \
              headerKeyStr  : tokStr}
  # Build the request string
  resStr = 'https://{}.myshopify.com/api/graphql'.format(storeStr)
  response = requests.post(resStr, headers=headers, data=data)
  responseRequestCode = response.status_code
  if responseRequestCode == 200:
    responseTextStr = response.text
  return responseRequestCode, responseTextStr
    
# Main program 
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Start the AWS secrets manager code
  secretsClient = HDLmAwsUtility.buildAwsSecretsManagerClient()
  # Test code
  data = '{"text":"Hello, World!"}'
  storeStr = 'hdlm1'
  # TempApp1 userid and password
  useridStr1 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString1')
  passwordStr1 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString1')
  # TempApp2a userid and password (private app)
  useridStr2a = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString2a')
  passwordStr2a = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString2a')
  sharedSecretStr2a = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1SharedSecetString2a')
  storeFrontTokenStr2a = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1StoreFrontTokenString2a')
  # TempApp2b userid and password
  useridStr2b = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString2b')
  passwordStr2b = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString2b')
  # TempApp3 userid and password
  useridStr3 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString3')
  passwordStr3 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString3')
  # TempApp4 userid and password
  useridStr4 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString4')
  passwordStr4 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString4')
  # TempApp5 userid and password (private app) 
  useridStr5 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1UseridString5') 
  passwordStr5 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1PasswordString5')
  sharedSecretStr5 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1SharedSecetString5')
  storeFrontTokenStr5 = HDLmAwsUtility.getJustSecretFromAws(secretsClient, 'ShopifyHdlm1StoreFrontTokenString5')
  # Set the request type
  reqTypeStr = 'orders'
  reqTypeStr = 'products'
  reqTypeStr = 'shop'
  reqTypeStr = 'events'
  reqTypeStr = 'webhooks'
  # Run the Admin API request
  if 1 == 1:
    responseRequestCode, responseTextStr = adminAPI(useridStr5, passwordStr5, storeStr, reqTypeStr)
    if responseRequestCode == 200:
      jsonObj = json.loads(responseTextStr)
      print(json.dumps(jsonObj, indent=2, sort_keys=True))
  # Run the Storefront API request
  if 1 == 2:
    responseRequestCode, responseTextStr = storeAPI(storeStr, storeFrontTokenStr2a)
    if responseRequestCode == 200:
      jsonObj = json.loads(responseTextStr)
      print(json.dumps(jsonObj, indent=2, sort_keys=True))
  # Collect some ending time values  
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  printTimeEnd = datetime.datetime.now()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()