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

txid: 0f198c6d12e1e8bde9dc56d97d26a00c31d5d8c51bdd91802f8dfd9f7fee

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

