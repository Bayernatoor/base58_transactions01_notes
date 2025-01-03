# Formating and Parsing Bitcoin Transactions: 

## Recap: 

how many fees in block 855929

coinbase = 3.20539651
subsidy =  3.12500000
fees =     0.08039651

## This section:

1. Sizes of ields
    - 
2. compactSize
3. hashes
    - why are they useful
4. where txids come from
5. calculating fees    


## personal recap on bits and bytes

0000 0000  -> 8 bits = 1 byte

hex: a single byte (8bits) can be represented with 2 chars. (0 - ff)
decimal: can take up to 3 chars (0-255)

ex: 

Amount field of bitcoin output tx:
000000010ab86a1f --> 8 bytes


8 bytes in binary would be: 
00000000 -> 00 
00000000 -> 00 
00000000 -> 00 
00000000 -> 01
00000000 -> 0a
00000000 -> b8 
00000000 -> 6a 
00000000 -> 1f

so 8 binary bits or 1 binary byte is equal to 2 hex chars

00000000 == 1f


##  New transaction dict format: 






# Basic Structure of any Legacy Bitcoin Transaction
# {
# Version: (4 bytes, little endian),
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
#     ScriptSig: (unlocking script, big endian)
#     Sequence: (4 bytes) (normally ffffffff)
#     }
# ],
# Output Count: (Compact Size)
# Output(s): [
#     Amount: (8 bytes, sats value, little endian) (normally ends with 00s)
#     ScriptPubKey Size: (Compact Size)
#     ScriptPubKey: (locking script, big endian)
# ],
# Locktime: (4 Bytes, little endian) (always the last 4 bytes)
# }
 
 
 
# python dict format you should use
 
parsed_transaction = {
    "version": 0,
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
    "locktime": 0
}


# Section 4

## Parsing transactions by hand

Infront of any variable sized field, you put the length of the field
 - the number must be in hex, so if the variable sized field is 50 (25x2) long then the correct hex value is 19. 

locktime:
 - first block the transaction can be mined at.



## compact size:

What is compactSize

1. compact way of saying a size
2. To use the least number of bytes BUT allowing for expansion when necessary

Computes are dumb they roll up to the next number then roll over to 0
(in 2 bytes you can get to 65535 before it rolls over to 0)

one byte --> biggest number we can fit in one-byte
    - hex: ff or decimal: 255

two byte option: -> biggest number we can fit in two-byte
    - hex: ffff or decimal 65535

four byte option --> biggest number we can fit in 4bytes?
    - hex: ffffffff or decimal 4,294,967,295
    - default interger option

eigth byte option --> biggest we can fit in 8 bytes?
    - hex: ffffffffffffffff or decimal 18,446,744,073,709,551,615
    - long integer

In bitcoin you pay per byte you want to save, so we want minimize how much data we send.

Example: long scriptSig with the number 80K in bytes - how many bytes does it take?
    A: 4 byte option

80000 decimal in hex is: 13880 --> 1 38 80 --> 01 38 80 (however 3 bytes is not allowed it must be 4 bytes) --> 00 01 38 80 (big endian)

How does this related to compactSize? 
    - in most cases things are going to be less then 255 or 1 byte so optimize for the small case.

1 byte, up to 252
00 - fc (252) with just 1 byte
fd (253) -> 2 byte size, so read the next two bytes as the size 
fe (254) -> 4 byte size, so read next four bytes as the size
ff (255) -> 8 byte size, so read next eight bytes as the size

so for the 80k decimal example, since it takes 4 bytes to represent it, we'd displaylike so: 

scriptSig: fe 00013880 (size) --> the 80k number

Final explainer:

A compactSize is a field that might be 1,2,4, or 8 bytes long.

The number of bytes in a compact size field can be:

1, 3, 5, 9 (where the first byte is either the length, if 1 byte, or tells you how many more bytes to read to get the length)

https://learnmeabitcoin.com/technical/general/compact-size/


# Coding exercise 4:

## Parsing Bitcoin Transactions with > 1 Byte Compact Field Sizes

version: 01000000
input: 01
    txid: bbb397fdf39cf8b14a49148861c751543172a6f6500e679e079a7aecfbf7aac4 -- convert to little endian: c4aaf7fbec7a9a079e670e50f6a672315451c7618814494ab1f89cf3fd97b3bb
    vout: 00000000
    scriptSig Size: fdb505
    scriptSig: 
00483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d8b42f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a744
83045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401483045022100e222a0a6816475d85ad28fbeb66e97c931081076dc9655da3afc6c1d81b43f9802204681f9ea9d52a31c9c47cf78b71410ecae6188d7c31495f5f1adfe0df5864a7401
    sequence: ffffffff

output: 01
    amount: 80841e0000000000 - convert to little endian --> 00000000001e8480 - convert to decimal --> 2000000
    scriptPub Key length: 19    
    scriptPubKey: 76a9144663e5aab48b092c7478620d867ef2976bce149a88ac
    locktime: 00000000

# {
# Version: (4 bytes, little endian),
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
#     ScriptSig: (unlocking script, big endian)
#     Sequence: (4 bytes) (normally ffffffff)
#     }
# ],
# Output Count: (Compact Size)
# Output(s): [
#     Amount: (8 bytes, sats value, little endian) (normally ends with 00s)
#     ScriptPubKey Size: (Compact Size)
#     ScriptPubKey: (locking script, big endian)
# ],
# Locktime: (4 Bytes, little endian) (always the last 4 bytes)
# }


## Hashing vs Cryptographic hashes


cryptopgrahic hashes are special as they have some randomness properties
    - given any input, the result is equally likely

ex: lisahash4 --> 1111 (binary) --> 16 possible result
    -> 0000, 0001, 0010 .... 1111
                   
regular hash: different but similar input data will result in a different but similar hash
cryptohrapic hash: different but similar input data will result in a wildly different hash

hash functions are not cryptographic
    - do not have the equality of distribution

every hash function property same input == same output

sha256:

256: number of bits in the result

256 bits --> 32-bytes

every txid will always be 32-bytes

the txid is a fixed 32-byte field, because the sha256 hash function will always return 32-bytes of data.

empty tx --> 32-bytes
monster tx --> 32-bytes

magic of using a hash function is that regardless of the length of input data you get a fixed length output. 

with hash functions you have an equal chance of getting any of the numbers between:
0 and 2^256(num of bits in the hash output)

sha256 possibilities:
115792089237316195423570985008687907853269984665640564039457584007913129639936

see learnmeabitcoin for more info.


## How to make a TXID:

1. take all the bitcoin tx raw data
2. convert it from hex to bytes
3. run data through sha256 function twice
4. profit

The sha256 function will return the txid in little-endian to search for it you have to reverse it (big-endian)

## important criterias of a Strong or Crytographic hash function:

Preimage resistance: It is computationally infeasible to determine an input given a hashed output.

2nd preimage resistance: it is computationally infeasible to find any second input which has the same output as any specified input. 

Collision resistance: it is computationally infeasible to find any two distinct inputs which has to the same output.:w




