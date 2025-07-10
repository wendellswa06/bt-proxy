#!/usr/bin/env python3
"""
Proxy script for blockchain staking operations.
"""

import argparse
import sys
from modules import RonProxy
from bittensor.utils.balance import Balance

DELEGATOR = {
    'jjcom': '5CF3fFYemt9A4DfdPGQiE8rqMYEeG3ioL3dQHkbX97MqmNBE',
    'atel': '5CHLb1prLQ4MjA6bYbpPfx1gzvaGpeSfXkk84sMDcNXRQDPd',
}

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Proxy script for blockchain staking operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # add stake command
    parser.add_argument('--coldkey', type=str, required=True, default='jjcom', help='Name of the wallet')
    parser.add_argument('--hotkey', type=str, required=True, default='jja', help='Name of the wallet')
    parser.add_argument('--netuid', type=int, required=True, help='Network/subnet ID')
    
    
    return parser

def main():
    """Main entry point."""
    network = 'finney'
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    # Create parser
    parser = create_parser()
    
    # Parse arguments
    
    args = parser.parse_args()
    if args.coldkey != 'jjcom' and args.coldkey != 'atel':
        sys.exit(1)
    proxy_wallet = args.coldkey
    proxy_hotkey = args.hotkey
        
    delegator = DELEGATOR[proxy_wallet]
        
    # Initialize RonProxy object
    ron_proxy = RonProxy(
        proxy_wallet=proxy_wallet,
        network=network,
        delegator=delegator,
        proxy_hotkey=proxy_hotkey,
    )
    print(f"Initialized RonProxy object for {network} network")
    
    try:        
        ron_proxy.register_miner(
            netuid=args.netuid,
        )
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
