
"""
In this example we demonstrate how you can obtain the balances of a wallet.

This method uses the provider without using a signer as there is no need to create a full wallet
object to perform this simple query (you can do it from the wallet object, it's just not needed.)
"""
import time
import schedule
import boto3
import asyncio
import json
from typing import Optional, List, Dict, Any
import radixlib as radix
from constant_types import CRUD
import parser_radix_hash
import check_data_and_add
from config import PROJECT_WALLET_ADDRESS,ACCESS_KEY_ID,SECRET_ACCESS_KEY,BUCKET_NAME,XRD_TRANSACTIONS_FILE_KEY


s3_client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
response = s3_client.get_object(Bucket=BUCKET_NAME, Key=XRD_TRANSACTIONS_FILE_KEY)
existing_json = json.loads(response['Body'].read())
existing_data = existing_json['xrdTransactions']


async def main() -> None:
    # The address of the account that we want to get the transaction history for.
    account_address: str = f"{PROJECT_WALLET_ADDRESS}"

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.MAINNET

    # Creating the provider object which is esentially our link or connection to the blockchain
    # via the gateway API.
    provider: radix.Provider = radix.Provider(network)

    # Creating an empty list to store the transactions and beggining to query for the transactions
    transactions_list: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while True:
        # Getting the transaction history for the current cursor
        query_response: Dict[str, Any] = provider.get_account_transactions(
            account_address=account_address,
            cursor=cursor
        )

        # Parsing the query response and then extending the transactions list with the parsed
        # response.
        parsed_transaction_list: List[Dict[str, Any]] = radix.parsers.DefaultParser.parse(
            data=query_response,
            data_type="get_account_transactions"
        )
        transactions_list.extend(parsed_transaction_list)

        # Getting the cursor from the query response if it's present. If there is no cursor present
        # then we have reached the end of the transaction history and can safely stop fetching
        # transactions
        cursor = query_response.get('next_cursor')
        if cursor is None:
            break

    # Проверка каждой транзакции по хэшу
    for transaction in transactions_list:
        try:
            hash_value = transaction['hash']
            print(hash_value)
            # check_transactions_file(hash_value, CRUD.PENDING)
            if not check_transactions_file(hash_value, CRUD.PENDING):
                print("The transaction has already been verified.")
                break
            else:
                # Вызов функции get_info для проверки транзакции
                info = parser_radix_hash.get_info(hash_value)
                print(info)
                if info[2] == f'{PROJECT_WALLET_ADDRESS}':
                    await check_data_and_add.check(info)

                check_transactions_file(hash_value,CRUD.SUCCESS)
                print(
                    "The transaction has been successfully added to the verified list.")
        except Exception as e:
            check_transactions_file(hash_value,CRUD.ERROR)
            print("Error validating transaction.---", e)


def check_transactions_file(hash_value, type):
    new_hash_flag = True
    if type == CRUD.PENDING:
        for old_transaction in existing_data:
            if hash_value == old_transaction["id"]:
                new_hash_flag = False
            

        if new_hash_flag == True:
            new_transaction_data={
                "id":hash_value,
                "status":CRUD.PENDING,
            }
            existing_data.append(new_transaction_data)
            s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=XRD_TRANSACTIONS_FILE_KEY)
        
    elif type == CRUD.SUCCESS:
        for index,old_transaction in enumerate(existing_data):
            if hash_value == old_transaction['id']:
                update_transaction_data={
                    "id":hash_value,
                    "status":CRUD.SUCCESS,
                }
                existing_data[index] = update_transaction_data
                break
        s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=XRD_TRANSACTIONS_FILE_KEY)

    elif type == CRUD.ERROR:
        for index,old_transaction in enumerate(existing_data):
            if hash_value == old_transaction["id"]:
                update_transaction_data={
                    "id":hash_value,
                    "status":CRUD.ERROR,
                    }
                existing_data[index] = update_transaction_data
                break
        s3_client.put_object(Body=json.dumps(existing_json), Bucket=BUCKET_NAME, Key=XRD_TRANSACTIONS_FILE_KEY)

    return new_hash_flag
            
def cronJob():
    asyncio.run(main())

schedule.every(5).seconds.do(cronJob)

if __name__ == "__main__":
    # asyncio.run(main())
    while True:
        schedule.run_pending()
        time.sleep(5)

def lambda_handler(event, context):
    main()
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }