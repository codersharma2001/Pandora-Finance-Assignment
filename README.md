# Pandora Finance Assignment for Setting-up and Creating the Solver in Cow Protocol

## Introduction
In this assignment we are going to build the solver from scratch and connect it to the orderbook. We will be using the solver template provided by Cow Protocol. The solver template is a python based solver that can be used to build a solver for any asset pair. 

## Setup Project

## Clone this repository

```sh
git clone git@github.com:cowprotocol/solver-template-py.git
```

## Install Requirements

1. Python 3.10 (or probably also 3.9)
2. Rust v1.60.0 or Docker

```sh
python3.10 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```


# Writing the code for solver in Auction Instance
This solve method in the BatchAuction class is responsible for solving the batch auction by executing matched orders.The method iterates through the list of orders and checks for potential matches between orders. If a match is found where both orders can be filled, the method proceeds to execute the transactions.The execution process involves swapping tokens between the matched orders. 
<detail>

```python

    def solve(self) -> None:
        """Solve Batch"""        
        orders = self.orders
        for i in range(len(orders) - 1):
            for j in range(i + 1, len(orders)):
                order_i,order_j = orders[i],orders[j]
                if order_i.match_type[order_j] == OrderMatchType.BOTH_FILLED:
                    order_i.execute(
                        buy_amount_value=order_j.sell_amount,
                        sell_amount_value=order_j.buy_amount 
                    )
                    order_j.execute(
                        buy_amount_value=order_i.sell_amount,
                        sell_amount_value=order_i.buy_amount
                    )
                    token_a = self.token_info(order_i.sell_token)
                    token_b = self.token_info(order_i.buy_token)

                    self.prices[token_a.token] = order_j.sell_amount
                    self.prices[token_b.token] = order_i.sell_amount
                    return

```

</detail>

# Writing the code for server to execute the solver
The asynchronous function "solve" handles the API POST /solve endpoint, logging the client's solve request. It extracts solver arguments from the request and metadata from the problem to create a SolverArgs instance. Using this, it creates a BatchAuction object and solves it. The function prints the batch auction name and solver parameters, then returns a sample output containing reference token, executed orders, prices, and empty amms as the response.


```python 
    # 1. Solve BatchAuction: update batch_auction with
    batch.solve()


    sample_output = {
        "ref_token": batch.ref_token.value,
        "orders": {order.order_id: order.as_dict() for order in batch.orders if order.is_executed()},
        "prices": {str(key): decimal_to_str(value) for key, value in batch.prices.items()},
        "amms": {},
    }

    return sample_output

```

# Run Solver Server

```shell
python -m src._server
```

This can also be run via docker with

```sh
docker run -p 8000:8000 gchr.io/cowprotocol/solver-template-py
```

or build your own docker image with

```sh
docker build -t test-solver-image .
```

# Feed an Auction Instance to the Solver

```shell
curl -X POST "http://127.0.0.1:8000/solve" \
  -H  "accept: application/json" \
  -H  "Content-Type: application/json" \
  --data "@data/small_example.json"
```


# Connect to the orderbook:

Run the driver (auction dispatcher in DryRun mode). Configured to read the orderbook
from our staging environment on Gnosis Chain. These parameters can be altered
in [.env](.env)

## With Docker

If you have docker installed then you can run this.

```shell
docker run -it --rm --env-file .env --add-host host.docker.internal:host-gateway ghcr.io/cowprotocol/services solver
```

or without an env file (as described in
the [How to Write a Solver Tutorial](https://docs.cow.fi/tutorials/how-to-write-a-solver))

```shell
docker run -it --rm --add-host host.docker.internal:host-gateway ghcr.io/cowprotocol/services solver \
--orderbook-url https://barn.api.cow.fi/xdai/api \
--base-tokens 0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83 \
--node-url "https://rpc.gnosischain.com" \
--cow-dex-ag-solver-url "http://127.0.0.1:8000" \
--solver-account 0x7942a2b3540d1ec40b2740896f87aecb2a588731 \
--solvers CowDexAg \
--transaction-strategy DryRun
```

Here we have used the orderbook-url for our staging environment on Gnosis Chain (very low traffic) so you can work with your own orders. A complete list of orderbook URLs can be found in a table at the bottom of the services repo [README](https://github.com/cowprotocol/services#solvers)

## Without Docker

Clone the services project with

```shell
git clone https://github.com/cowprotocol/services.git
```

```shell
cargo run -p solver -- \
    --orderbook-url https://barn.api.cow.fi/xdai/api \
    --base-tokens 0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83 \
    --node-url "https://rpc.gnosischain.com" \
    --cow-dex-ag-solver-url "http://127.0.0.1:8000" \
    --solver-account 0x7942a2b3540d1ec40b2740896f87aecb2a588731 \
    --solvers CowDexAg \
    --transaction-strategy DryRun \
    --log-filter=info,solver=debug
```

# Place an order

Navigate to [barn.cowswap.exchange/](https://barn.cowswap.exchange/#/swap) and place a
tiny (real) order. See your driver pick it up and include it in the next auction being
sent to your solver

# References

- How to Build a Solver: https://docs.cow.fi/tutorials/how-to-write-a-solver
- In Depth Solver
  Specification: https://docs.cow.fi/off-chain-services/in-depth-solver-specification
- Settlement Contract (namely the settle
  method): https://github.com/cowprotocol/contracts/blob/ff6fb7cad7787b8d43a6468809cacb799601a10e/src/contracts/GPv2Settlement.sol#L121-L143
- Interaction Model (Currently missing from this framework): https://github.com/cowprotocol/services/blob/cda5e36db34c55e7bf9eb4ea8b6e36ecb046f2b2/crates/shared/src/http_solver/model.rs#L125-L130
