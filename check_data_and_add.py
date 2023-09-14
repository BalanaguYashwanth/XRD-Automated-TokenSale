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
AVAILABLE =  "available"



async def get_one_free(info, count):
    available_nft = []
    data_json.reverse()
    for item in data_json:
        if item['owner'] == AVAILABLE:
            if len(available_nft) < count:
                available_nft.append(item['ID'])
                item['owner'] = info[1]
            else:
                break
    data_json.reverse()
    if len(available_nft):
        total_nfts_str = ", ".join(available_nft)
        message  =  f"As per of BUY 1 GET 1, You're now purchased the Jungler NFT(s) with ID(s) {total_nfts_str}. Thank you for joining our mission to save the rainforest! Welcome to the community! "
        tx_hash = await send_junger_token(info[1], message, int(len(available_nft)))
        status = await check_tx_hash(tx_hash, PROJECT_WALLET_ADDRESS, int(len(available_nft))) #use try catch
        time.sleep(5)
        if status:
            s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)

async def check(info):
    with open("metadata.json") as file:
        digits = re.findall(r'\d+', info[5])
        i = 0
        numbers = [num for num in digits]
        value = (float(XRD_LIMIT)* int(len(numbers)))/float(info[3])
        rounded_value = round(value, 1)
        nums_to_send = []
    if info[0] == 'TransferTokens' and info[4] == 'xrd_rr1qy5wfsfh' and info[5] != '-' and rounded_value == 1 and len(numbers) > 0:  # this is not needed info[5] != '-'
        for num in numbers:
            i += 1
            found = False
            for item in data_json:
                if item["ID"] == num:
                    found = True
                    if item["owner"] == "available":
                        nums_to_send.append(num)
                    else:
                        message = f"NFT with ID {num} already owned"
                        await send_radix(info[1], message, info[4], float(XRD_LIMIT)) #we need to add check_tx_hash()  #use try catch
                        time.sleep(5)
            if not found:
                message = f"NFT with ID {num} not found, Try buying Another"
                await send_radix(info[1], message, info[4], float(XRD_LIMIT))
                time.sleep(5)

        if len(nums_to_send) > 0:
            nums_str = ", ".join(nums_to_send)
            message  =  f"Purchased Successful! You're now the guardian of Jungler NFT(s) with ID(s) {nums_str}. Thank you for joining our mission to save the rainforest! Welcome to the community! "
            tx_hash = await send_junger_token(info[1], message, int(len(nums_to_send))) # we need to send only len of available nfts 2/3
            time.sleep(5)
            status = await check_tx_hash(tx_hash, PROJECT_WALLET_ADDRESS, int(len(nums_to_send))) #use try catch
            time.sleep(5)
            if status:
                for nftItem in nums_to_send:
                    for item in data_json:
                        if item['ID'] == nftItem and item['owner'] == "available":
                            item["owner"] = info[1]
                #if buy one offer expires then remove below code
                s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)
                time.sleep(5)
                #Get 1 NFT free for each 1 NFT purchase
                await get_one_free(info,len(nums_to_send))
            else:
                nums_str = ", ".join(nums_to_send)
                message  =  f"Transaction failed: Yours NFT(s) with ID(s) {nums_str}, please try after sometime."
                refund_xrd_amount = float(len(nums_to_send) * XRD_LIMIT)
                await send_radix(info[1], message, info[4], refund_xrd_amount)
                time.sleep(5)

        s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=METADATA_FILE_KEY)

    else:
        await send_radix(info[1], "Refund processed! We detected an invalid transaction attempt. Follow the instructions on srilankanjunglers.com. Please ensure you have the necessary funds and try again. If this issue persists, reach out to our support team for assistance.",info[4], float(info[3]))
        time.sleep(5)
