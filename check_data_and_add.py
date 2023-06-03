import boto3
import json
import re
from config import XRD_LIMIT
from sale import send_radix, send_junger_token
from config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,BUCKET_NAME,METADATA_FILE_KEY


s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
response = s3_client.get_object(Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)
existing_json = json.loads(response['Body'].read())
data_json = existing_json['collection']

def check(info):
    with open("metadata.json") as file:
        digits = re.findall(r'\d+', info[5])
        i = 0
        numbers = [num.zfill(4) for num in digits]
        value = int(((float(XRD_LIMIT)* float(len(numbers)))/(float(info[3])))) 
        

    if info[0] == 'TransferTokens' and info[4] == 'xrd_rr1qy5wfsfh' and info[5] != '-' and value == 1:

        for num in numbers:
            i += 1
            found = False
            for item in data_json:
                if item["ID"] == num:
                    found = True
                    if item["owner"] == "available":
                        idf = item["ID"]
                        print(f"New owner for NFT ID - {idf}")
                        item["owner"] = info[1] #checks transaction status and add it
                        message = f"Yours NFT with ID {num} "
                        send_junger_token(info[1], message)
                    else:
                        message = f"NFT with ID {num} already owned"
                        print(message)
                        send_radix(info[1], message,float(info[3]))
            if not found:
                message = f"NFT with ID {num} not found, Try buying Another"
                print(message)
                send_radix(info[1], message, float(info[3]))

        s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)

    else:
        send_radix(info[1], "Please check instructions and again send XRD",float(info[3]))
        print("its not TransferTokens or token not xrd or message = null or not sent exact amount ")
