# Section 6 - Standard Bitcoin Scripts: Pay to Script Hash

## Pay to script hash recap:

Script ( the language)
script ( a specific script written in Script ;))

1. We found ou that there's 2 fields in a tx that contain script "parts"
    a. ScriptSig and scriptPubKey
2. match scriptSigs and scriptPubKey are actually in TWO different txs.
3. we wrote our own script and split it in 2 parts
    a. scriptSig (Unlocking part)
    b. scriptPubKey (locking part)
4. We made 2 txs. one to lock up some bitcoin to the locking part and one to unlock it.
5. When locking the bitcoin, we ran into an error with the scriptPubKey. When attempting to send the raw tx, an error was returned: ```unstandardscript```.
    a. We need to use a "standard script" to broadcast the tx.
6. We took our original script and packaged it differently. We hashed it and put the hasd in a "P2SH formula" --> OP_HASH160 <script> OP_EQUAL
7. We put the P2SH script into our scriptPubKey field of TX1
8. And we then had to make a few changes in TX2's scriptSig field to spend it. 

P2SH Recap:

1. Has 2 opcodes and 1 piece of data.
2. piece of data is always a hash160 of the original script

Human readable form of P2SH: 
        
OP_HASH160 <hash160 of OG script> OP_EQUAL

Changing it to Hex:

a914fb528f99064469fd19f1fc7f105a9fd324c7160787

## Interpreting a P2SH Script:

----- 
Original transactions from Section 5: 

OP_HASH160 a914fb528f99064469fd19f1fc7f105a9fd324c7160787 OP_EQUAL

asm: OP_HASH160 a914fb528f99064469fd19f1fc7f105a9fd324c7160787 OP_EQUAL
hex: a914fb528f99064469fd19f1fc7f105a9fd324c7160787

TX1:
txid: dac3397e17744817b33365b7c3377e797266173cddf761fef6a935f9d96f3
version: 01000000
vin:
    txid: c0511a3bcc42d6d7cdc3a39569b0f782bd5d74220d566eb386e0d9cb198ce83
    vout: 00000000
    scriptSig: 00
    sequence: ffffffff

outputs: 01
    amount: 18ddf500000000
    -> scriptPubKey: 17 a914fb528f99064469fd19f1fc7f105a9fd324c7160787
locktime: 00000000

TX2:
version: 01000000
01
    txid: f3963df3956aef1f67f7dd3c176672797e37c376b556337b814477e19730c3da
    vout: 00000000
    scriptSig: 2e
        156b6176626620566e207346179696e662072706f6f72
        17156861762b6620566e207346179696e662072706f6f7287
    sequence: ffffffff

    amount: 30d9f500000000
    -> scriptPubKey: 17 a914fb528f99064469fd19f1fc7f105a9fd324c7160787

txid: 0f198ec61d2e1e8b86e5dd9c56d97d26a00c31d5d8c51b6d919b028fdd9f77ee

----


We need: scriptSig TX2 | scriptPubKey TX1 

-> scriptPubKey: a914fb528f99064469fd19f1fc7f105a9fd324c7160787
-> scriptSig: 
        15686176652066756e2073746179696e6720706f6f72
        -> 17156861762b6620566e207346179696e662072706f6f7287
        redeemScript: last item in the scriptSig


script:
            

questions when an OP code operates:

1. How many items in the stack does this touch?
2. does it take data off the stack? 
3. does it put data on the stack? 

a9 = OP_HASH160

1. Read off first stack item
2. hash160 it
3. pop off first item from stack
4. push back the hash160 to the stack

OP_EQUAL:

the are!

stack:

1: 1
0: 686176652066756e2073746179696e6720706f6f72


Verification:

Is it empty: No
Is the last item on the stack a 1: No

So we'd think this failed...

Some MAGIC happens now... lol.. but only because this is a P2SH script
This happens on line 1997 of interpreter.cpp

IF p2sh:

1. Stack cannot be empty
2. Pops stack once so we remove the 1
3. puts the scriptSig back on the stack using the redeemscript --> ```156b6176626620566e207346179696e662072706f6f72```
4. Starts evaluation again

"new" script:


new stack: 

87

1: 686176652066756e2073746179696e6720706f6f72
0: 686176652066756e2073746179696e6720706f6f72

OP_EQUAL

0: 1

scripts passes!! Woot

## Takeaways and Tradeoffs with P2SH


w/o P2SH nonstandard:
    original (locking) script: 15686176652066756e2073746179696e6720706f6f7287 (have fun staying poor) "in hex" --> Bob pays
    scriptSig (unlocking): 156861762b6620566e207346179696e662072706f6f72 -> I pay for this


w/ P2SH scripthash:
    locking script: a914fb528f99064469fd19f1fc7f105a9fd324c7160787, Bob pays for this.
    unlocking script: 156861761b6620566e207346179696e662072706f6f7215686176652066756e2073746179696e6720706f6f7287, I pay for this. 

*Remember lock script in script hash is a hash160 of the original nonstandard script*

TakeAways:
    1. we had to use P2SH. No other way to use our custom script w/o it.
    2. how many bytes ended up in a tx for the nonstandard script? 
        45 bytes
    3. how many bytes ended up in the txs for the p2sh script?
        69 bytes
    4. which is more expensive in bytes? 
        P2SH

diffence 69-45 = 24 bytes. The extra byte came from having to add the length byte for the redeemscript in the p2sh unlocking script

    5. Who's paying for these txs
        TX1 -> locked to the p2sh script, Bob pays for this one, He pays 23 bytes
        TX2 -> spent the p2sh script, I pay to spend this

Bob's gonna pay me money with a914fb528f99064469fd19f1fc7f105a9fd324c7160787

The person responsible paying for the potentially more expensive/complicated P2SH unlocking script is the one benefitting from the script (whoever can then spend it)


##### QUIZ 9:


Q: Where does our custom script end up if we lock to it using a Pay 2 ScriptHash?


A: We lock to the hash of the script, the script itself goes in the scriptSig of the unlocking transaction.

We lock to the hash of the script, the script itself goes in the scriptSig of the unlocking transaction.

## Coding exercise: Convert Custom Scripts to P2SH Addresses


Using regtest you can convert a custom script to a P2SH address by running:
    `bitcoin-cli -regtest decodescript my_custom_script`

The output will include a p2sh address which is the base58 address encoding of the P2SH
scriptPubKey

You can convet a base58 encoded address back to a scriptPubKey by runnng:
    `bitcoin-cli -regtest decodescript my_address`

This returns the p2sh address's scriptPubKey. This scriptPubKey is what you find in the raw transaction. The base58 address is a just a human readable version of the scriptPubKey


*What's happening here?*

When I decode the script. I am given a base58 encoded address. I can send (lock) bitcoin to this address. To unlock it I would need to present the (key) or the scriptSig that corresponds with the scriptPubKey. 

custom script: `010101029301038801027693010487`

 run:`bitcoin-cli -regtest decodescript my_custom_script`
 Get a base58 adress: `2MurSWkcDqSq69nuWSBXwNraCFbHvSouGQn`
 Send bitcoin to that address
 That bitcoin is now locked to that address via the custom_script, to unlock it (spend it) I have to provide the correct scriptSig (The script that satisfies my scriptPubKey (custom script))

## Legacy Bitcoin Addresses and Base58 Encodings

1. where do bitcoin addresses come from?
2. Complicated scripts and fun scripts!
3. Wallet support for P2SH (abysmal!)

A bitcoin address is essentially scriptPubKey data. It's script data but wrapped in base58 encoding


Let's make a bitcoin address using a P2SH script 
    scriptPubKey: a914fb528f99064469fd19f1fc7f105a9fd324c7160787

3 parts to a pre-segwit bitcoin address:
    1. flag
        05 -> P2SH mainnet
        c4 -> P2SH testnet/regtest
    2. hash160 (data) that goes in the standard script (payload)
        fb528f99064469fd19f1fc7f105a9fd324c71607
    3. checksum

c4 fb528f99064469fd19f1fc7f105a9fd324c71607 checksum


Flag (version bytes): What kind of data is in this base58 encoded string
      P2SH txs: whether it's a mainnet or testnet address

data: is always the hash160 of the original script

checksum:
    The point is to be able to verify that we've gotten the correct information
    - find a hash of the important info(payload) --> sha256(sha256(flag + data)) take the first 4 bytes
    - to verify it, since you are sending them the checksum in the address, they can remove the checksum, hash the data and confirm if the checksums match.

    hashing the checksum (flag + payload) :  c4fb528f99064469fd19f1fc7f105a9fd324c71607 
    takes first 4 bytes: 35f43cbd

new data:

flag  data/payload                            checksum
c4   fb528f99064469fd19f1fc7f105a9fd324c71607 35f43cbd

Now encode it as base58
c4fb528f99064469fd19f1fc7f105a9fd324c7160735f43cbd
--> 2NGA6VsFnfyQ5mQjem32pDuYPFnZGAGPkqJ

We can verify by running
    `bitcoin-cli getaddressinfo 2NGA6VsFnfyQ5mQjem32pDuYPFnZGAGPkqJ`

which will spit out a json object with a scriptPubKey, if that matches our scriptPubKey from above then we're good to go:
    Result:  a914fb528f99064469fd19f1fc7f105a9fd324c7160787
    Original a914fb528f99064469fd19f1fc7f105a9fd324c7160787

Success!

Above was testnet/regtest:
--> c4fb528f99064469fd19f1fc7f105a9fd324c7160735f43cbd
--> 2NGA6VsFnfyQ5mQjem32pDuYPFnZGAGPkqJ

Now lets do it for mainnet:
--> 05 fb528f99064469fd19f1fc7f105a9fd324c7160735f43cbd checksum
    get checksum (double sha256 the flag+data):
    ---> 05fb528f99064469fd19f1fc7f105a9fd324c71607 bb83e0ab
    Now encode to base58 to get the address:
    ---> 05fb528f99064469fd19f1fc7f105a9fd324c71607bb83e0ab
    return: 3QbtS8Km4WtjZd775uQwbxZ83SM6RwzFEz
    (all P2SH mainnet address starts with a 3)


Side Question: When would I ever generate a P2SH address when using a normal bitcoin wallet(pre-segwit)

  - typically there are 2 reasons:
    1. Multisig (the most common)
    2. weird funky segwit thing that is P2SH - next section
    3. not typically reason, you wrote your own script!

When you have a P2SH script you have to save the original script (redeemScript)
    If you lose it you can't spend the bitcoin, this is because you locked the bitcoin to a hash of the redeemScript. In order to spend it you have to provide the original script yourself

descriptor wallets are much better allowing funky/custom scripts
For a long time there was no standard way for wallets to tell each other about the redeemScript
PSBTs --> you can put redeemScript in them.

## ScriptHash Security and P2SHs in the Wild:

1. Why are P2SH absolutely terrible
2. Look at P2SHs in the wild
3. non-standard scripts that in exist in bitcoin (before standard (P2SH) became mandatory)


3MGERhsHFk7nL9TgmqwQPa6be2QJzMAnUt
    flag: 05
    hash160: ?
    checksum: ?

to find the hash160 you have to re-encode address as hex, not bas58
base58.b58decode(address).hex()
--> 05(flag) d6b28dadb9966952e2c05b497176e01c1acb3c8b 0950d5ad(checksum)

Let's verify the checksum:

Take the flag + data: 05d6b28dadb9966952e2c05b497176e01c1acb3c8b 

convert to bytes and Run double sha256 on it. Do the first 8 bytes, match the above checksum?

my result: -->     0950d5ad
original checksum: 0950d5ad

Correct!

remove flag and checksum and you get hash160:

hash160: d6b28dadb9966952e2c05b497176e01c1acb3c8b 

to recreate the p2sh:
    P2SH: OP_HASH160 <hash160> OP_EQUAL
          a9 14(length of hash) d6b28dadb9966952e2c05b497176e01c1acb3c8b 87
    scriptPubKey: a914d6b28dadb9966952e2c05b497176e01c1acb3c8b87


Take scriptPubKey and run it through -> `bitcoin-cli decodescript` to verify if address matches

{
  "asm": "OP_HASH160 d6b28dadb9966952e2c05b497176e01c1acb3c8b OP_EQUAL",
  "desc": "addr(3MGERhsHFk7nL9TgmqwQPa6be2QJzMAnUt)#ulfdl3rz",
  "address": "3MGERhsHFk7nL9TgmqwQPa6be2QJzMAnUt",
  "type": "scripthash"
}


Matches!

Since we have the scriptPubKey we could lock bitcoin to it. But since we do not have the redeemScript we can't spend it. 


