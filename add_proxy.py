import bittensor as bt
from substrateinterface import SubstrateInterface

RPC_ENDPOINTS = {
    'test': 'wss://test.finney.opentensor.ai:443',
    'finney': 'wss://entrypoint-finney.opentensor.ai:443',
}

if __name__ == "__main__":
    network = input("Enter network (test/finney): ")
    print("")

    if network not in ['test', 'finney']:
        print("Invalid network")
        exit(1)
        
    wallet_name = input("Enter wallet name: ")
    print("")
    
    wallet = bt.wallet(name=wallet_name)

    proxy_address = input("Enter proxy address: ")
    print("")
    
    if not proxy_address:
        print("Proxy address is required")
        exit(1)
    
    substrate = SubstrateInterface(
        url=RPC_ENDPOINTS[network],
        ss58_format=42,
        type_registry_preset="substrate-node-template",
    )
    
    call = substrate.compose_call(
        call_module='Proxy',
        call_function='add_proxy',
        call_params={
            'delegate': proxy_address,
            'proxy_type': 'Staking',
            'delay': 0,
        }
    )
    extrinsic = substrate.create_signed_extrinsic(
        call=call,
        keypair=wallet.coldkey,
    )
    receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
    
    is_success = receipt.is_success
    if is_success:
        print("Proxy added successfully")
        print(f"Transaction hash: {receipt.extrinsic_hash}")
    else:
        print(f"Error: {receipt.error_message}")
