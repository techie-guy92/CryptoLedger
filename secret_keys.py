import boto3
import json
from botocore.exceptions import ClientError


REGION = 'me-central-1'  
SECRET_NAME = 'crypto-ledger-secrets'

secret_data = {
    "SECRET_KEY": "django-insecure-66li=*ryr3vk$7*bv5b9ym!uk+a827=qmi%*4=fsl5(0ts4&@v",
    "DB_PASSWORD": "Soheil0014",
    "EMAIL_HOST_PASSWORD": "wlkh cxlm jrsj eiel"
}

# Initialize Secrets Manager client
client = boto3.client('secretsmanager', region_name=REGION)

try:
    # Try to create the secret
    response = client.create_secret(
        Name=SECRET_NAME,
        SecretString=json.dumps(secret_data),
        Tags=[
            {'Key': 'project', 'Value': 'crypto_ledger'},
            {'Key': 'env', 'Value': 'production'}
        ]
    )
    print(f"Secret created: {response['ARN']}")

except ClientError as error:
    if e.response['Error']['Code'] == 'ResourceExistsException':
        # If secret already exists, update it
        update_response = client.put_secret_value(
            SecretId=SECRET_NAME,
            SecretString=json.dumps(secret_data)
        )
        print("Secret updated.")
    else:
        print(f"Error: {error}")
        raise  