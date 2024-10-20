import sys
from pathlib import Path

# Add the parent directory to sys.path
parent_dir = str(Path(__file__).parent.parent)
sys.path.append(parent_dir)

import chain_index
print(f"chainindex location: {chain_index.__file__}")
from chain_index import get_chain_info, ChainNotFoundError

def print_chain_info(chain):
    print(f"Chain Name: {chain.name}")
    print(f"Chain ID: {chain.chainId}")
    print(f"Native Currency: {chain.nativeCurrency}")
    print(f"RPC URLs: {chain.rpc}")
    print(f"Block Explorer: {chain.explorers[0].url if chain.explorers else 'N/A'}")
    print(f"ENS Registry: {chain.ens or 'N/A'}")
    print(f"Aliases: {chain.shortName}")
    print("-" * 50)

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

if __name__ == "__main__":
    main()
