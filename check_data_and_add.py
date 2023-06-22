import time
import boto3
import json
import re
from config import XRD_LIMIT,PROJECT_WALLET_ADDRESS
from sale import send_radix, send_junger_token,check_tx_hash
from config import ACCESS_KEY_ID,SECRET_ACCESS_KEY,BUCKET_NAME,METADATA_FILE_KEY


s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
response = s3_client.get_object(Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)
existing_json = json.loads(response['Body'].read())
data_json = existing_json['collection']

#check
async def check(info):
    with open("metadata.json") as file:
        digits = re.findall(r'\d+', info[5])
        i = 0
        numbers = [num.zfill(4) for num in digits]
        value = int(((float(XRD_LIMIT)* float(len(numbers)))/(float(info[3])))) #check once
        nums_to_send = []

    if info[0] == 'TransferTokens' and info[4] == 'xrd_rr1qy5wfsfh' and info[5] != '-' and value == 1:

        for num in numbers:
            i += 1
            found = False
            for item in data_json:
                if item["ID"] == num:
                    found = True
                    if item["owner"] == "available":
                        nums_to_send.append(num)
                        # idf = item["ID"]
                        # print(f"New owner for NFT ID - {idf}")
                        # item["owner"] = info[1] #checks transaction status and add it
                        # message = f"Yours NFT with ID {num} "
                        # send_junger_token(info[1], message)

                    else:
                        message = f"NFT with ID {num} already owned"
                        print(message) #remove it
                        await send_radix(info[1], message,float(XRD_LIMIT)) #we need to add check_tx_hash()  #use try catch
                        # time.sleep(5)
            if not found:
                message = f"NFT with ID {num} not found, Try buying Another"
                print(message) #remove it
                await send_radix(info[1], message, float(info[3]))  #we need to add check_tx_hash()
                # time.sleep(5)

        if len(nums_to_send) > 0:
            nums_str = ", ".join(nums_to_send)
            message  =  f"Yours NFT(s) with ID(s) {nums_str}"
            tx_hash = await send_junger_token(info[1], message, int(len(nums_to_send))) # we need to send only len of available nfts 2/3
            print('tx_hash------',tx_hash)
            time.sleep(5)
            status = await check_tx_hash(tx_hash, PROJECT_WALLET_ADDRESS, int(len(nums_to_send))) #use try catch
            print('status------',status)
            if status:
                for nftItem in nums_to_send:
                    for item in data_json:
                        if item['ID'] == nftItem and item['owner'] == "available":
                            item["owner"] = info[1]
            else:
                nums_str = ", ".join(nums_to_send)
                message  =  f"Yours NFT(s) with ID(s) failed {nums_str} please try after sometime"
                refund_xrd_amount = len(nums_to_send) * XRD_LIMIT
                print('refund XRD============>',refund_xrd_amount) #check getting issue when 1/2 i.e 1 owned out 2. another not owned
                await send_radix(info[1], message, refund_xrd_amount)
                # time.sleep(5)

        s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)

    else:
        await send_radix(info[1], "Please check instructions and again send exact XRD",float(info[3]))
        time.sleep(5)
        print("its not TransferTokens or token not xrd or message = null or not sent exact amount ")


#check 1/2 or 2/3 check tx is getting failed