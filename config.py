import radixlib as radix


MNEMONIC_PHRASE = ""
PROJECT_WALLET_ADDRESS = ''

network: radix.network.Network = radix.network.MAINNET
xrd_rri: str = radix.derive.xrd_rri_on_network(network)


token_name: str = ""
token_symbol: str = ""
token_description: str = ""
token_icon_url: str = ""
token_url: str = ""
token_granularity: int = 1
token_supply: int = 10_000 * (10**18)  # The token supply is 10K
