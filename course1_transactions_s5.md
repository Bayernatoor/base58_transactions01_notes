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


op_code Data                                                               op_code
a8      2012998c017066eb0d2a70b94e6ed3192985855ce390f321bbdb832022888bd251 87

2 ways to view Script (language) script.

1. in a transaction as hex-encoded bytes
2. as a human-readable version of Script, field starts with asm
    1. you can get it by passing the script through "decodescript" 


 
## Stack Evaluation of Bitcoin Script

Generally script is called a stack based language

Got date? Push it on a stack. Like a stack of plates. 1 plate ontop of the next.
You can't get to the bottom one before you take the ones from the top first.

Stack comes in as a long string of data and the stack executor will look at it one byte at a time (similar to how I did it in the previous exercise) 

#### Example:

DATA: raw_script2 = "176567616d6965727020676e697473657265746e69206e41a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287"

asm_script2 = "6567616d6965727020676e697473657265746e69206e41 OP_SHA256 a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5 OP_EQUALVERIFY OP_DUP OP_ADD 2 OP_EQUAL"

Stack:

7: OP_EQUAL
6: 2
5: OP_ADD
4: OP_DUP
3: OP_EQUALVERIFY
2: a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5
1: OP_SHA256
0: 6567616d6965727020676e697473657265746e69206e41


Success criteria: 
    1. Either the stack is empty 
    2. Or there's a true (one thing left on stack, only thing left on stack)
  
#### Example From Video:

script 3 XXXXXX 3 XXXXXX

1: XXXXXX
0: XXXXXX


The above stack does not pass criteria (items still on stack)

To make it pass we can add OP_CODES or operation codes, such as OP_EQUAL

Every opcode touches a different number of items on the stack. Let's look at OP_EQUAL.


OP_EQUAL -> 
    1. Takes 2 items off the stack
    2. compares them
    3. if equal, push back onto stack as 1
        if not equal, push back onto stack as 0 

Taking above example if it ended with OP_EQUAL, we could make this script pass. 

We need the Hex code for OP_EQUAL (find it in script.h in bitcoin_core repo)

Hex code = 0x87

New Script : 3 XXXXXX 3 XXXXXX 87 

2: XXXXXX
1: XXXXXX
0: OP_EQUAL

is XXXXXX == XXXXXX --> yes

Stack is now:

0: 1

This evaluates to true and so the script is valid.


##### Quiz 2:

Question 1: Perform a Stack Evaluation of the following Bitcoin Script, stepping through how it would be evaluated by a bitcoin node:

hex: "010101029301038801027693010487"
asm: "1 2 OP_ADD 3 OP_EQUALVERIFY 2 OP_DUP OP_ADD 4 OP_EQUAL"

Answer: 

Stack:

1: 2
0: 1

OP_ADD

New Stack: 

0: 3 (new value)

OP_EQUALVERIFY

New Stack: 

0: 1 (True) 

New Stack :

0: 2

OP_DUP

1: 2
0: 2

OP_ADD

1: 4 (add last byte of data)
0: 4 (From the OP_ADD above)
 
OP_EQUAL

0: 1 (TRUE)

pops off the 1 stack is empty

[]

This script passes the criterias and is valid 


Question 2: 
Perform a Stack Evaluation of the following Bitcoin Script:

hex: "176567616d6965727020676e697473657265746e69206e41a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287"

asm: "6567616d6965727020676e697473657265746e69206e41 OP_SHA256 a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5 OP_EQUALVERIFY OP_DUP OP_ADD 2 OP_EQUAL


Stack: 

0: 6567616d6965727020676e697473657265746e69206e41 

OP_SHA256

1: a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5
0: a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5

OP_EQUALVERIFY

0: 1 --> inputs are equal

Pops off the 1

New Stack: 

[]

OP_DUP

Nothing to DUP, script fails. 

## What's the point of Script?

1. How does it fit into a transaction?
2. how does it keep Bitcoin safe


Lets look at that script again:

3XXXXXX --> is our scriptSig (someone needs to know this)
3XXXXXX87 --> is the lock we put onto the scriptPubKey (anything in here immediately becomes public)


##### Quiz 3
What does it mean to OWN Bitcoin?


A: UTXOs have locking scripts in them. To own Bitcoin is to know the secret which would let me unlock that Bitcoin and use it as an input to another transaction. I own my Bitcoin because I know the secret, which I would put in the ScriptSig spending the UTXO, and no one else does.


------------------

## Locking to a Custom Script

**Reminder: When adding the SCRIPT portions to a transaction, the script fields require their own byte to determine how long the script data is**.

176567616d6965727020676e697473657265746e69206e41a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287

Locking script: 176567616d6965727020676e697473657265746e69206e41 (scriptSig) 

Unlocking script:  a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287(scriptPubKey)

Let's make a Tx with these:

I need 2 tx:
    1. lock to that scriptPubKey
        -> scriptPubKey: a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287
    2. spend it in a second tx that spends the locked bitcoin.
        -> scriptSig: 176567616d6965727020676e697473657265746e69206e41

Tx:

Version: 0100000000
input
    ???
output: 01
    amount: ???
    scriptPubKey: 28 a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287
locktime: 00000000
p
a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287
When attempting to broadcast the above she runs into an error. The scriptPubKey comes back as nonstandard. 

## Standard scripts  (pay to script hash)

Bitcoin won't let you lock bitocin to any script (used to)

They introduced something calle standard scripts:
 - Only certain "Standard" scripts are allowed to show up in a bitcoin TX.

If you want to lock it to any old script you can by using a very special standard script. We'll have to convert our script to this type of script

It's called P2SH --> Pay to script hash.

How do you do this?

1. Take the original script
2. Hash it
3. Put that hash in a special pre-determined script format P2SH
4. then lock the bitcoin to the P2SH "formula that has the hash of our original script

What is the P2SH script "formula"
    1. OP_HASH160 <hash160 of OG script> then OP_EQUAL

txid: sha256(sha2569(tx_data))

hash160 is two has functions
  1. ripemd160(sha256(original script))
 
Once you have the hash160 of the original script you all it the P2SH script "formula"

1. OP_HASH160 <OG script hash> OP_EQUAL
2. a9 14 e0c055e46e44709c4134a1a7e57bb8b896c5f4d8 87 


complete script: a914e0c055e46e44709c4134a1a7e57bb8b896c5f4d887 

to confirm run bitcoin-cli decodescript: 

{
  "asm": "OP_HASH160 e0c055e46e44709c4134a1a7e57bb8b896c5f4d8 OP_EQUAL",
  "desc": "addr(3NBPhDhXADiwbtxYXXSExFzVLbfFnJEWqT)#z7tm6smx",
  "address": "3NBPhDhXADiwbtxYXXSExFzVLbfFnJEWqT",
  "type": "scripthash"
}

type is scripthash, so we're good to go. We'll replace the scriptPubKey in our original TX with thi
script.


## Unlocking from the pay to script hash

After broadcasting the original Tx you'd end up with a TXid

To unlock the amount in the TX from that TXid that we previously locked up we'll need to create a new TX.

version: 0100 000 
01
txid: ....
output: 00000000
scriptSig: 42 18176567616d6965727020676e697473657265746e69206e4128a820a966e2ccbbcd3814c8f913abcb1c4d487d63f23d93667c186b00a5a9181fd7b5887693010287
sequence: feffffff
output: 01
amount: 30d9f50500000000 
complete script: 17 a914e0c055e46e44709c4134a1a7e57bb8b896c5f4d887 
locktime 00000000

combine all the above data into one line and use bitcoin-cli sendrawtransaction to spent it. 











