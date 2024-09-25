from orderly_evm_connector.lib.utils import check_required_parameters, get_timestamp


def get_registration_nonce(self):
    """[Public] Get Registration Nonce

    Retrieve a nonce used for registering an account on Orderly Network. The validity of the nonce value is 2 minutes. Each nonce can only be used once (ie for one account).

    GET /v1/registration_nonce

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/get-registration-nonce

    """

    return self._request("GET", "/v1/registration_nonce")

def get_account_details(self, account_id: str):
    """[Public] Get Account Details
    Limit: 10 requests per 1 second per IP address

    GET /v1/public/account

    Args：
        account_id(string):  The address of the user wallet

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/get-account-details

    """
    check_required_parameters([[account_id, "address"]])
    payload = {"account_id": account_id}
    return self._request("GET", "/v1/public/account", payload=payload)

def get_account(self, address: str, broker_id: str):
    """[Public] Get Account
    Limit: 10 requests per 1 second per IP address

    Check whether a particular account is registered on Orderly Network.

    GET /v1/get_account

    Args：
        address(string):  The address of the user wallet
        broker_id(string):	The broker that the account is registered on

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/get-account

    """
    check_required_parameters([[address, "address"], [broker_id, "broker_id"]])
    payload = {"address": address, "broker_id": broker_id}
    return self._request("GET", "/v1/get_account", payload=payload)


def get_broker(self, address: str):
    """[Public] Get Address Registered
    Limit: 10 requests per 1 second per IP address

    Check whether a particular address is registered on Orderly Network.

    GET /v1/get_broker

    Args：
        address(string):  The address of the user wallet

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/get-broker

    """
    check_required_parameters([[address, "address"]])
    payload = {"address": address}
    return self._request("GET", "/v1/get_broker", payload=payload)


def register_account(
    self, brokerId: str, chainId: int, registrationNonce: str, userAddress: str
):
    """Register Account

    Limit: 10 requests per 1 second per IP address

    Registers a new account to Orderly Network. Note an account is unique for each wallet address + broker id (ie the same wallet address can have multiple accounts with Orderly Network, 1 with each broker)

    POST /v1/register_account

    Args:
        message(json): Message object containing the message that is signed by the wallet owner
        message.brokerId(string): Broker ID
        message.chainId(number): Chain ID of registering chain (within those that are supported by the Network)
        message.timestamp(timestamp):   timestamp in UNIX milliseconds
        message.registrationNonce(string): Get Registration Nonce
        signature(string): The signature generated by signing the message object via EIP-712
        userAddress(string):   The address of the wallet signing the message object via EIP-712

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/register-account
    """
    _message = {
        "brokerId": brokerId,
        "chainId": chainId,
        "timestamp": int(get_timestamp()),
        "registrationNonce": registrationNonce,
    }
    message = {
        "domain": {
            "name": "Orderly",
            "version": "1",
            "chainId": chainId,
            "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
        },
        "message": _message,
        "primaryType": "Registration",
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Registration": [
                {"name": "brokerId", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "timestamp", "type": "uint64"},
                {"name": "registrationNonce", "type": "uint256"},
            ],
        },
    }

    _signature = self.get_wallet_signature(message=message)
    payload = {"message": _message, "signature": _signature, "userAddress": userAddress}
    check_required_parameters(
        [
            [brokerId, "brokerId"],
            [chainId, "chainId"],
            [registrationNonce, "registrationNonce"],
            [userAddress, "userAddress"],
        ]
    )
    return self._request("POST", "/v1/register_account", payload=payload)


def get_orderly_key(self, account_id: str, orderly_key: str):
    """Get Orderly Key
    Limit: 10 requests per 1 second per IP address

    GET /v1/get_orderly_key

    Check the validity of an Orderly access key attached to the account.

    Args:
        account_id(string): The account id of the user
        orderly_key(string): The public key of the Orderly access key

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/get-orderly-key
    """
    check_required_parameters(
        [[account_id, "account_id"], [orderly_key, "orderly_key"]]
    )
    payload = {"account_id": account_id, "orderly_key": orderly_key}
    return self._request("GET", "/v1/get_orderly_key", payload=payload)


def add_orderly_key(
    self,
    brokerId: str,
    chainId: int,
    orderlyKey: str,
    scope: str,
    timestamp: int,
    expiration: int,
    userAddress: str,
    **kwargs
):
    """Add Orderly Key

    Limit: 10 requests per 1 second per IP address

    POST /v1/orderly_key

    Adds an Orderly access key to an account.
    Args:
        message(json): Message object containing the message that is signed by the wallet owner
        message.brokerId(string): Broker ID
        message.chainId(number): Chain ID of registering chain (within those that are supported by the Network)
        message.orderlyKey(string):  The public key of the Orderly access key
        message.scope(string): Valid nonce from Get Registration Nonce
        message.timestamp(timestamp):   timestamp in UNIX milliseconds
        message.expiration(timestamp):	The signature generated by signing the message object via EIP-712
        signature(string): The signature generated by signing the message object via EIP-712
        userAddress(string):   The address of the wallet signing the message object via EIP-712
    Optional Args:
        tag(string): An optional tag of string values


    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/add-orderly-key
    """
    _message = {
        "brokerId": brokerId,
        "chainId": chainId,
        "orderlyKey": orderlyKey,
        "scope": scope,
        "timestamp": int(get_timestamp()),
        "expiration": expiration,
    }
    message = {
        "domain": {
            "name": "Orderly",
            "version": "1",
            "chainId": chainId,
            "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
        },
        "message": _message,
        "primaryType": "AddOrderlyKey",
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "AddOrderlyKey": [
                {"name": "brokerId", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "orderlyKey", "type": "string"},
                {"name": "scope", "type": "string"},
                {"name": "timestamp", "type": "uint64"},
                {"name": "expiration", "type": "uint64"},
            ],
        },
    }
    _signature = self.get_wallet_signature(message=message)
    payload = {
        "message": _message,
        "signature": _signature,
        "userAddress": userAddress,
        **kwargs,
    }
    check_required_parameters(
        [
            [brokerId, "brokerId"],
            [chainId, "chainId"],
            [orderlyKey, "orderlyKey"],
            [scope, "scope"],
            [timestamp, "timestamp"],
            [expiration, "expiration"],
            [userAddress, "userAddress"],
        ]
    )
    return self._request("POST", "/v1/orderly_key", payload=payload)

def remove_orderly_key(self, orderly_key: str):
    """Remove Orderly Key
    Limit: 10 requests per 1 second per IP address

    POST /v1/remove_orderly_key

    Remove an Orderly access key from the account.

    Args:
        orderly_key(string): The public key of the Orderly access key

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/public/remove-orderly-key
    """
    check_required_parameters([[orderly_key, "orderly_key"]])
    payload = {"orderly_key": orderly_key}
    return self._sign_request("POST", "/v1/client/remove_orderly_key", payload=payload)

def update_leverage_configuration(self, leverage: int):
    """Update leverage setting

    Limit: 5 requests per 60 second per user

    POST /v1/client/leverage

    Choose maximum leverage for futures mode

    Args:
        leverage(number): One of 1,2,3,4,5,10

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/update-leverage-setting
    """
    check_required_parameters([[leverage, "leverage"]])
    payload = {"leverage": leverage}
    return self._sign_request("POST", "/v1/client/leverage", payload=payload)


def get_current_holdings(self, all: bool = None):
    """Get current holding

    Limit: 10 requests per 1 seconds

    GET /v1/client/holding

    Get the current summary of user token holdings.

    Optional Args:
        all(enum):	 true/false. If true then will return all token even if balance is empty.

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-current-holding
    """
    payload = {"all": all}
    return self._sign_request("GET", "/v1/client/holding", payload=payload)


def get_account_information(self):
    """Get account information

    Limit: 10 requests per 60 seconds

    Get basic account information including current user fee rates.

    GET /v1/client/info

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-account-information
    """
    return self._sign_request("GET", "/v1/client/info")


def set_maintenance_config(self, maintenance_cancel_order_flag: bool):
    """Set maintenance config
    Limit: 10 requests per 60 seconds

    Set the user config for whether the system should automatically cancel the user's pending orders during maintenance.

    POST /v1/client/maintenance_config

    Args:
       maintenance_cancel_order_flag : if true, system will cancel all of user's pending orders during maintenance.

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/set-maintenance-config
    """
    check_required_parameters(
        [[maintenance_cancel_order_flag, "maintenance_cancel_order_flag"]]
    )
    _payload = {"maintenance_cancel_order_flag": maintenance_cancel_order_flag}
    return self._sign_request("POST", "/v1/client/maintenance_config", payload=_payload)

def get_user_daily_statistics(self, start_date: str, end_date: str):
    """Get User Daily Statistics
    Limit 10 requests per 60 seconds

    GET /v1/client/statistics/daily

    Get user daily statistics of assets/pnl/volume.

    Args:
        start_date(string): Format YYYY-MM-DD.
        end_date(string): Format YYYY-MM-DD.
    Optional Args:
        page(number)
        size(number)

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-user-daily-statistics
    """
    check_required_parameters([[start_date, "start_date"], [end_date, "end_date"]])
    payload = {"start_date": start_date, "end_date": end_date}
    return self._sign_request("GET", "/v1/client/statistics/daily", payload=payload)

def get_user_daily_volume(self, start_date: str, end_date: str):
    """Get user daily volume
    Limit 10 requests per 60 seconds

    GET /v1/volume/user/daily

    Get the daily historical breakdown of the user trading volume.
    The provided start_date/end_date has to be within a 90-day range.

    Args:
        start_date(string): Format YYYY-MM-DD.
        end_date(string): Format YYYY-MM-DD.

    The provided start_date/end_date has to be within a 90-day range.

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-user-daily-volume
    """
    check_required_parameters([[start_date, "start_date"], [end_date, "end_date"]])
    payload = {"start_date": start_date, "end_date": end_date}
    return self._sign_request("GET", "/v1/volume/user/daily", payload=payload)


def get_user_volume_statistics(self):
    """Get user volume statistics

    Limit 10 requests per 60 seconds

    GET /v1/volume/user/stats

    Get the latest volume statistics of the user.

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-user-volume-statistics
    """
    return self._sign_request("GET", "/v1/volume/user/stats")


def get_current_orderlykey_info(self, **kwargs):
    """Get current Orderly key info

    Limit 10 requests per 60 seconds

    GET /v1/client/key_info

    Retrieve all the registered Orderly key pairs under the account.

    Optional Args:
        key_status(string): Filter by the status of the key (ACTIVE / REMOVING / REMOVED)

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-current-orderly-key-info
    """
    payload = {**kwargs}
    return self._sign_request("GET", "/v1/client/key_info", payload=payload)


def get_orderlykey_ip_restriction(self, orderly_key: str):
    """Get Orderly Key IP restriction

    Limit 10 requests per 60 seconds

    GET /v1/client/orderly_key_ip_restriction

    Retrieves the current IP restriction of a particular Orderly key.

    Args:
        orderly_key(string): The Orderly Key to query the IP restriction list

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/get-orderly-key-ip-restriction

    """
    check_required_parameters([[orderly_key, "orderly_key"]])
    payload = {"orderly_key": orderly_key}
    return self._sign_request(
        "GET", "/v1/client/orderly_key_ip_restriction", payload=payload
    )


def set_orderlykey_ip_restriction(self, orderly_key: str, ip_restriction_list: str):
    """Set Orderly key IP restriction

    Limit: 10 requests per 60 seconds

    POST /v1/client/set_orderly_key_ip_restriction

    Set the IP restrictions of a particular Orderly key under the account.

    Args:
        orderly_key(string): The Orderly Key to set the IP restriction list.
        ip_restriction(string): List of IP or IP ranges (comma separated), that will be allowed to place orders with the orderly_key.

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/set-orderly-key-ip-restriction
    """
    check_required_parameters(
        [[orderly_key, "orderly_key"], [ip_restriction_list, "ip_restriction_list"]]
    )
    payload = {"orderly_key": orderly_key, "ip_restriction_list": ip_restriction_list}
    return self._sign_request(
        "POST", "/v1/client/set_orderly_key_ip_restriction", payload=payload
    )


def reset_orderlykey_ip_restriction(self, orderly_key: str, reset_mode: str):
    """Reset orderly key IP restriction
    Limit: 10 requests per 60 seconds

    POST /v1/client/reset_orderly_key_ip_restriction

    Reset the IP restriction of a particular Orderly key under the account.

    Args:
        orderly_key(string): The Orderly Key to set the IP restriction list.
        reset_mode(string): The new mode of the IP restriction for this Orderly Key (ALLOW_ALL_IPS, DISALLOW_ALL_IPS).

    https://orderly.network/docs/build-on-evm/evm-api/restful-api/private/reset-orderly-key-ip-restriction
    """
    check_required_parameters(
        [[orderly_key, "orderly_key"], [reset_mode, "reset_mode"]]
    )
    payload = {"orderly_key": orderly_key, "reset_mode": reset_mode}

    return self._sign_request(
        "POST", "/v1/client/reset_orderly_key_ip_restriction", payload=payload
    )


def get_position_history(self, symbol: str = None, limit: int  = None):
    payload = {
        "symbol": symbol,
        "limit": limit
    }

    return self._sign_request(
        "GET", "/v1/position_history", payload=payload
    )