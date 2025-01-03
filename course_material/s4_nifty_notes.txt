session number two of base58's bitcoin (tx) protocol class

last class:
what a bitcoin tx is
we learned what bitcoin is (really just a number in a bitcoin tx somewhere in the blockchain)
we went and found a bitcoin tx in the wild
we broke it into a bunch of different fields
how much bitcoin does it spend (in the inputs)?
how much bitcoin does it lock into outputs?
there's a difference btw these numbers -> get claimed by the miner
-> talked about the super special miner transaction coinbase
-> this includes the miner subsidy (6.25bitcoin + fees)

6.37692203
6.25000000 --> block subsidy
  12692203 in fees in block 731841


version
list of inputs
list of outputs
locktime

this class:
- sizes of fields 
	-> how i was able to break the tx up by hand
	-> "hand parsing a transaction"
(the empty transaction)
- compactsize
what are the fields in a tx?

- hashes 
  why are they useful?
- where txids come from
  - (the empty transaction)

- calculating fees 
	-> how much is a fee worth per byte?
	-> important for convincing a miner to take your tx


extension:
BIPS!
funky "postmortem" BIP tx that had a LOT of inputs
input i'm spending: 
	0cabf31a3d9ac70caec915fa22502ddfc7a1e473d7d386cd7865a6200b25d92f:1
script to spend to: 76a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac

4-bytes is the "default size" for any number in most computer systems.
create new fields or data in any computer program, one big important part of designing the system
is telling the computer how big that number will ever get

there's a default setting, and whatever computer satoshi was using to write the original bitcoin
core software on, that was 4-bytes.
also, the default setting on satoshi's computer was little-endian

TX FORM:
version: is always 4-bytes long. always a number. 1,2
	01000000 -> future proofing!

inputs: 
	counter for the number of inputs: 01
	an input tells you what previous output we're spending!	
	txid: 2fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c
		32-bytes long!
	vout: 01000000  <- always 4 bytes, little endian
	scriptSig: 00 <- the length of this field is zero.
		variable length field. this proves that you can spend it.
	sequence:  4-bytes, little endian
		feffffff

outputs:
	counter of number of outputs: 01
	number of bytes for an output. (compact size, "varint")
	
	amount:	8-bytes, 99999000
	18ddf50500000000
	scriptPubKey: 19 76a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac
		variable sized field.
		lock up the bitcoin so only a certain person can spend this.

locktime: 4-bytes little endian. 
	00000000

TX FORM:
01000000
01
	 2fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c
	 01000000  
	 00 
	 feffffff

01
	18ddf50500000000
	19 76a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac

00000000


01000000012fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c0100000000feffffff0118ddf505000000001976a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac00000000

01000000012fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c010000006a47304402204512717deea5012f3d5255f065b4ee225daad8330cb2c8d045e428454a93cd4f022031057c5f78db44de22b279b86c3c95c774c1671dc672d54f65d82f7eb243f1f201210329c5e847406f309281711ca483a1a6de968478f1548252fce3d40404861c59effeffffff0118ddf505000000001976a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac00000000

broadcast transaction with id....
-> be668b9d7a2f82726d795caef43515951a3c38555dd18a5f2b072862702bc6b5


promised we'd talk about two things!
what is compact size

if there's 255 or less items, i can say "the number 255" in 1-byte, 
	ff -> 255

how many items can i fit into 2-bytes?
	ffff -> 65,535

how many items can i fit in 4-bytes?
	ffffffff -> 4,294,967,295

how many items can i fit in 8-bytes?
	ffffffffffffffff -> 18,446,744,073,709,551,615

so compact size is a field that MIGHT be 1, 2, 4, 8 bytes long!

let's say i had a scriptPubKey field (variable) with 70k bytes in it.
how many bytes do i need to say "70k"? 4-bytes

how do i tell the parser that i'm going to give you 4-bytes?

if the number is less than 253 -> put one byte
if it's more than 253 -> the first byte tells you how many more bytes to read off

   4-bytes

fc -> 0-252
fd 0000
fe 0001 1170
ff 0000 0000 0000 0000

the number of bytes in a compact size field
1, 3, 5, 9

creative encoding! minimize the amount of bytes you need to write a number, where in most cases, the
number is less than 253! has flexibility to be much much larger!


where do txids come from?

01000000012fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c010000006a47304402204512717deea5012f3d5255f065b4ee225daad8330cb2c8d045e428454a93cd4f022031057c5f78db44de22b279b86c3c95c774c1671dc672d54f65d82f7eb243f1f201210329c5e847406f309281711ca483a1a6de968478f1548252fce3d40404861c59effeffffff0118ddf505000000001976a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac00000000

broadcast transaction with id....
-> be668b9d7a2f82726d795caef43515951a3c38555dd18a5f2b072862702bc6b5


the id of a transaction (especially true for pre-segwit txs)

take the data of the signed transaction and run it through a hash function twice.


what is a hash function?

magic thing. that you can take any length of data, give it to a hash function.
hash function will "hash" the input -> always return data of a known size

NAMES OF HASH FUNCTIONS! "SHA" or "RIPEMD" -> description of the process they're gonna use to produce the hash

sha(128) -> the number of BITS that the result (after hashing) will be
sha(256) -> 32-bytes
sha512
ripemd160

the size of a tx is variable
take that tx data and put it through a hash function with a fixed result length
then i will have a fixed length identifer for a variable length item!

how to get 32-byte txid from any length tx?
1. take the raw data
2. put the data through sha256 twice!
3. reverse the bytes of the answer

cryptographic hash functions:
- it is very very difficult to figure out what the original data was if you know the hash
- if the input changes by a single bit, the output will change by a lot more than that
- same data in -> ALWAYS GET THE SAME OUTPUT

a txid is the sha256 of the sha256 of the tx data.

empty transaction? 
- not actually valid
- the minimum bytes you need to produce to get decoderawtransaction to accept it

version: 00000000
number of inputs: 00
number of outputs: 00
locktime: 00000000

empty tx: 00000000000000000000
txid:     f702453dd03b0f055e5437d76128141803984fb10acb85fc3b2184fae2f3fa78


how do you figure out the feerate of a transaction?
we know the fee is the difference btw the amount the inputs are worth - output amounts

ok. miners care about number of bytes per amount of fee that you're paying

smol tx: 10 size
size: 10
vsize: 10
weight: 40
00000000000000000000

bigger tx: 191 size
size: 191
vsize/vbytes: 191
weight: 764  <- gets weird in segwit!


4 version
1 count of inputs
32 txid
4  output number
106 + 1 for the scriptSig
4 sequence
1 count of outputs
8 amount
1 + 25 variable scriptPubKey
4 locktime

01000000012fd9250b20a66578cd86d3d773e4a1c7df2d5022fa15c9ae0cc79a3d1af3ab0c010000006a47304402204512717deea5012f3d5255f065b4ee225daad8330cb2c8d045e428454a93cd4f022031057c5f78db44de22b279b86c3c95c774c1671dc672d54f65d82f7eb243f1f201210329c5e847406f309281711ca483a1a6de968478f1548252fce3d40404861c59effeffffff0118ddf505000000001976a91448d94f3767735667a13c6d1ac75363bf1894f9e088ac00000000

size: literally how many bytes
vsize: weight / 4
weight: size times four!  

feerate is sats // vbyte

1000 sats
191 vbytes => 5.25 sats / vbyte!