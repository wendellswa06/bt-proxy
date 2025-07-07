import bittensor as bt
from substrateinterface import SubstrateInterface
from typing import Optional, cast
from bittensor.utils.balance import Balance, FixedPoint, fixed_to_float

RPC_ENDPOINTS = {
    'test': 'wss://test.finney.opentensor.ai:443',
    'finney': 'wss://entrypoint-finney.opentensor.ai:443',
}

class RonProxy:
    def __init__(self, proxy_wallet: str, network: str, delegator: str):
        """
        Initialize the RonProxy object.
        
        Args:
            proxy_wallet: Proxy wallet address
            network: Network name
            delegator: Delegator address
        """
        if network not in RPC_ENDPOINTS:
            raise ValueError(f"Invalid network: {network}")
        
        self.network = network
        self.delegator = delegator
        self.proxy_wallet = bt.wallet(name=proxy_wallet)
        self.subtensor = bt.subtensor(network=network)
        self.substrate = SubstrateInterface(
            url=RPC_ENDPOINTS[self.network],
            ss58_format=42,
            type_registry_preset='substrate-node-template',
        )


    def _add_stake(self, netuid: int, hotkey: str, amount: Balance) -> None:
        """
        Add stake to a subnet.
        
        Args:
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to stake
        """
        balance = self.subtensor.get_balance(
            address=self.delegator,
        )
        print(f"Current balance: {balance}")
        
        confirm = input(f"Do you really want to stake {amount}? (y/n)")
        if confirm == "y":
            pass
        else:
            return
        
        call = self.substrate.compose_call(
            call_module='SubtensorModule',
            call_function='add_stake',
            call_params={
                'hotkey': hotkey,
                'netuid': netuid,
                'amount_staked': amount.rao,
            }
        )
        is_success, error_message = self._do_proxy_call(call)
        if is_success:
            print(f"Stake added successfully")
        else:
            print(f"Error: {error_message}")
    
    def _calculate_slippage(
        self, subnet_info, amount: Balance, stake_fee: Balance
    ) -> tuple[Balance, str, float, str]:
        """Calculate slippage when adding stake.

        Args:
            subnet_info: Subnet dynamic info
            amount: Amount being staked
            stake_fee: Transaction fee for the stake operation

        Returns:
            tuple containing:
            - received_amount: Amount received after slippage and fees
            - slippage_str: Formatted slippage percentage string
            - slippage_float: Raw slippage percentage value
            - rate: Exchange rate string
        """
        amount_after_fee = amount - stake_fee
        
        if amount_after_fee < 0:
            print_error("You don't have enough balance to cover the stake fee.")
            raise ValueError()
        received_amount, _ = subnet_info.tao_to_alpha_with_slippage(amount_after_fee)
        print(received_amount)
        if subnet_info.is_dynamic:
            ideal_amount = subnet_info.tao_to_alpha(amount)
            total_slippage = ideal_amount - received_amount
            slippage_pct_float = 100 * (total_slippage.tao / ideal_amount.tao)
            slippage_str = f"{slippage_pct_float:.4f} %"
            rate = f"{(1 / subnet_info.price.tao or 1):.4f}"
        else:
            slippage_pct_float = (
                100 * float(stake_fee.tao) / float(amount.tao) if amount.tao != 0 else 0
            )
            slippage_str = f"{slippage_pct_float:.4f} %"
            rate = "1"

        return received_amount, slippage_str, slippage_pct_float, rate

    def add_stake(self, wallet: str, netuid: int, hotkey: str, amount: Balance, tolerance: float) -> None:
        """
        Add stake to a subnet.
        
        Args:
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to stake
        """
        allow_partial_stake = False
        balance = self.subtensor.get_balance(
            address=self.delegator,
        )
        
        stake_fee = self.subtensor.get_stake_add_fee(
            amount,
            netuid,
            self.delegator,
            hotkey
        )
        subnet_info = self.subtensor.all_subnets()[netuid]
        received_amount, slippage_pct, slippage_pct_float, rate = (
            self._calculate_slippage(subnet_info, amount, stake_fee)
        )
        
        pool = self.subtensor.subnet(netuid=netuid)
        base_price = pool.price.rao
        price_with_tolerance = base_price * (1 + tolerance)
        original_tolerance = 0
        if tolerance * 100 < slippage_pct_float:
            original_tolerance = tolerance
            tolerance = slippage_pct_float / 100 * 1.5
        print(f"----validator to delegate to: {hotkey}")
        print(f"----Current balance: {balance}")
        print(f"----price: {base_price/100000}")
        print(f"----rao amount to stake: {amount.rao}")
        print(f"----slippage: {tolerance}")
        
        # calculate base slippage
        print(wallet)
        
        
        print(f"🚩🚩🚩🚩🚩🚩Base Slippage: {slippage_pct} | original: {original_tolerance} | new: {tolerance}")
        
        call = self.substrate.compose_call(
            call_module='SubtensorModule',
            call_function='add_stake_limit',
            call_params={
                'hotkey': hotkey,
                'netuid': netuid,
                'amount_staked': amount.rao,
                "limit_price": price_with_tolerance,
                "allow_partial": allow_partial_stake,
            }
        )
        is_success, error_message = self._do_proxy_call(call)
        if is_success:
            print(f"Stake added successfully")
        else:
            print(f"Error: {error_message}")

    def _remove_stake(self, netuid: int, hotkey: str, amount: Balance,
                    all: bool = False) -> None:
        """
        Remove stake from a subnet.
        
        Args:
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to unstake (if not using --all)
            all: Whether to unstake all available balance
        """
        balance = self.subtensor.get_stake(
            coldkey_ss58=self.delegator,
            hotkey_ss58=hotkey,
            netuid=netuid,
        )
        print(f"Current alpha balance: {balance}")

        if all:
            confirm = input("Do you really want to unstake all available balance? (y/n)")
            if confirm == "y":
                amount = balance
            else:
                return
        else:
            confirm = input(f"Do you really want to unstake {amount}? (y/n)")
            if confirm == "y":
                pass
            else:
                return
            
        if amount.rao > balance.rao:
            print(f"Error: Amount to unstake is greater than current balance")
            return

        call = self.substrate.compose_call(
            call_module='SubtensorModule',
            call_function='remove_stake',
            call_params={
                'hotkey': hotkey,
                'netuid': netuid,
                'amount_unstaked': amount.rao - 1,
            }
        )
        is_success, error_message = self._do_proxy_call(call)
        if is_success:
            print(f"Stake removed successfully")
        else:
            print(f"Error: {error_message}")

    def remove_stake(self, wallet: str, netuid: int, hotkey: str, amount: Balance, tolerance: float,
                    all: bool = False) -> None:
        """
        Remove stake from a subnet.
        
        Args:
            netuid: Network/subnet ID
            hotkey: Hotkey address
            amount: Amount to unstake (if not using --all)
            all: Whether to unstake all available balance
        """
        balance = self.subtensor.get_stake(
            coldkey_ss58=self.delegator,
            hotkey_ss58=hotkey,
            netuid=netuid,
        )
        print(f"----Current alpha balance: {balance}")

        print(f"----rao amount to unstake: {amount.rao}")
        print(f"----slippage: {tolerance}")
        print(f"----validator to delegate to: {hotkey}")
        
        if all:
            confirm = input("Do you really want to unstake all available balance? (y/n)")
            if confirm == "y":
                amount = balance
            else:
                return
        
        if amount.rao > balance.rao:
            print(f"Error: Amount to unstake is greater than current balance")
            return

        pool = self.subtensor.subnet(netuid=netuid)
        base_price = pool.price.rao
        price_with_tolerance = base_price * (1 - tolerance)
        allow_partial_stake = False
        
        call = self.substrate.compose_call(
            call_module='SubtensorModule',
            call_function='remove_stake_limit',
            call_params={
                'hotkey': hotkey,
                'netuid': netuid,
                'amount_unstaked': amount.rao,
                "limit_price": price_with_tolerance,
                "allow_partial": allow_partial_stake,
            }
        )
        is_success, error_message = self._do_proxy_call(call)
        if is_success:
            print(f"Stake removed successfully")
        else:
            print(f"Error: {error_message}")


    def swap_stake(self, hotkey: str, origin_netuid: int, dest_netuid: int,
                amount: Balance, all: bool = False) -> None:
        """
        Swap stake between subnets.
        
        Args:
            hotkey: Hotkey address
            origin_netuid: Source subnet ID
            dest_netuid: Destination subnet ID
            amount: Amount to swap (if not using --all)
            all: Whether to swap all available balance
        """
        balance = self.subtensor.get_stake(
            coldkey_ss58=self.delegator,
            hotkey_ss58=hotkey,
            netuid=origin_netuid,
        )
        print(f"Current alpha balance on netuid {origin_netuid}: {balance}")
        
        if all:
            confirm = input("Do you really want to swap all available balance? (y/n)")
            if confirm == "y":
                amount = balance
            else:
                return
        else:
            confirm = input(f"Do you really want to swap {amount}? (y/n)")
            if confirm == "y":
                pass
            else:
                return
            
        if amount.rao > balance.rao:
            print(f"Error: Amount to swap is greater than current balance")
            return
        
        call = self.substrate.compose_call(
            call_module='SubtensorModule',
            call_function='swap_stake',
            call_params={
                'hotkey': hotkey,
                'origin_netuid': origin_netuid,
                'destination_netuid': dest_netuid,
                'alpha_amount': amount.rao,
            }
        )
        is_success, error_message = self._do_proxy_call(call)
        if is_success:
            print(f"Stake swapped successfully")
        else:
            print(f"Error: {error_message}")


    def _do_proxy_call(self, call) -> tuple[bool, str]:
        proxy_call = self.substrate.compose_call(
            call_module='Proxy',
            call_function='proxy',
            call_params={
                'real': self.delegator,
                'force_proxy_type': 'Staking',
                'call': call,
            }
        )
        extrinsic = self.substrate.create_signed_extrinsic(
            call=proxy_call,
            keypair=self.proxy_wallet.coldkey,
        )
        receipt = self.substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        
        is_success = receipt.is_success
        error_message = receipt.error_message
        return is_success, error_message