from orderly_evm_connector.lib.utils import check_required_parameters, get_timestamp
from orderly_evm_connector.lib.utils import check_enum_parameter,get_withdraw_settle_verifyingcontract
from orderly_evm_connector.lib.enums import WalletSide, AssetStatus


def get_asset_history(
    self,
    token: str = None,
    side: str = None,
    status: str = None,
    start_t: int = None,
    end_t: int = None,
    page: int = None,
    size: int = None,
):
    """Get asset history

    Limit 10 requests per 60 seconds

    GET /v1/asset/history

    Get asset history, including token deposits/withdrawals.

    Optional Args:
        token(string):	            token name you want to search
        side(string):	            DEPOSIT/WITHDRAW
        status(string):	        NEW/CONFIRM/PROCESSING/COMPLETED/FAILED
        start_t(timestamp):	    start time range that wish to query, noted the time stamp is 13-digits timestamp.
        end_t(timestamp):       end time range that wish to query, noted the time stamp is 13-digits timestamp.
        page(number):           (default: 1)	the page you wish to query.
        size(number):           (default: 25)
    """
    if status:
        check_enum_parameter(status, AssetStatus)
    if side:
        check_enum_parameter(side, WalletSide)

    payload = {
        "token": token,
        "side": side,
        "status": status,
        "start_t": start_t,
        "end_t": end_t,
        "page": page,
        "size": size,
    }

    return self._sign_request("GET", "/v1/asset/history", payload=payload)


def get_withdraw_nonce(self):
    """Get Withdrawal Nonce
    Limit 10 requests per 1 seconds

    GET /v1/withdraw_nonce

    Retrieve a nonce used for requesting a withdrawal on Orderly Network. Each nonce can only be used once.

    https://docs-api-evm.orderly.network/#restful-api-private-get-withdrawal-nonce
    """

    return self._sign_request("GET", "/v1/withdraw_nonce")


def withdraw_request(
    self,
    brokerId: str,
    chainId: int,
    receiver: str,
    token: str,
    amount: str,
    withdrawNonce: int,
    userAddress: str,
    # verifyingContract: str,
):
    """Create Withdraw Request
    
    Limit: 10 requests per 1 second per IP address

    POST /v1/withdraw_request
    
    This API will throw an error with message 22 - Cross-chain withdrawal required for this withdrawal request. if allow_cross_chain_withdrawal is false while the request is a cross-chain request.

    Args
    message(JSON): Message object containing the message that is signed by the wallet owner
    message.brokerId(string): Broker ID
    message.allowCrossChainWithdrawal(boolean)
    message.chainId(int): Chain ID of registering chain (within those that are supported by the Network)
    message.receiver(string): Address of the receiver, which should be equal to the address of the account.
    message.token(string): The string representation of the token that is being withdrawn (eg "USDC")
    message.amount(int): Amount of tokens to be withdrawn
    message.withdrawNonce(int): Valid withdrawal nonce from Get withdrawal nonce
    message.timestamp(timestamp): current timestamp in UNIX milliseconds
    signature(string): The signature generated by signing the message object via EIP-712
    userAddress(string): The address of the wallet signing the message object via EIP-712
    # verifyingContract(string): Address of the Orderly Network ledger contract

    https://docs-api-evm.orderly.network/#restful-api-private-create-withdraw-request

    """
    check_required_parameters(
        [
            [brokerId, "brokerId"],
            [chainId, "chainId"],
            [receiver, "receiver"],
            [token, "token"],
            [amount, "amount"],
            [withdrawNonce, "withdrawNonce"],
            [userAddress, "userAddress"],
            # [verifyingContract, "verifyingContract"],
        ]
    )
    _message = {
        "brokerId": brokerId,
        "chainId": chainId,
        "receiver": receiver,
        "token": token,
        "amount": amount,
        "withdrawNonce": withdrawNonce,
        "timestamp": int(get_timestamp()),
        "type": "Withdraw",
    }
    verifyingContract = get_withdraw_settle_verifyingcontract(self.orderly_testnet)
    message = {
        "domain": {
            "name": "Orderly",
            "version": "1",
            "chainId": chainId,
            "verifyingContract": verifyingContract,
        },
        "message": _message,
        "primaryType": "Withdraw",
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "Withdraw": [
                {"name": "brokerId", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "receiver", "type": "address"},
                {"name": "token", "type": "string"},
                {"name": "amount", "type": "uint256"},
                {"name": "withdrawNonce", "type": "uint64"},
                {"name": "timestamp", "type": "uint64"},
            ],
        },
    }
    _signature = self.get_wallet_signature(message=message)
    payload = {
        "message": _message,
        "signature": _signature,
        "userAddress": userAddress,
        "verifyingContract": verifyingContract,
    }
    return self._sign_request("POST", "/v1/withdraw_request", payload=payload)
