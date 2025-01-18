# Section 7 - Segwit

## OVERVIEW:

 - why segwit?
 - what is segwit
 - what does it change? 
    - The format tx
    - feerate calcs
    - new standard scripts
    - how txid is calculated
  - new standard scripts

-----

### Segwit 

Segwit is the bitcoin "omnibus bill"

A series of BIPS
    - changed scripts
    - changed sighashes
    - "" size of tx
    - "" how much data can fit in a block
    - "" the form of as transaction
    - How fees are calculated

Segwit = Segregated witness

segregated: separating things
witness: signature data (scripSig field)

--> We moved the ScriptSig field apart from other input data

### Legacy TX FORMAT

version
list of inputs
    txid
    output index(vout)
    scriptSig
    sequence
list out ouputs
    amount
    scriptPubKey
locktime

### SEGWIT TX FORMAT

version 
segwite market + flag
list of inputs
    txid
    output index (vout)
    scriptSig
    sequence
list of outputs
    amount
    scriptPubKey
list of "witness stacks"
    - count of items in the stack
    - stack items
locktime


### LEGACY TX TO SEGWIT
version: 01000000
segwit marker + flag: 0001
inputs: 01
    txid: f3963df3956aef1f67f7dd3c176672797e37c376b556337b814477e19730c3da
    vout: 00000000
    scriptSig: 00 
    sequence: feffffff
outputs: 01
    amount: 30d9f500000000
        scriptPubKey: 17 a914fb528f99064469fd19f1fc7f105a9fd324c7160787
witness stacks: 
02 (2 items in stack)
        15 6b6176626620566e207346179696e662072706f6f72
        17 156861762b6620566e207346179696e662072706f6f7287
locktime: 00000000



01000000000101f3963df3956aef1f67f7dd3c176672797e37c376b556337b814477e19730c3da0000000000feffffff0130d9f50000000017a914fb528f99064469fd19f1fc7f105a9fd324c71607870215686176652066756e2073746179696e6720706f6f7217156861762b6620566e207346179696e662072706f6f728700000000

*Decoding the Legacy TX vs the Segwit TX would result in the Segwit transaction having an empty scriptSig in the input field and a new txinwitness field above the sequence field.*

## Segwit Differences - TXIDs and vBytes

In segwit the TXID and the HASH will be different (unlike in legacy where the 2 match)

### Getting a TXID 

Legacy:
    sha256 of the sha256 of the txdata
    `sha256(sha256(data))`

Segwit:
    - When take all data in a segwit TX and run double sha256 on it you get the HASH, in segwit this is not the txid. 
    - The TXID is all the data that would exist in a legacy tx (do not include the segwit data) and then double sha256 hash that data, the result is the TXID. 

### Sizes:

Size: count of the bytes
vbytes: weight / 4
weight: ? 

#### LEGACY:
size: 129
vbytes: 129 
weight: size * 4 = 516

Feerate:
1000 sats fee

1000 sats / 129vbytes = 7.75sats/vByte

#### SEGWIT:
Size: 132 (3 bytes more then legacy)
    - segwit marker + flag + witness stack count byte
vbytes: 96
weight: 381

Formular for weight: 
    Any legacy bytes have a weight of 4!
    Any segwit bytes have a weight of 1!

##### calculating the weight: 

version: 01000000 -> 4 * 4 = 16
segwit marker + flag: 0001 -> 2 * 1 = 2
inputs: 01 -> 1 * 4 = 4
    txid: f3963df3956aef1f67f7dd3c176672797e37c376b556337b814477e19730c3da -> 32 * 4 = 128
    vout: 00000000 -> 4 * 4 = 16
    scriptSig: 00 -> 1 * 4 = 4
    sequence: feffffff -> 4 * 4 = 16
outputs: 01 -> 1 * 4 = 4
    amount: 30d9f500000000 -> 8 * 4 = 32
        scriptPubKey: 17 a914fb528f99064469fd19f1fc7f105a9fd324c7160787 -> 24 * 4 = 96
witness stacks: 
02 (2 items in stack) -> 1 * 1 = 1 
        15 6b6176626620566e207346179696e662072706f6f72 -> 22 * 1 = 22 
        17 156861762b6620566e207346179696e662072706f6f7287 -> 24 * 1 = 24
locktime: 00000000 -> 4 * 4 = 16 

Total weight = 381 


## Block Weight vs Block Size

Comparing the feerates


Segwit calc:
1000 sats fee
1000 sats / 96 vBytes = 10.417 sats/vByte

Legacy calc 
1000 sats fee
1000 sats / 129vbytes = 7.75sats/vByte

How come the segwit has a higher sats/Vbyte? This is related to Segwits blocksize increase:

- the number of vbytes allowed in a block is 1,000,000 (1MB)
- therefore, the total weight of a block maxes out at 4,000,000
- segwit allows you to get more bytes mined but it "costs" you less

This is why moving the signature data (witness data) apart is so great because it les you get real savings.

The byte weight between segwit and legacy is called the segwit discount is a 1:4 difference.


## TX Malleability & Why Lightning required Segwit:

Reminder:
    TXID for any transaction uses ONLY the legacy bytes when calculated. Which means none of the segwit data ends up in the txid.

When do we use TXIDs?
    - They go in transactions - they're a field in the inputs

What has segwit done? 
    - we've remoed the signature data (scriptSig) from the txid
    - why??
    - The move to segwit was necessary for lightning to work
    - the TXID not including the signature data was a key part of this.

The problem with putting signature data into a txid is that if the signature data changes, the txid will change
    - signatures can be changed and still be valid.
    - meaning, it's possible to produce a signature, give that sig to someone else and that person can change the signature and still have it be valied (the original SIG has to be valid)
    - THis isn't a security problem (original sig has to be valid) but it's a data integrity problem, due to the TXID being "malleable".

Lighting requires pre-signed transactions:
    - you work with another peer in lighting and part of it is the exchange of signatures for txs that your peer may broadcast in the future.
    - If I change the original tx that those funds are based on, you can screw over you channel partner, as they pre-signed tx won't be valid.

Ex: 
    1. Create a tx that has an output that is a 2 of 2 output. 
    2. Before you broadcast TX you get a signature from your peer that lets you spend that 2of2
    3. You have to give your peer a txid that they then give you a signature for.
    
    
TX1 --> before this is broadcasted, TX2 needs a valid sig
    inputs
    outputs
        2of2 output 

TX2 --> get a signature for this before I broadcast TX1 
    inputs
        -spends TX1 output 2of2


If TX1 has a pre-segwit input (therfore is malleable), a malicious person could get TX1 an change the signature. This would result in TX1's TXID changing without affecting the validity of the transaction. The malicious actor cannot spend the funds by doing this, but changing the signature changes the TXID, that TX can still be mined but anything that depends on the original TXID of TX1 would become invalid.


###### Quiz 10 - TX MALLEABILITY:


Question 1:
Run the following command in bitcoin-cli, or parse the raw transaction and calculate the hashes by hand:

010000000001014bd289251780cf66c55ec09706eec00e031101bb3b7bd0aa9a815136389923e5010000000000000000020065cd1d0000000017a914b4c405153d385a21e5691c8f83fcdae8b97241f587acea645900000000160014db7ac922e011e579ff3f84623b7d9d6944b5c8d3024830450221008b09269cd88bcdc5681a4dddbbbad506ee85f4445418046f6d175f2f380259850220497427ad95e78448434c7d6bcb6d8c1828613c256309ee6ad2da7b0dc3d7e53e0121027a919db019d6ad889c682e446f6b91b7c02fba7f0c9164e331374545adce1ee000000000

What is the txid of this transaction?

14e43dd73b63206d286d2707dc62f3cd988a085b22a7adf4a946bd6931b4ff5e

--> Yes! The txid EXCLUDES the witness data. It is the hash of the version, inputs, outputs, and locktime only.

## Converting our P2SH to a Segwit Tx - Pay to WITNESS script hash

Segwit introduced new standard scripts!
    - The one we know about is P2SH: pay 2 scripthash
        script: OP_HASH160 <hash160> OP_EQUAL
    - Segwit introduced: Native segwit script.
        -P2WSH: pay 2 witness scripthash

P2WSH: 
    1. There are no opcodes
        script: <version number> <sha256>
    2. Just 2 data pushes 
        - version number zero (taporoot is version 1)
        - hash, P2WSH sha256, 32-bytes long
    3.  
### Converting our last P2SH script to P2WSH:

OG script: 15686176652066756e2073746179696e6720706f6f7287
scriptSig: 15686176652066756e2073746179696e6720706f6f72

P2WSH script --> 00 20 ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934

P2SH: OP_CODE hash160(OG script) OP_CODE
P2WSH: <0> sha256(original script)

P2WSH: 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934

Decoded: 
{
  "asm": "0 ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934",
  "desc": "addr(bc1q4dykzwjw6qunxjxvademzdegrepxtvw0veylqr08zejkewgupy6qgqu7y2)#3ly5lq0f",
  "address": "bc1q4dykzwjw6qunxjxvademzdegrepxtvw0veylqr08zejkewgupy6qgqu7y2",
  "type": "witness_v0_scripthash",
  "p2sh": "37tvo5XK52qfYWUG4yzUDNgUx9dacjr3YQ"
}

### Adding the P2WSH into a Legacy TX

Example (doesn't actually work in mainnet)

Using a P2WSH script, we'll look money to it using a past transaction.

P2WSH: 0020ab49613a4ed0393348cceb73b137281e4265b1cf6649f00de716656cb91c0934
TXID: 0f198ec61d2e1e8b86e5dd9c56d97d26a00c31d5d8c51b6d919b028fdd9f77ee

TX1: lock funds to our P2WSH script, using a Legacy transaction 
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

TX2: spends the P2WSH! (segwit tx)
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

broadcast the above to get TXID spending a segwit transaction!

See witness data for notes

## Segwit Marker & Flag:

Why does version number stay as 1
    - if you change forms you'd normally use another version #, segwit did not do this.
    
Answer: We want segwit to be backwards compatible
    - if bitcoin core gets a tx w/ a version # it doesn't understand, it'll still try to parse it

Segwit marker and flag were added so the parsers could differentiate between segwit and Legacy.

The segwit market+flag = 0001, this combination will never appear in a Legacy transaction.
 - as it would be treated as 00 --> inputs and 01 --> ouputs (impossible) and is therefore a safe byte sequence.

#### Updated skeleton of a parsed Bitcoin transaction, this time including Segwit:

# Basic Structure of any Segwit Bitcoin Transaction

# {
# Version: (4 bytes, little endian),
# Segwit marker+flag: 0001
# Input Count: (Compact Size),
# Input(s): [
#     {
#     TXID: (32 bytes, little endian)
#     VOUT: (4 bytes, little endian) (normally XX000000)
#     ScriptSig Size: (Compact Size)
#     ScriptSig: 00
#     Sequence: (4 bytes) (normally ffffffff)
#     },
#     {
#     TXID: (32 bytes, little endian)
#     VOUT: (4 bytes, little endian) (normally XX000000)
#     ScriptSig Size: (Compact Size)
#     ScriptSig: 00
#     Sequence: (4 bytes) (normally ffffffff)
#     }
# ],
# Output Count: (Compact Size)
# Output(s):
#     Amount: (8 bytes, sats value, little endian) (normally ends with 00s)
#     ScriptPubKey Size: (Compact Size)
#     ScriptPubKey: (locking script, big endian)
# Witness: (The number of witness stacks are implied by the number of inputs)
#     [
#     Input1's Witness Stack Element Count: 02
#         [
#         len <element1>,
#         len <element2>,
#         ],
#     Input2's Witness Stack Element Count: 01
#         [
#         len <element1>,
#         ],
#     ],
# Locktime: (4 Bytes, little endian) (always the last 4 bytes)
# }
 
 
 
# python dict format you should use
 
parsed_transaction = {
    "version": 0,
    "segwit marker+flag": '',
    "input_count": 1,
    "inputs": [
        {
            "txid": '',
            "vout": 0,
            "scriptSig": '',
            "sequence": 0,
        },
    ],
    "output_count": 1,
    "outputs": [
        {
            "amount": 0,
            "scriptPubKey": ''
        },
    ],
    "witness": [
        [], # input1's witness stack
        [], # input2's witness stack
    ],
    "locktime": 0
}

## REGTEST EXERCISE: Pay to Witness Script Hash




