"""
This example demonstrates how tokens can be sent from your wallet to another wallet.
"""
import requests
import radixlib as radix
import os
import config
from config import MNEMONIC_PHRASE,PROJECT_WALLET_ADDRESS,JUNGLER_LIMIT,CHANNEL_ID,TELEGRAM_BOT_TOKEN


async def send_radix(recipient_address, transaction_message, amount):
    # Information about the person who we're sending the tokens to and the amount of tokens we're
    # sending.
    # recipient_address: str = "tdx1qsprkzrtmdhvfjnd9z00xtmmwg9p5wn5yawsuttu7dqqgsx2wfm25eqawk3n0"
    token_rri: str = radix.constants.XRD_RRI['mainnet']
    transfer_amount = radix.derive.atto_from_xrd(float(amount))  # We will be sending them 200 XRD.
    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.MAINNET

    # Getting the mnemonic phrase for the wallet that we will be connecting to. In this case, my
    # mnemonic phrase is stored in an envirnoment variable under the name "MNEMONIC_PHRASE".
    # You might want to do the same or you could also just put your mnemonic phrase as a literal
    # string.
    mnemonic_phrase: str = MNEMONIC_PHRASE

    # Creating a new wallet object using the mnemonic phrase above on the network defined.
    wallet: radix.Wallet = radix.Wallet(
        provider=radix.Provider(network),
        signer=radix.Signer.from_mnemonic(mnemonic_phrase)
    )

    # Using the quick transactions capability of the wallet object to create a transaction for the
    # token transfer.

    try:
        #TODO- Send telegram channel link,
        tx_hash =  wallet.build_sign_and_send_transaction(
            actions=(
                wallet.action_builder.token_transfer(
                        from_account_address=wallet.address,
                        to_account_address=recipient_address,
                        token_rri=token_rri,
                        transfer_amount=transfer_amount
                    )
            ),
            message_string=transaction_message
        )

        await telegram_bot_push_message(tx_hash=tx_hash)
        # print("Fund transfer done under transaction hash:", tx_hash)
    except Exception as e:
        print('error in send radix-----',e)


async def send_junger_token(recipient_address, transaction_message, jungler_count):
    # Loading up our wallet through the information that we provided in the config file
    
    mnemonic_phrase: str = MNEMONIC_PHRASE
    transfer_amount: int = radix.derive.atto_from_xrd(float(JUNGLER_LIMIT)*float(jungler_count))

    wallet: radix.Wallet =  radix.Wallet(
        provider=radix.Provider(config.network),
        signer=radix.Signer.from_mnemonic(mnemonic_phrase)
    )
    # Deriving the token RRI for the token that we will will be selling
    token_rri: str =  radix.derive.token_rri(
        creator_public_key=wallet.public_key,
        token_symbol=config.token_symbol.lower(),
        network=config.network
    )
    # print("Sale is done on token:", token_rri)

    # Using the quick transactions capability of the wallet object to create a transaction for the
    # token transfer.

    try:
        #TODO- Send telegram channel link,
        tx_hash =  wallet.build_sign_and_send_transaction(
            actions=(
                wallet.action_builder
                .token_transfer(
                    from_account_address=PROJECT_WALLET_ADDRESS,
                    to_account_address=recipient_address,
                    token_rri=token_rri,
                    transfer_amount=transfer_amount
                )
            ),
            message_string=transaction_message
        )
        await telegram_bot_push_message(tx_hash=tx_hash)
        # print("Fund transfer done under transaction hash:", tx_hash)
        return tx_hash
    except Exception as e:
        print('error in sending jungler---',e)


async def check_tx_hash(tx_hash, project_wallet_address, count_tx_check) -> None:
    # The address of the account that we want to get the transaction history for.
    account_address: str = project_wallet_address

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.MAINNET

    # Creating the provider object which is esentially our link or connection to the blockchain
    # via the gateway API.
    provider: radix.Provider = radix.Provider(network)

    # Creating an empty list to store the transactions and beggining to query for the transactions
    transactions_list: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    try:
        query_response: Dict[str, Any] = provider.get_account_transactions(
                account_address=account_address,
                cursor=cursor,
                limit=count_tx_check
            )
        parsed_transaction_list: List[Dict[str, Any]] =  radix.parsers.DefaultParser.parse(
            data=query_response,
            data_type="get_account_transactions"
        )
        transactions_list.extend(parsed_transaction_list)
        
    except Exception as e:
        print('error in checking tx hash---',e)

    # sliced_transaction_list = transactions_list[0,count_tx_check+1]
    status = False
    for tx in transactions_list:
        if tx['hash'] == tx_hash and tx['status'] == "CONFIRMED":
            status = True
            break
        

    # Printing the transactions to the console
    # print('Transactions:', transactions_list)
    # return True #if success true or failure false\
    return status

async def telegram_bot_push_message(tx_hash):
    base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    parameters = {
        "chat_id" : CHANNEL_ID,
        "text" : tx_hash
    }

    requests.get(base_url, data = parameters)