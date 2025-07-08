# Overview

Proxy for Bittensor Staking - Ensuring 100% confidence and security for Subnet alpha token traders

# How to use

## Installation

```git clone https://github.com/wendellswa06/bt-proxy.git```

```cd bt-proxy```

```python3 -m venv .venv```

```source .venv/bin/activate```

```pip3 install -r requirements.txt```

## Configure environment variables

- NETWORK=<test/finney>
- DELEGATOR=<multisig_wallet_address>
- PROXY_WALLET=<your_wallet_name>
- APPROVER=<approver_address> (another signatory of the multisig address)

## Add proxy

You need to add proxy to your delegator address.

```python3 multisig.py```

It will prompt you to select action type. Select `proxy`.

Then you need to input proxy address you want to add. If you want to add your wallet as a proxy, just type `self` and type your wallet password.

Then you need to select proxy type. Currently we support staking and registration. Select `staking`.

Making a transaction with multisig account involves two step.

The first step is you propose a transaction and the second step is the approver approves the proposed transaction.

It will display `call_hash` and `call_data` before asking you to enter your wallet password.

If you enter your password correctly, it will create a transaction proposal successfully.

Note that you need to hold some balance (at least 0.2 ~ 0.3 TAO) because multisig transaction proposal requires to lock some funds temporarily before the transaction gets approved. After successful approval, it will release the locked funds.

After successful transaction proposal, just copy `call_data` and send it to the approver so he can approve the proposed transaction.

Once the approver approves the proposed transaction, you should be able to make staking tansactions (including `add_stake`, `remove_stake`, and `swap_stake`) on behalf of delegator address.

## Do alpha trading with proxy address

First, you need to set environment variables by doing the below:

```cp .env.example .env```

Edit `.env` with your own environment variables.

Now you can run `proxy.py` script to make trading operations.

```python3 proxy.py --help```

You can see available commands in `proxy.py`.

You can do three types of operations – add, remove, and swap.

```python3 proxy.py addstake --help```

```python3 proxy.py removestake --help```

```python3 proxy.py swapstake --help```

## Transfer balance from multisig account

This process is similar with `add_proxy` process.

Just run `python3 multisig.py` and select `transfer` as action type.

Then enter the required inputs and propose a transfer transaction.

You just need to send `call_data` to the approver so he can approve the transfer transaction.

That's it!

## 🎉New🎉 Stake and unstake
You don't need .env anymore.
Before stake and unstake, DELEGATOR in add_stake and remove_stake should be changed for your case.

python add_stake --coldkey jjcom --netuid 39 --amount 1000 --tol 0.02
python remove_stake --coldkey jjcom --netuid 39 --amount 1000 --tol 0.02

## Get stake info from multisig wallets
You can use Info.sh
### Usage
./Info jjcom
This will show you multisig-jjpes-jjcom.
Useful or not?

# Buy me a coffee!

Just follow me on GitHub and star this repo. Thank you!
