import os
import radixlib as radix


MNEMONIC_PHRASE = os.environ.get("MNEMONIC_PHRASE")
PROJECT_WALLET_ADDRESS = os.environ.get("PROJECT_WALLET_ADDRESS") 

XRD_LIMIT = os.environ.get("XRD_LIMIT")
JUNGLER_LIMIT = os.environ.get("JUNGLER_LIMIT")

network: radix.network.Network = radix.network.MAINNET
xrd_rri: str = radix.derive.xrd_rri_on_network(network)


token_name: str = "Srilankan Junglers"
token_symbol: str = "SJ"
token_description: str = "Preserve The Rainforest, Own A Piece Of Nature"
token_icon_url: str = ""
token_url: str = "https://srilankanjunglers.com/"
token_granularity: int = 1
token_supply: int = 10_000 * (10**18)  # The token supply is 10K
