Write a program in any language called `vault`.

When run with: `./vault <path>`

1. Creates and listens on an Unix domain socket at path `path`.
   It's fine to be able to handle only one connection at at time.

2. Commands will be sent through that socket as a JSON document on a single line (terminated with `\n`).
   For example:

   ```js
   {"id":"1", "value":"this is the first command"}
   {"id":"2", "value":"this is the second command"}
   ```

3. The program is expected to reply with the result of a command through the same socket as a JSON document on a single line.
   For example:

   ```js
   {"id":"1", "value":"this is the result of the first command"}
   {"id":"2", "value":"this is the result of the second command"}
   ```

   It's fine to only handle one request at a time.
   Responses must have the same `id` as the request that it serves.

Only one single command needs to be implemented:

```js
{
	"id": "Some id",
	"type": "sign_transfer",
	"from_address": "ETH address",
    "to_address": "ETH address",
	"amount": "Amount as string"
}
```

Expected response:

```js
{
	"id": "Some id",
	"tx": "Tx string"
}
```

Note: the example uses multiple lines for readability only.
Requests and responses are always sent in a single line.

The value of `tx` must be a valid signed ETH transaction for _testnet_, such that when it is broadcasted with: https://ropsten.etherscan.io/pushTx,
an `amount` of ETH will be sent from `from_address` to `to_address` in _testnet_.

Note: the program can only construct and sign a transaction, it must not broadcast the transaction.

Fees should already be included in `amount` and the program should just use the current fee value in the network.
For example if `amount` is 1 ETH and the current fee is 0.1 ETH, the receiver would receive 0.9 ETH.

The private key for `from_address` is stored in a file with the same name as the address in the same directory as the program.
Just create one for testing. You can decide the format.

Any libraries can be used and the program can connect to an _online_ remote ETH node if needed (see https://infura.io/)
However, it cannot make use of any other web API.