"""
This file defines problem, solution, and solver parameters schemas,
using pydantic that is then used to validate IO and autogenerate
documentation.
"""

from typing import Dict, List, Optional, Union

from enum import Enum
from pydantic import BaseModel, Field

# Example instance to use in the autogenerated API documentation.

example_instance = {
    "metadata": {
        "environment": "xDAI",
        "auction_id": 1,
        "gas_price": 4850000000.0,
        "native_token": "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
    },
    "tokens": {
        "0x6b175474e89094c44da98b954eedeac495271d0f": {
            "decimals": 18,
            "alias": "DAI",
            "external_price": 0.00021508661247926934,
            "normalize_priority": 0,
            "internal_buffer": "8213967696976545926330",
        },
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {
            "decimals": 6,
            "alias": "USDC",
            "external_price": 214890212.34875953,
            "normalize_priority": 0,
            "internal_buffer": "2217249148",
        },
        "0xdac17f958d2ee523a2206206994597c13d831ec7": {
            "decimals": 6,
            "alias": "USDT",
            "external_price": 214523029.31427807,
            "normalize_priority": 0,
            "internal_buffer": "4227015605",
        },
        "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
            "decimals": 18,
            "alias": "WETH",
            "external_price": 1.0,
            "normalize_priority": 1,
            "internal_buffer": "895880027660372311",
        },
    },
    "orders": {
        "0": {
            "sell_token": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "buy_token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "sell_amount": "4693994755140375611596",
            "buy_amount": "1000000000000000000",
            "allow_partial_fill": False,
            "is_sell_order": False,
            "fee": {
                "amount": "103079335446226157568",
                "token": "0x6b175474e89094c44da98b954eedeac495271d0f",
            },
            "cost": {
                "amount": "6657722265694875",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "is_liquidity_order": False,
        },
        "1": {
            "sell_token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "buy_token": "0x6b175474e89094c44da98b954eedeac495271d0f",
            "sell_amount": "1000000000000000000",
            "buy_amount": "4692581049969374626065",
            "allow_partial_fill": False,
            "is_sell_order": True,
            "fee": {
                "amount": "23212472598551576",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "cost": {
                "amount": "6657722265694875",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "is_liquidity_order": True,
        },
    },
    "amms": {
        "01": {
            "kind": "ConstantProduct",
            "reserves": {
                "0x6b175474e89094c44da98b954eedeac495271d0f": "44897630044876228891318837",
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "9626911517235794223708",
            },
            "fee": "0.003",
            "cost": {
                "amount": "9507044675748200",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "mandatory": False,
        },
        "02": {
            "kind": "ConstantProduct",
            "reserves": {
                "0x6b175474e89094c44da98b954eedeac495271d0f": "84903768350604287941150958",
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": "18233677073990818080605",
            },
            "fee": "0.003",
            "cost": {
                "amount": "9507044675748200",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "mandatory": False,
        },
        "03": {
            "kind": "WeightedProduct",
            "reserves": {
                "0x6b175474e89094c44da98b954eedeac495271d0f": {
                    "balance": "1191959749018354276837",
                    "weight": "0.4",
                },
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
                    "balance": "392171457910841840",
                    "weight": "0.6",
                },
            },
            "fee": "0.0025",
            "cost": {
                "amount": "12047450379000000",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "mandatory": False,
        },
        "04": {
            "kind": "WeightedProduct",
            "reserves": {
                "0x6810e776880c02933d47db1b9fc05908e5386b96": {
                    "balance": "21330539255670269346",
                    "weight": "0.25",
                },
                "0x6b175474e89094c44da98b954eedeac495271d0f": {
                    "balance": "10928595376682871418747",
                    "weight": "0.25",
                },
                "0xba100000625a3754423978a60c9317c58a424e3d": {
                    "balance": "444658133648670940819",
                    "weight": "0.25",
                },
                "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {
                    "balance": "2237408990689298635",
                    "weight": "0.25",
                },
            },
            "fee": "0.01",
            "cost": {
                "amount": "12047450379000000",
                "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            },
            "mandatory": False,
        },
    },
}


# The following classes model the contents of a PROBLEM instance.
# They are used for input validation and documentation.


class TokenId(str):
    """Token unique identifier."""


class OrderId(str):
    """Order unique identifier."""


class AmmId(str):
    """AMM unique identifier."""


class BigInt(str):
    """Big integer (as a string)."""


class Decimal(str):
    """Decimal number (as a string)."""


class TokenInfoModel(BaseModel):
    """Token-specific data."""

    decimals: Optional[int] = Field(None, description="Number of decimals.")
    alias: Optional[str] = Field(None, description="Human-readable name (e.g. DAI).")
    normalize_priority: Optional[int] = Field(
        0,
        description="Priority for solution price vector normalization purposes "
        "(larger=higher preference).",
    )
    external_price: Optional[Decimal] = Field(None, description="External token price.")
    internal_buffer: Optional[BigInt] = Field(
        None, description="Internal token buffer."
    )


class TokenAmountModel(BaseModel):
    """Order/AMM cost and order fee."""

    amount: BigInt = Field(..., description="Amount.")
    token: TokenId = Field(..., description="Token.")


class OrderModel(BaseModel):
    """Order data."""

    sell_token: TokenId = Field(..., description="Token to be sold.")
    buy_token: TokenId = Field(..., description="Token to be bought.")
    sell_amount: BigInt = Field(
        ...,
        description="If is_sell_order=true indicates the maximum amount to sell, "
        "otherwise the maximum amount to sell in order to buy buy_amount.",
    )
    buy_amount: BigInt = Field(
        ...,
        description="If is_sell_order=false indicates the maximum amount to buy, "
        "otherwise the minimum amount to buy in order to sell sell_amount.",
    )
    allow_partial_fill: bool = Field(
        ...,
        description="If the order can sell/buy less than its maximum sell/buy amount.",
    )
    is_sell_order: bool = Field(
        ...,
        description="If it is a sell or buy order, changing the semantics of "
        "sell_amount/buy_amount accordingly.",
    )
    is_liquidity_order: Optional[bool] = Field(
        False,
        description="Liquidity orders (from market makers) can not receive surplus.",
    )
    has_atomic_execution: Optional[bool] = Field(
        False, description="Indicates, if the order needs to be executed atomically."
    )
    fee: Optional[TokenAmountModel] = Field(
        None,
        description="Fee contribution when order is matched "
        "(pro-rata for partial matching).",
    )
    cost: Optional[TokenAmountModel] = Field(
        None, description="Cost of matching the order."
    )

    class Config:
        """Includes example in generated openapi file"""

        schema_extra = {
            "example": {
                "sell_token": "0x6b175474e89094c44da98b954eedeac495271d0f",
                "buy_token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                "sell_amount": "4693994755140375611596",
                "buy_amount": "1000000000000000000",
                "allow_partial_fill": False,
                "is_sell_order": False,
                "fee": {
                    "amount": "103079335446226157568",
                    "token": "0x6b175474e89094c44da98b954eedeac495271d0f",
                },
                "cost": {
                    "amount": "6657722265694875",
                    "token": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                },
                "is_liquidity_order": False,
            }
        }


class AmmKindEnum(str, Enum):
    """AMM kind."""

    CONSTANT_PRODUCT = "ConstantProduct"
    WEIGHTED_PRODUCT = "WeightedProduct"
    STABLE = "Stable"
    CONCENTRATED = "Concentrated"


class ConstantProductReservesModel(BigInt):
    """Tokens and balances of constant-product AMMs."""


class WeightedProductReservesModel(BaseModel):
    """Tokens and balances+weights of weighted-product AMMs."""

    balance: BigInt = Field(..., description="Token balance in AMM.")
    weight: BigInt = Field(..., description="Weight of the token.")


class AmmModel(BaseModel):
    """AMM data."""

    kind: AmmKindEnum = Field(..., description="AMM type.")
    reserves: Optional[Dict[
        TokenId, Union[ConstantProductReservesModel, WeightedProductReservesModel]
    ]] = Field(None, description="AMM tokens and balances.")
    fee: Optional[Decimal] = Field(None, description="AMM trading fee (e.g. 0.003 for 0.3% fee).")
    cost: Optional[TokenAmountModel] = Field(
        None, description="Cost of using the pool."
    )


class MetadataModel(BaseModel):
    """Batch auction metadata."""

    environment: Optional[str] = Field(
        None, description="Runtime/blockchain environment."
    )
    auction_id: Optional[str] = Field(..., description="Max Number of executed orders")
    gas_price: Optional[float] = Field(..., description="Current Gas price")
    native_token: Optional[TokenId] = Field(..., description="Wrapped Native Token")


class BatchAuctionModel(BaseModel):
    """Batch auction instance data."""

    tokens: Dict[TokenId, TokenInfoModel] = Field(..., description="Tokens.")
    orders: Dict[OrderId, OrderModel] = Field(..., description="Orders.")
    metadata: MetadataModel = Field({}, description="Metadata.")
    amms: Optional[Dict[AmmId, AmmModel]] = Field({}, description="AMMs")

    class Config:
        """Includes example in generated openapi file"""

        schema_extra = {"example": example_instance}


# The following classes model the contents of a SOLUTION instance.
# They are used for input validation and documentation.


class ExecutedOrderModel(OrderModel):
    """Executed order data (solution)."""

    exec_buy_amount: BigInt = Field(..., description="Executed buy amount.")
    exec_sell_amount: BigInt = Field(..., description="Executed sell amount.")


class ExecPlanCoordsModel(BaseModel):
    """Execution plan coordinates."""

    sequence: int = Field(..., description="Sequence index.")
    position: int = Field(..., description="Position within the sequence.")
    internal: Optional[bool] = Field(False, description="Using internal liquidity")


class AmmExecutionModel(BaseModel):
    """AMM settlement information."""

    sell_token: TokenId = Field(..., description="Token sold by the AMM.")
    buy_token: TokenId = Field(..., description="Token bought by the AMM.")
    exec_sell_amount: BigInt = Field(..., description="Executed sell amount.")
    exec_buy_amount: BigInt = Field(..., description="Executed buy amount.")
    exec_plan: Optional[ExecPlanCoordsModel] = Field(
        None, description="Execution plan coordinates."
    )


class ExecutedAmmModel(AmmModel):
    """List of AMM executions."""

    execution: Optional[List[AmmExecutionModel]] = Field(
        None, description="AMM settlement data."
    )


class InteractionData(BaseModel):
    """Interaction data."""

    target: TokenId = Field(
        ..., description="Target contract address to interact with."
    )
    value: BigInt = Field(
        ..., description="Value of native token, e.g. amount eth in eth transfer"
    )
    call_data: bytes = Field(..., description="Interaction encoding.")


class SettledBatchAuctionModel(BaseModel):
    """Settled batch auction data (solution)."""

    orders: Dict[OrderId, ExecutedOrderModel] = Field(
        ..., description="Executed orders."
    )
    prices: Dict[TokenId, BigInt] = Field(
        ..., description="Settled price for each token."
    )
    amms: Dict[AmmId, ExecutedAmmModel] = Field(..., description="Executed AMMs.")

    interaction_data: List[InteractionData] = Field(
        description="List of interaction data.", default=[]
    )
