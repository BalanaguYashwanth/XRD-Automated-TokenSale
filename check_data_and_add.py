import json
import re

from sale import send_radix, send_junger_token


def check(info):
    with open("metadata.json") as file:
        data_json = json.load(file)
        
    if info[0] == 'TransferTokens' and info[4] == 'xrd_rr1qy5wfsfh' and info[5] != '-':

        value = int(float(info[3]) / 1)
        digits = re.findall(r'\d+', info[5])
        i = 0
        numbers = [num.zfill(4) for num in digits]
        for num in numbers:
            i += 1
            found = False
            for item in data_json:
                if item["ID"] == num:
                    found = True
                    if item["owner"] == "available":
                        idf = item["ID"]
                        print(f"New owner for NFT ID - {idf}")
                        item["owner"] = info[1]
                        message = f"Yours NFT with ID {num} "
                        send_junger_token(info[1], message)
                    else:
                        message = f"NFT with ID {num} already owned"
                        print(message)
                        send_radix(info[1], message)
            if not found:
                message = f"NFT with ID {num} not found"
                print(message)
                send_radix(info[1], message)
            if i == value:
                break

        with open("metadata.json", "w") as file:
            json.dump(data_json, file)
    else:
        print("its not TransferTokens or token not xrd or message = null")
