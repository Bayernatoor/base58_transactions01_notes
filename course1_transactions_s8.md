# Section 8 - Script Hashes and Segwit

## Review:

'Native Segwit' standard script: P2WSH
    - segwit version of P2SH

Segwit bytes cost less. Which actually results in a sneaky blocksize increase (1mb -> 4mb)
    - segwit bytes cost lost (less weight)
txid are caculated differently
malleability --> one of the reasons segwit was introduced.


## P2WSH refrsh:


P2WSH: 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934
TXID: 0f198ec61d2e1e8b86e5dd9c56d97d26a00c31d5d8c51b6d919b028fdd9f77ee

TX1: lock funds to our P2WSH script (scriptPubKey output), using a Legacy transaction 
version: 01000000
inputs: 01
    txid: 0f198ec61d2e1e8b86e5dd9c56d97d26a00c31d5d8c51b6d919b028fdd9f77ee
    vout: 00000000
    scriptSig: 2e 
               15686176652066756e2073746179696e6720706f6f72 
               *1715686176652066756e2073746179696e6720706f6f7287* --> Redeem script
    sequence: feffffff
outputs: 02
    amount: 48d5f50500000000  
    scriptPubKey: 22 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934
locktime: 00000000 

---> txid: TX1ID 


TX2: spends the P2WSH! (segwit tx) --> Spends the scriptPubKey from TX1
version: 01000000 
segwit marker+flag: 0001
inputs: 01
    txid: TX1D
    vout: 00000000
    scriptSig: 00
    sequence: feffffff
outputs: 01
    amount: 60d1f50500000000
    scriptPubKey: 22 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934
witness data:
    02
    15686176652066756e2073746179696e6720706f6f72 
    *1715686176652066756e2073746179696e6720706f6f7287* --> this is the redeemScript but is called witness script in segwit
locktime: 00000000


### The P2WSH script:
    
    scriptPubKey: <length22> [<00> <length20> <data ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934>]

Witness stacks

    unlocking script: 15686176652066756e2073746179696e6720706f6f72 
    locking script: 17 [15686176652066756e2073746179696e6720706f6f7287]
    P2WSH: 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934

## Making a new P2WSH Script:

- first time our script was a "phrase" and we compared the phrase to itself to unlock it (not very safe)
- This time let's use some crypto.


Unlocking script: b'this is base58 yall' --> 13 74686973206973206261736535382079616c6c
Locking script (always public): OP_SHA256 ... OP_EQUAL
    asm: OP_SHA256 <affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e73> OP_EQUAL
            a8     20 affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e73 87

### Clean scripts:

Unlocking script: 1374686973206973206261736535382079616c6c
new original locking scripting: a820affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e7387


Lets take our orginal script and make it a P2WSH

    P2WSH -> <0> <sha256 of our original script>
            asm: <0> <20 e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1>
            0020e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1
    The above is now a P2WSH
{
  "asm": "0 e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1",
  "desc": "addr(bc1qu04njevcrk7tk9hywwqmm2pmh46vzsrruxr2mamuprctpc9zrtss6l24ut)#wtnnyhf4",
  "address": "bc1qu04njevcrk7tk9hywwqmm2pmh46vzsrruxr2mamuprctpc9zrtss6l24ut",
  *"type": "witness_v0_scripthash",*
  "p2sh": "3LAmNTVXjhGp5Pmu9zVWu8vTb7H8oXJShx"
}

### Making our transactions:

We need an address to send bitcoin to
    decoding the P2WSH script above will return a 
    --> bc1qu04njevcrk7tk9hywwqmm2pmh46vzsrruxr2mamuprctpc9zrtss6l24ut

Bech32 bitcoin address
    - bech32 is an encoding and is a replacement for base58
    - there are 4 parts to a bech32 address
        hrp: human readable part (mainnet = bc, testnet = tb, regtest = bcqt)
        separator: 1
        data
        checksum

        bc 1 qu04njevcrk7tk9hywwqmm2pmh46vzsrruxr2mamuprctpc9zrtss 6l24ut

Base58 bitcoin address:
    - flag(P2SH/P2PKH, mainnet/testnet)
    - data itself
    - checkum
    
    base58(flag|data|checksum) -> bitcoin address

##### building a Bech32 address:

HRP: bc
Separator: 1 (5 bits)
    witness version 00 (1 byte?
hash (data):  e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1
checksum: last 6 chars


TX1: (locking tx) ... send bitcon and lock it to our custom P2WSH script
TXD_of_tx1

TX2: spend P2WSH tx above
version: 01000000
marker+flag: 0001
inputs: 01
    txid:  ..
    vout: 00000000
    scriptSig:a 00
    sequenece: feffffff
outputs: 01
    amount: 18ddf50500000000
    scriptPubKey 22 0020e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1
witness stacks:
    02
    unlock: 13 74686973206973206261736535382079616c6c
    witness script: 23 a820affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e7387
locktime: 00000000

## Backwards Compatible Segwit AKA Nested Segwit:

Take the P2WSH and make it backwards compatible. 

1. Take out P2WSH and wrap it into a P2SH

Unlocking Script: b'have fun staying poor'
    length + hex: 15 686176652066756e2073746179696e6720706f6f72
Locking Script: OP_SHA256  <c4c648b19dfd0c567fd2e60022d871e70cf50370e126a0eac839e16126152455> OP_EQUAL
    full:  a820c4c648b19dfd0c567fd2e60022d871e70cf50370e126a0eac839e1612615245587
P2WSH: <0> <sha256 locking script>
    fb582c06298e0e5e6364ef57a349422b3961c0c923ed1f7f18c627db67bf3e7d
P2SH-P2WSH: <OP_HASH160> len+<hash of our P2WSH> OP_EQUAL
    Script: a9 14  a08aafe37130d39354494c69b0c565c2cb945cb9 87
    complete P2SH-P2WSH: a914a08aafe37130d39354494c69b0c565c2cb945cb987

TX3 - lock bitcoin to a P2SH-P2WSH script.
Version: 02000000
marker+flag: 0001
input: 01
    txid: txid to spend
    vout: 00000000
    scriptSig: 00
    sequence: feffffff
outputs: 01
    amount: 30d9f50500000000
    scriptPubKey:  17 a914a08aafe37130d39354494c69b0c565c2cb945cb987 <-- P2SH-P2WSH script
witness stacks:
02
    15 686176652066756e2073746179696e6720706f6f72
    23 a820affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e7387
locktime: 00000000


### spending from our P2SH-P2WSH script (the above output)

TX4:
version 02000000
marker+flag: 00001
input: 01
    txid: txid_to_spend_utxo_of_tx3
    vout: 00000000
    scriptPubKey:23 220020e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1 (redeemScript)
    sequence: feffffff:
output: 01
    amount: 48d5f50500000000
    scriptPubKey:  22 0020e3eb3965981dbcbb16e47381bda83bbd74c14063e186adf77c08f0b0e0a21ae1
witness data: (P2WSH)
02
    15 686176652066756e2073746179696e6720706f6f72
    <witness script> 23 a820affb7035b385c7e8608d209498cd85c60eddadf4e2e50356f601289198219e7387
locktime: 00000000


## Fun facts about segwit:


If you decode the P2WSH or the P2SH-P2WSH script, bitcoin-cli returns the same P2SH address:


```
bc decodescript 0020fb582c06298e0e5e6364ef57a349422b3961c0c923ed1f7f18c627db67bf3e7d (P2WSH)
{
  "asm": "0 fb582c06298e0e5e6364ef57a349422b3961c0c923ed1f7f18c627db67bf3e7d",
  "desc": "addr(bc1qldvzcp3f3c89ucmyaat6xj2z9vukrsxfy0k37lccccnakeal8e7sskw3ax)#5kd9237f",
  "address": "bc1qldvzcp3f3c89ucmyaat6xj2z9vukrsxfy0k37lccccnakeal8e7sskw3ax",
  "type": "witness_v0_scripthash",
  "p2sh": "3A1QqLZoktFtYfqbeTjEXmAW6PWTbr8iJE"
}
```

OR

```
bc decodescript a9145b3b9e3b72a5abdbdbbf2c14fe02bd0254c3e2a087 (P2SH-P2WSH)
{
  "asm": "OP_HASH160 5b3b9e3b72a5abdbdbbf2c14fe02bd0254c3e2a0 OP_EQUAL",
  "desc": "addr(3A1QqLZoktFtYfqbeTjEXmAW6PWTbr8iJE)#szrq9lfq",
  "address": "3A1QqLZoktFtYfqbeTjEXmAW6PWTbr8iJE",
  "type": "scripthash"
}
```



