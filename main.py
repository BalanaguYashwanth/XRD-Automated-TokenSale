
"""
In this example we demonstrate how you can obtain the balances of a wallet.

This method uses the provider without using a signer as there is no need to create a full wallet
object to perform this simple query (you can do it from the wallet object, it's just not needed.)
"""
import time
from typing import Optional, List, Dict, Any
import radixlib as radix

import parser_radix_hash
import check_data_and_add
from config import PROJECT_WALLET_ADDRESS


def main() -> None:
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

    txt_file_path = "transactions.txt"

    # Загрузка существующих транзакций из текстового файла
    existing_transactions = set()
    try:
        with open(txt_file_path, "r") as file:
            lines = file.readlines()
            existing_transactions = set(map(str.strip, lines))
    except FileNotFoundError:
        pass

    # Проверка каждой транзакции по хэшу
    for transaction in transactions_list:
        try:
            hash_value = transaction['hash']
            print(hash_value)
            if hash_value in existing_transactions:
                print("The transaction has already been verified.")
                break
            else:
                # Вызов функции get_info для проверки транзакции
                info = parser_radix_hash.get_info(hash_value)
                print(info)
                if info[2] == f'{PROJECT_WALLET_ADDRESS}':
                    check_data_and_add.check(info)
                # Добавление хэша транзакции в текстовый файл
                with open(txt_file_path, "a") as file:
                    file.write(hash_value + "\n")
                print("The transaction has been successfully added to the verified list.")
        except Exception as e:
            print("Error validating transaction.---",e)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(300)
