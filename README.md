# Overview

Proxy for Bittensor Staking - Ensuring 100% confidence and security for Subnet alpha token traders

# How to use

## Installation

```git clone https://github.com/ronx-labs/bt-proxy.git```

```cd bt-proxy```

```python3 -m venv .venv```

```source .venv/bin/activate```

```pip3 install -r requirements.txt```

## Add proxy

You need to add proxy to your delegator address.

```python3 add_proxy.py```

It will prompt you to enter your delegator wallet name and proxy address. And it will add the proxy address to the delegator address.

Now the proxy address can make staking tansactions (including `add_stake`, `remove_stake`, and `swap_stake`) on behalf of delegator address.

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

# Buy me a coffee!

Just follow me on GitHub and star this repo. Thank you!
