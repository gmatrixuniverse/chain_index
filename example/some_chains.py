import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

import chain_index
print(f"chainindex location: {chain_index.__file__}")
from chain_index import get_chain_info, ChainNotFoundError, get_token_info, get_chain_tokens, get_all_chain_tokens

def print_chain_info(chain):
    print(chain)
    # print(f"Chain Name: {chain.name}")
    # print(f"Chain ID: {chain.chainId}")
    # print(f"Native Currency: {chain.nativeCurrency}")
    
    # # Check if wrapperNativeCurrency attribute exists
    # if hasattr(chain, 'wrapperNativeCurrency'):
    #     print(f"Wrapper Native Currency: {chain.wrapperNativeCurrency or 'N/A'}")
    
    # print(f"RPC URLs: {', '.join(chain.rpc)}")
    # print(f"Explorer: {chain.explorers[0].url if chain.explorers else 'N/A'}")
    # print(f"Block Explorer: {chain.explorers[0].url if chain.explorers else 'N/A'}")
    # print(f"ENS Registry: {chain.ens or 'N/A'}")
    # print(f"Aliases: {chain.shortName}")
    # print("-" * 50)

def print_chain_tokens(chain_id):
    try:
        tokens = get_chain_tokens(chain_id)
        print(f"\nCommon tokens on chain {chain_id}:")
        for symbol, token in tokens.items():
            print(f"- {token.name} ({symbol})")
            print(f"  Contract: {token.contract}")
            print(f"  Decimals: {token.decimals}")
    except ChainNotFoundError as e:
        print(f"Error: {e}")

def print_all_chain_tokens(chain_id):
    try:
        chain_tokens = get_all_chain_tokens(chain_id)
        print(f"\nAll tokens on chain {chain_id} ({chain_tokens.chain.name}):")
        
        # Print native token
        print("\nNative token:")
        print(f"- {chain_tokens.native_token.name} ({chain_tokens.native_token.symbol})")
        print(f"  Decimals: {chain_tokens.native_token.decimals}")
        
        # Print wrapped native token if exists
        if chain_tokens.wrapped_native:
            print("\nWrapped native token:")
            print(f"- {chain_tokens.wrapped_native.name} ({chain_tokens.wrapped_native.symbol})")
            print(f"  Contract: {chain_tokens.wrapped_native.contract}")
            print(f"  Decimals: {chain_tokens.wrapped_native.decimals}")
        
        # Print common tokens
        print("\nCommon tokens:")
        for symbol, token in chain_tokens.common_tokens.items():
            print(f"- {token.name} ({symbol})")
            print(f"  Contract: {token.contract}")
            print(f"  Decimals: {token.decimals}")
            
    except ChainNotFoundError as e:
        print(f"Error: {e}")

def main():
    # Example 1: Get chain info by ID
    print("Example 1: Ethereum Mainnet (by ID)")
    ethereum = get_chain_info(1)
    print_chain_info(ethereum)

    # Example 2: Get chain info by name
    print("Example 2: Polygon Mainnet (by name)")
    try:
        polygon = get_chain_info("Polygon Mainnet")
        print_chain_info(polygon)
    except ChainNotFoundError as e:
        print(f"Error: {e}")

    # Example 3: Get info for a testnet
    print("Example 3: Goerli Testnet")
    try:
        goerli = get_chain_info("Goerli")
        print_chain_info(goerli)
    except ChainNotFoundError as e:
        print(f"Error: {e}")

    # Example 4: Error handling for invalid chain
    print("Example 4: Invalid Chain")
    try:
        invalid_chain = get_chain_info(999999)
    except ChainNotFoundError as e:
        print(f"Error: {e}")

    # Example 5: Compare two chains
    print("Example 5: Compare Ethereum and Optimism gas tokens")
    try:
        ethereum = get_chain_info(1)
        optimism = get_chain_info("Optimism")
        eth_gas = ethereum.nativeCurrency
        op_gas = optimism.nativeCurrency
        print(f"Ethereum gas token: {eth_gas.name} ({eth_gas.symbol})")
        print(f"Optimism gas token: {op_gas.name} ({op_gas.symbol})")
    except ChainNotFoundError as e:
        print(f"Error: {e}")

    # Example 6: Get token information
    print("\nExample 6: Get token information")
    try:
        usdt = get_token_info(1, "USDT")
        print(f"USDT contract on Ethereum: {usdt.contract}")
        
        # Print all common tokens on Ethereum
        print_chain_tokens(1)
    except (ChainNotFoundError, TokenNotFoundError) as e:
        print(f"Error: {e}")

    # Example 7: Get all tokens on a chain
    print("\nExample 7: Get all tokens on Ethereum")
    print_all_chain_tokens(1)
    
    # Example 8: Get specific token including native and wrapped
    print("\nExample 8: Get specific tokens")
    try:
        eth_tokens = get_all_chain_tokens(1)
        eth = eth_tokens.get_token("ETH")
        weth = eth_tokens.get_token("WETH")
        print(f"ETH contract: {eth.contract}")
        print(f"WETH contract: {weth.contract}")
    except (ChainNotFoundError, TokenNotFoundError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
