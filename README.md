# Vault

This is a test for applying `numoney` internship. The full problem statement is at `problem_statement.md`.

## Some assumptions
1. I assume the unit for `amount` from the input is `ether`.

2. I assume the input format is valid. My program doesn't check the validity of the input and might get run time error if the input is not valid.

3. I assume that the `Tx` response is not broadcasted immediately. There are some issues with multiple         commands within one query. Consider this scenario:
    
    1. `A` sends transaction to `B`          (in the transaction record, `A`'s nonce is `X`)
    2. `A` sends other transaction to `C`    (in the transaction record, `A`'s nonce is also `X` because the first transaction has not yet broadcasted)
    3. broadcast the first transaction (`A` to `B`), now `A`'s nonce becomes `X + 1`
    4. broadcast the second transaction (`A` to `C`). there is a mismatch, `A`'s nonce should be `X + 1`, but in the transaction record, it is `X`. The `Tx` is invalid and cannot be broadcasted.

## How to run
1. activate virtual environment:

    ```
    source venv/bin/activate
    ```

2. to run the program:

    ```
    ./vault <path>
    ```
    or alternatively
    
    ```
    python3 vault.py <path>
    ```

## Several Tests I make
1. I made two ropsten ethereum accounts for testing purposes. As instructed in problem_statement.md, I put      the private key of each account in a file with the name of the corresponding address. The two files are:

    - 0x1348E7E2b73993bEE501aa4413C193d3722f2b60
    - 0xdD8dA64825a55b3339fccEEE4c0443174517A666
    
2. I make two files as test datas:
    - query_one_time.txt
    - query_multiple_times.txt
    
3. I make `client.py`. This python code will send test files through UDS socket to `vault`.
    To test, do the following:
    1. run the vault program:
        ```
        ./vault <path>
        ```
    2. run client.py:
        ```
        python3 client.py <path>
        ```
        
    3. for each command, client.py will receive a response in the form of:
        ```
        received <response>
        ```
        
        broadcast `Tx` in the response to ropsten test network, then check the balance of the accounts involved.
    
    
