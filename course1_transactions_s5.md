# Module 5 - Intro to Script: Locking and Unlocking Bitcoin

script -> varialble length fields
## Recap:

Every field has a length (fixed or variable)
Variable length fields have a compact sie at the front
    - This tells you how long or how many chars there are following it.

Most of the fields are numbers. We write numbers using little endian

## Fields in a TX:

Version Number(nversion)
list of ins
    -everr input has 4 fields
        - txid..
        - vout (output index)
        - scriptSig (Proof to spend it) (unlocking script)
        - sequence --> fffffff
list of outs
    -every output has 2 fields
        - amount
        - scriptPubKey --> need to prove it to spend the output (it's a lock)
locktikme (nlocktime)


--------------------

## Script:

scriptSig and ScriptPubKey go together. 2 parts of the same whole (yin/yang)

scriptPubKey is the locking script 
scriptSig is the unlocking script 

To check if the scriptSig unlocks the scriptPubkey for that output :

1) You need to look up the ScriptPubKey for the output you are trying to spend.  
2) These are scripts
3) Put them together, first the scriptSig and then the scriptPubKey
4) Then run the scripts as 1 program (together) 
5) did script execute finish and meet the success  criteria
    yes --> Person has successfully unlocked the output, spend is valid
    no --> Spend is invalid and the tx with the scriptSig is discarded 


#### Example

Tx1:
    output: 5 bitcoin
    scriptPubKey: XXXXXX locking key

Spend TX1 by creating a new TX

TX2:
    txid: TX1
    vout: 0
    scriptSig: YYYYY unlocking key

Verification:

Must verify that the scriptSig passes the lock in scriptPubKey.

    "run YYYYY XXXXXX through script interpreter"
        Yes ? Ok ... NO? Trash

If valid then TX2 is eligible to be included in a block


##### QUIZ:

Q1: Why is the scriptPubKey, the locking script that specifies under what conditions we can unlock our bitcoin, called the scriptPubKey?

A: Correct! The original locking mechanisms for Bitcoin were Pay to Public Key (and Pay to IP), so while we don't commonly do Pay to Public Key much anymore we still call the locking script the scriptPubKey.

Q2: Why is the ScriptSig, the unlocking Script, called the ScriptSig?

A: Yes! A cryptographic signature proves you know a private key for an associated public key. For the original Pay to Pubkey payments, you'd lock to a public key and unlock by signing the transaction, the signature would go in the Input's script section, so we call it the scriptSig. It doesn't HAVE to be a signature, and in this course we're not going to use signatures at all, but that's why we call it the scriptSig.


# What is Script?

A way to take data and saving it somewhere in order, as well as being able to run code on that data. the code is called Operations. 

Operations codes are called OP codes

### Data:

Very similar to variable length fields in a bitcoin TX but not quite the same

First byte (normally) has a prefix, which represents the length of the data (kinda like compactSize), prefix is followed by the actual data

I have some base58 data that I want to include in a script
I'll use python to turn it into hex string

#### Example:

Data="736f6d6568657864617461"

to put this in data in the script i need the length

len = len(Data)
--> 22 

len // 2 = 11

b'11'.hex()
--> b

length,  data
0b        736f6d6568657864617461  


valid script with data in it with 11 bytes of data in it.

you can run the data with length in bitcoin-cli.

    run bitcoin-cli 0b736f6d6568657864617461  

result:

{
  "asm": "736f6d6568657864617461",
  "desc": "raw(0b736f6d6568657864617461)#rea0hjv5",
  "type": "nonstandard",
  "p2sh": "32tRvw39zH9GDw7uyjq5jFxR38K199f5Vo",
  "segwit": {
    "asm": "0 6e8a723bc635136a69c2dc8ef31cb97d754d31746be8c32808543d68664ac9c4",
    "desc": "wsh(raw(0b736f6d6568657864617461))#ue5ngmss",
    "hex": "00206e8a723bc635136a69c2dc8ef31cb97d754d31746be8c32808543d68664ac9c4",
    "address": "bc1qd698yw7xx5fk56wzmj80x89e04656vt5d05vx2qg2s7ksej2e8zqjw6w5l",
    "type": "witness_v0_scripthash",
    "p2sh-segwit": "3HiXZXvfJymYQXcd2WvUr36yetF8F97kEf"
  }
}

## Operation Codes (OP codes):

Single bytes which serve as special flags that are used to lookup what actual "operation" was done.

0b 736f6d6568657864617461  

Here's a quick example of a script with some data and opcodes. Yes, it is just a string of hex data.

"a82012998c017066eb0d2a70b94e6ed3192985855ce390f321bbdb832022888bd25187"

I can break this apart into opcodes and data because I'm a wizard. Here it is divided out as data + opcodes. There are two opcodes, one at the start and one at the end. The big chunk of hex in the middle is data.

a8 2012998c017066eb0d2a70b94e6ed3192985855ce390f321bbdb832022888bd251 87

2 ways to view Script (language) script.

1. in a transaction as hex-encoded bytes
2. as a human-readable version of Script, field starts with asm
    1. you can get it by passing the script through "decodescript" 


 

