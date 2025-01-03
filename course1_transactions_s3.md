# Bitcoin Transactions:

2 legacy inputs to 1 legacy ouput
TXID: ecc1bb5860f85eaaae855ecbf5da9ac8b85f4fe6f27ad2a64b29d005551688fd 

Raw transaction in Hex:
Each Byte consists of 2 hex chars
nVersion: 01000000 - > always 4 bytes long
inputs count: 02
    input data:
        txid:
        output number:
        scriptSig(unlockscript):
        nsequence:


cb8bc5ab40ab6528a140a41342fbe7dc0592738f4f5c258d4a41bdf4ecb785ed
000000006b

script input 1: 483045022100b53e5c01c3fd2ac0fefaed82b2badcdd0869c60bd4d28b8e0048ad38e722c7de02202431de8e8c9312c8c0f64a4eb3308fc390385bdb422a7dd7049a0e0f36e4d4be012103666474fc54f7c73ec90ab7caa3717a87a510225379ff4989f5e24a396acbeac2

ffffffff53d3e4433eeee585880de4d1ae640e71f793759d064fb58e2e35189a0edc715a000000006a

script input 2: 47304402207101ab1001f0dcc09a95202560c3ac936125b2032c9ef8877344d2517f0c4f5202207adc38c190305e6e3cf17040966aa12434c7b480280de9307721cd5ef6b20107012103666474fc54f7c73ec90ab7caa3717a87a510225379ff4989f5e24a396acbeac2

ffffffff0136d17500000000001976a914640131c56db98ae95537a4063f7312d5780fc63388ac00000000


SEGWIT tx breakdown:

TXID: 68333a10b368e0d002098827fa3f348135fb728ade74d265e6abf41dfcb60a1c

nversion: 02000000
segwit bytes: 0001
number of inputs: 03
#0
    txid: d19441b832d4e24e4e10c08413b57c017785ea7407b373d4566e11ad94d8134c
    index of the output: 1c000000 (28 dec)
    script 171600147c846a806f4d9e516c9fb2fe364f28eac4e3c3fc  
    sequence: ffffffff
#1
    txid: 3d416a5941422eeecbcc0e3fe6aa7a88d00d22b67df149293e3c5bee10c4719a
    index of the output: 2c000000
    script: 171600147c846a806f4d9e516c9fb2fe364f28eac4e3c3fc
    sequence: ffffffff
#2
    txid: 4f22589a292781a3cc2d636b9f1932f367305625a7874f8573b72b98ad736996
    index of the output: 00000000
    script: 171600147c846a806f4d9e516c9fb2fe364f28eac4e3c3fc
    sequence: ffffffff

count of outputs: 02
#0
    amount: f564680400000000
    person that can spend: 17a9142c21151d54bd219dcc4c52e1cb38672dab8e36cc87

#1
    amount: c027654400000000
    person that can spend: 1976a91439b1050dba04b1d1bc556c2dcdcb3874ba3dc11e88ac

segwit data (additional proof that you can spend the inputs - witness data)
1 witness data for each input
02
47304402203ccede7995b26185574a050373cfe607f475f7d8ee6927647c496e3b45bf61a302202bd1ff88c7f4ee0b6f0c98f687dff9033f770b23985f590d178b9085df589101012103789a9d83798d4cbf688f9969a94084ee1655059e137b43492ee94dc4538790ab

02
483045022100b46ab18056655cc56b1778fd61a56f895c2f44c97f055ea0269d991efd181fb402206d651a5fb51081cfdb247a1d489b182f41e52434d7c4575bea30d2ce3d24087d012103789a9d83798d4cbf688f9969a94084ee1655059e137b43492ee94dc4538790ab

02
473044022069bf2ac34569565a62a1e0c12750104f494a906fefd2f2a462199c0d4bc235d902200c37ef333b453966cc5e84b178ec62125cbed83e0c0df4448c0fb331efa49e51012103789a9d83798d4cbf688f9969a94084ee1655059e137b43492ee94dc4538790ab

locktime:00000000

-------------- parsing a raw txid explained:

RAW TX:
0100000001913f3edcafa48bcd5742225a752f3dd8cef35596dfb0fce551c5b455ce0a02d63b0000006a473044022062f4f61766e1edf89b9b94d0629d67bfefb62e6ffec63f17d0f10ce5e329dbf4022039d566558c1f98742345e70b194bbcb8b8fff5b7fa2f0507c9f31a5a2ea24749012103fc3e6b07b7bec800cb0861c172344687d146888aaf0f811eaca8b1ef6684c9fc0000008002f07e0e000000000017a914783b39e49c6b6544a51bf0cbd4f47eef116be81987e0ec0400000000001976a91456c0bc2f50bc150d4ea122e66db7c48b01b9722988ac00000000

two (three) types of fields:
    - fixed length fields, pre-set number of bytes for field
        -> always little endian (seems to come as big endian in the rawtx)
    - variable length, no preset length, instead a length byte and then data for tha field (scriptSig)
        -> always big endian
    - compactSize fields. hybrid fixed/variable length field. always used to tell a size
        -> always little endian (probably)

----
<!--NOTE: Transaction field types-->
nVersion: fixed 4 bytes - little endian (big endian in raw tx)
Count of inputs - vin: CompactSize - little endian
TXID: fixed 32bytes little endian (big endian in raw tx_
scriptSig length: variable
scriptPubKey (locking script): variable
nSequence: Fixed 4-bytes - little endian (big endian in raw tx)
Count of outputs - vout:  CompactSize - little Endian
Amount: Fixed at 8 bytes - little endian (big endian in raw tx)
scriptSig length: variable
scriptPubKey (locking script): variable
Locktime: Fixed at 4 bytes
----
1976a91456c0bc2f50bc150d4ea122e66db7c48b01b9722988ac00000000

nVersion fixed at 4-bytes:  01000000
count of inputs, compactSize field: 01 
    txid, fixed at 32-bytes: 913f3edcafa48bcd5742225a752f3dd8cef35596dfb0fce551c5b455ce0a02d6 (big endian)
                             d6020ace55b455c551e5fcb0df9655f3ced83d2f755a224257cd8ba4afdc3e3f91 (little endian - must convert to this to find in explorer)
    output number, fixed at 8-bytes: 3b000000
                                     0000003b
    scriptSig, variable length: 
        length of scriptsig, compactSize: 6a (106 decimals)
        data of script, variable compactSize: 473044022062f4f61766e1edf89b9b94d0629d67bfefb62e6ffec63f17d0f10ce5e329dbf4022039d566558c1f98742345e70b194bbcb8b8fff5b7fa2f0507c9f31a5a2ea24749012103fc3e6b07b7bec800cb0861c172344687d146888aaf0f811eaca8b1ef6684c9fc
    nSequence fixed, 4-bytes: 00000080
    
count of outputs, compactSize field :02
0
    amount, fixed at 8-bytes:  f07e0e0000000000
    little endian amount, fixed at 8-bytes: 00000000000e7ef0 
0 = 0 
15 = 240
14 =3584
7 = 28672
14 = 917504

amount in btc: 0.00950000

    scriptPubKey. variable length: 
        length of field: 17 (23 decimals) 
        data of field, variable:  a914783b39e49c6b6544a51bf0cbd4f47eef116be81987
1
    big endian amount, 8-bytes: e0ec040000000000
    little endian amount, 8-bytes: 0000000004ece0
0 * 16 0
14 * 16 1 = 224
12 * 16 2 = 3072 
14 * 16 3 = 57344
4 * 16 4 = 262144

amount in btc: 0.00322784

    scriptPubKey: variable:
        length: 19 (25 in decimals) 
        data of script, variable: 76a91456c0bc2f50bc150d4ea122e66db7c48b01b9722988ac
    locktime: 00000000

<!--NOTE: Fixed fields are always little endian -->



Exercise: 

0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000


nversion: 01
count 00000001
    txid: c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704
    output number: 00000000
    scriptsig:
        length: 48
        data: 47304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901
    nSequence: ffffffff

count outputs: 02
    amount: 00ca9a3b00000000
    scriptpubkey: 
        length: 43
        data: 4104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac
    amount: 00286bee00000000
    scriptPubKey:
        length: 43
        data: 410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac
    locktime: 00000000


020000000206d95b56ee225895d7dd974684a1d399c1dedebd0f89fbced938f26a483ea97c020000006b48304502210090b4e141f943f8ac7c44d402bbca7775be6de048482000ab9ece80986b48394a02203360c0d814d8ac083404c247ed17c1e996c7a1e7623f94265ed0b3520417eda601210330af4cb9c937c9b68a67a242f7fcdb042d885409a82aadc30f99a24b6270318ffdffffffefb418b95f827015a1381ff60e94798125537f9db7548b007827c69f2b411831010000006b483045022100b6436e2256465c1de74eab15b840b50d86805ded05dfe1d5d7cfcb4267aac88302202e77a872f8e4e17566bca1e91819608d9e42198e7a8da8177eaa241e84c7f14501210330af4cb9c937c9b68a67a242f7fcdb042d885409a82aadc30f99a24b6270318ffdffffff0208cf0000000000001976a9141a05cd43066c60524ed87549f114047416b2b70e88ac93d00400000000001976a9144a8bb622440366e0b39f5803326dc92a6bd89b4b88ac00000000


------------------

# inputs and outputs


3 questions:
    1. How much bitcoin does this tx lock up?
        - Sum of all amount fields in the outputs 
        - Remember amount fields are 8byte little endian fields in raw tx. So you must covert to big endian before calculating
        A: 1272784 sats
    2. How much bitcoin was spent into this transaction?
        - this depends on the inputs being used. 
        - specifically the txids of those inputs - the txid of the input is a pointer to the previous transaction.
        - little endian txid of input: 'd6020ace55b4c551e5fcb0df9655f3ced83d2f755a224257cd8ba4afdc3e3f91'
        - we looked for the 59th output of the above "previous" txid and the amount was 0.01315269
        A: 1315269sats
    3. How much did this tx pay in fees:
        A:4248sats


What does a transaction do?
    - destroys outputs. marks it as spent -> inputs
    - created 2 new outputs

When making a new tx
    - Which exisiting outputs are you destroying?
    - what new outputs are you creating?

A satoshi: is the denomination of the amount field on an output in a bitcoin transaction.

How does bitcoin core know if an output can be spent?

------

# The UTXO set

When core gets a new block it does the following (very simplified):
    inputs:
    1. Go through the list of inputs to every tx
    2. check if input is in the utxoset to ensure none are double spends
    3. Remove that utxo from the utxoset since it's just been spent
    output:
    1. Go through the list of outputs in every tx
    2. add every new output to the utxoset


    utxoset :
        tx : x:59 (txid and ouput 59 of that transaction)
        0-58, 60-66 outputs
        tx:newtxi
        0,1 
    
with the above one extra ouput would be added to the utxoset

## initial block download:
    
    - new bitcoin core node
    - asking peers for block starting at the genesis block.
    - gets new blocks --> verification process
    - part of the time needed for this is the core checking to make sure no double spends happened
block: list of txs
tx: list of ouputs and inputs
------

# TX Fees and Coinbase TXs:

fees: Do NOT show up in the tx but do show up in the block

block:list of txs
    All of the inputs in a block: INPUT AMT 
    All of the outputs in a block: OUTPUT AMT

every tx (except the coinbase tx) pays a fee
    -  input > output --> difference is the fee paid
    
What is a coinbase tx?
    - Only one person can make the coinbase tx
    _ The person who mines the block
    - This tx has no inputs
    - It does not spend any outputs,no prior UTXO. 
    - it does have outputs
        

Total amount available fo a miner in the COINBASE TX: 
    - all the extra sats which werent included in that blocks transactions --> fees
    - Block subsidy --> new bitcoin creation
    Subsidy is determined based on the current block (epoch), currently 3.125

## A coinbase tx

A coinbase of 6.27697814 - 6.25 === FEE 
Fees: 0.02697813


# Replit for Bitcoin RegTesting:

1. Go to replit
2. make an account?
3. Create a new instance?
4. expse all hidden files
5. click on nix config file 
6. add pkgs.bitcoin
7. go to shell and hit enter
8. run bitcoind -regtest -fallbackfee=0.00000025 -daemon 
     

# block rewards and burning Bitcoin:

- possible to burn bitcoin by making it an unspendable bitcoin.
- miners don't have to claim the full block reward.


# Calculating output/input/fee totals:

Pre-segwit calculations:

<!--NOTE: transactions don't include the input amounts, you have to find em elsewhere-->
fee = total inputs (sats) - total outputs (in sats)

*You can calculate the feerate as fee over the length of the tx in bytes, provided below. Round the fee to the nearest whole satoshi*

len_tx_bytes = len(raw_tx)//2 
feerate = int(fee / len_tx_bytes)



