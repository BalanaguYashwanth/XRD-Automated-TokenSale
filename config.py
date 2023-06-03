import os
import radixlib as radix


MNEMONIC_PHRASE = os.environ.get("MNEMONIC_PHRASE")
PROJECT_WALLET_ADDRESS = os.environ.get("PROJECT_WALLET_ADDRESS") 

XRD_LIMIT = os.environ.get("XRD_LIMIT")
JUNGLER_LIMIT = os.environ.get("JUNGLER_LIMIT")

ACCESS_KEY_ID = os.environ.get("ACCESS_KEY_ID")
SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")

BUCKET_NAME = os.environ.get("BUCKET_NAME")
XRD_TRANSACTIONS_FILE_KEY = os.environ.get("XRD_TRANSACTIONS_FILE_KEY")
METADATA_FILE_KEY = os.environ.get("METADATA_FILE_KEY")

network: radix.network.Network = radix.network.MAINNET
xrd_rri: str = radix.derive.xrd_rri_on_network(network)


token_name: str = "Srilankan Junglers"
token_symbol: str = "SJ"
token_description: str = "Preserve The Rainforest, Own A Piece Of Nature"
token_icon_url: str = ""
token_url: str = "https://srilankanjunglers.com/"
token_granularity: int = 1
token_supply: int = 10_000 * (10**18)  # The token supply is 10K
