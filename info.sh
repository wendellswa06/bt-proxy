#!/bin/bash

# Proxy script for blockchain staking operations.

# Define delegator mapping
declare -A DELEGATOR
DELEGATOR[jjcom]="multisig-jjpes-jjcom"
DELEGATOR[atel]="multisig-jjpes-atel"

validator_hotkey='5CsvRJXuR955WojnGMdok1hbhffZyB4N5ocrv82f3p5A2zVp'

# Function to show help
show_help() {
    cat << EOF
Get multisig wallet info

Usage: $0 COLDKEY

Arguments:
    COLDKEY    Name of the wallet (required)

Options:
    -h, --help    Show this help message and exit
EOF
}

main() {
    local network='finney'
    
    # Check if no arguments provided
    if [[ $# -eq 0 ]]; then
        show_help
        exit 1
    fi
    
    # Check for help flag
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        show_help
        exit 0
    fi
    
    # Get coldkey from first argument
    coldkey="$1"
    
    # Validate coldkey
    if [[ "$coldkey" != "jjcom" && "$coldkey" != "atel" ]]; then
        exit 1
    fi
    
    # Get delegator wallet
    delegator_wallet="${DELEGATOR[$coldkey]}"
    
    # Execute command
    command="btcli st list --subtensor.network finney --wallet.name $delegator_wallet"
    eval "$command"
}

# Run main function with all arguments
main "$@"
