"""
This example demonstrates how tokens can be sent from your wallet to another wallet.
"""

import radixlib as radix
import os
import config
from config import MNEMONIC_PHRASE,PROJECT_WALLET_ADDRESS,JUNGLER_LIMIT


def send_radix(recipient_address, transaction_message, amount):
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
    tx_hash: str = wallet.build_sign_and_send_transaction(
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
    print("Fund transfer done under transaction hash:", tx_hash)


def send_junger_token(recipient_address, transaction_message):
    # Loading up our wallet through the information that we provided in the config file
    
    mnemonic_phrase: str = MNEMONIC_PHRASE
    transfer_amount: int = radix.derive.atto_from_xrd(float(JUNGLER_LIMIT))

    wallet: radix.Wallet = radix.Wallet(
        provider=radix.Provider(config.network),
        signer=radix.Signer.from_mnemonic(mnemonic_phrase)
    )
    # Deriving the token RRI for the token that we will will be selling
    token_rri: str = radix.derive.token_rri(
        creator_public_key=wallet.public_key,
        token_symbol=config.token_symbol.lower(),
        network=config.network
    )
    print("Sale is done on token:", token_rri)

    # Using the quick transactions capability of the wallet object to create a transaction for the
    # token transfer.
    tx_hash: str = wallet.build_sign_and_send_transaction(
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
    print("Fund transfer done under transaction hash:", tx_hash)
