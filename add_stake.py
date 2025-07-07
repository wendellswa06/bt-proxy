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

validator_hotkey = '5CsvRJXuR955WojnGMdok1hbhffZyB4N5ocrv82f3p5A2zVp'

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Proxy script for blockchain staking operations",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # add stake command
    parser.add_argument('--coldkey', type=str, required=True, default='jjcom', help='Name of the wallet')
    parser.add_argument('--netuid', type=int, required=True, help='Network/subnet ID')
    parser.add_argument('--amount', type=float, default=0, help='Amount to unstake')
    parser.add_argument('--tol', type=float, default=0.005, help='tolerance limit to be used')
    
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
    delegator = DELEGATOR[proxy_wallet]
        
    # Initialize RonProxy object
    ron_proxy = RonProxy(
        proxy_wallet=proxy_wallet,
        network=network,
        delegator=delegator,
    )
    print(f"Initialized RonProxy object for {network} network")
    
    try:        
        ron_proxy.add_stake(
            wallet=args.coldkey,
            netuid=args.netuid,
            hotkey=validator_hotkey,
            amount=Balance.from_tao(args.amount),
            tolerance=args.tol
        )
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
