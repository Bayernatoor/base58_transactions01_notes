Raw Tx:
nversion: 1
number of inputs: 3

input1:
    spending txid:  bc7530978073c78fbb0e020a503748130f5e10690a752eb794f6d87dd096988b (convert to little)

    vout: 0
        scriptSig_len:8a (138 or 276)
        scriptSig:47304402206213230eddf32c60167e654e3934602c0e46308932ea344a0e242699c1818f51022044895b0fc7adef9e551777d0de789d508fb56785ca80fbbfeec01b9d07b4fb7901410450128ec8ff327d0cd782702a32f51b14149d8a19b89075a56ead462363fa29ae9b35ca4f71ae8d5cd78803d835d05451ebb3ee861c80746f0e4fd5316ec306a7
        sequence: ffffffff

input 2:
    spending txid: 461af0f9c71cefe13db48b3dc396834cc19b0624b08aee7420a5f356e91c4992

    vout: 0
    scriptSig_len: 8b(139/278)
    scriptSig: 48304502207fec947609bd275a32cfd058c76678fe868c12b681c9ab0c31f716a92ba5fed0022100cd95a9ff2036a7ee0babe268ac64b425b4490be36609452ec01c11b8eaf14665014104b5a08389cbbf01178c5451f9e1c09265e73ef7bc4a1bc6761143593134e5c6460ab31ae2d5f09140a5e95a58538fd4651cb966a86de41c1a6a79b6045ecc0312
    sequence: ffffffff
input 3:
    spending txid: a1d13badbaa7ea88a1ff5a347d7b715131dcde7616ce7025876e91e75d84a33c

    vout: 0
    scriptSig_len: 6b (107/214)
    scriptSig: 483045022100a53211eed0e857dfab414f106190780c3791797b81aaf5a8a8f997681f6ea660022030a00ef0733bafa5f05026e027ac6f230c3929f9c766ef31edeabf2bcaed81740121036ec01e60571b5050bafb2d77063061a487228da342e996003e35ac7b5519e2e7
    sequence: ffffffff



number of outputs: 04

    output1:
        amount:8e2e1601
        scriptPubkey_len: 19
        scriptPubkey: 76a9142b18e0074aad70661b6fecf742cbefab4a145d1188ac
        locktime: 00000000

    output2:
        amount: 40420f00
        scriptpubkey_len: 19
        scriptpubkey: 76a914a229e570ef0c11b6a20451d65047b0fbe2c96a2f88ac
        locktime: 00000000

    output3:
        amount: 40420f00
        scriptpubkey_len: 19
        scriptpubkey: 76a91408536923b85945c704b47bb2657294757bc417dc88ac
        locktime: 00000000

    output4:
        amount: 40420f00
        scriptpubkey_len:19 
        scriptpubkey: 76a91415c307a88533528de8414fc2fc96b4e67ac0e0ef88ac
        locktime: 00000000

locktime: 00000000

RESULT:

parsed_tx = {
    "version": 1,
    "input_count": 3,
    "inputs": [
        {
            # Make sure you're parsing the txid here as big endian!! 
            # You'll know you parsed this correctly if you can find the txid when you search for it in a block explorer
            "txid": 'bc7530978073c78fbb0e020a503748130f5e10690a752eb794f6d87dd096988b',
            "vout": 0,
            "scriptSig_len": 138,
            "scriptSig": '47304402206213230eddf32c60167e654e3934602c0e46308932ea344a0e242699c1818f51022044895b0fc7adef9e551777d0de789d508fb56785ca80fbbfeec01b9d07b4fb7901410450128ec8ff327d0cd782702a32f51b14149d8a19b89075a56ead462363fa29ae9b35ca4f71ae8d5cd78803d835d05451ebb3ee861c80746f0e4fd5316ec306a7',
            "sequence": 4294967295,
        },
        {
            # Make sure you're parsing the txid here as big endian!! 
            # You'll know you parsed this correctly if you can find the txid when you search for it in a block explorer
            "txid": '461af0f9c71cefe13db48b3dc396834cc19b0624b08aee7420a5f356e91c4992',
            "vout": 0,
            "scriptSig_len": 139,
            "scriptSig": '48304502207fec947609bd275a32cfd058c76678fe868c12b681c9ab0c31f716a92ba5fed0022100cd95a9ff2036a7ee0babe268ac64b425b4490be36609452ec01c11b8eaf14665014104b5a08389cbbf01178c5451f9e1c09265e73ef7bc4a1bc6761143593134e5c6460ab31ae2d5f09140a5e95a58538fd4651cb966a86de41c1a6a79b6045ecc0312',
            "sequence": 4294967295,
        },
        {
            # Make sure you're parsing the txid here as big endian!! 
            # You'll know you parsed this correctly if you can find the txid when you search for it in a block explorer
            "txid": 'a1d13badbaa7ea88a1ff5a347d7b715131dcde7616ce7025876e91e75d84a33c',
            "vout": 0,
            "scriptSig_len": 107,
            "scriptSig": '483045022100a53211eed0e857dfab414f106190780c3791797b81aaf5a8a8f997681f6ea660022030a00ef0733bafa5f05026e027ac6f230c3929f9c766ef31edeabf2bcaed81740121036ec01e60571b5050bafb2d77063061a487228da342e996003e35ac7b5519e2e7',
            "sequence": 4294967295,
        },
    ],
    "output_count": 4,
    "outputs": [
        {
            "amount": 18230926,
            "scriptPubKey_len": 25,
            "scriptPubKey": '76a9142b18e0074aad70661b6fecf742cbefab4a145d1188ac'
        },
        {
            "amount": 1000000,
            "scriptPubKey_len": 25,
            "scriptPubKey": '76a914a229e570ef0c11b6a20451d65047b0fbe2c96a2f88ac'
        },
        {
            "amount": 1000000,
            "scriptPubKey_len": 25,
            "scriptPubKey": '76a91408536923b85945c704b47bb2657294757bc417dc88ac'
        },
        {
            "amount": 1000000,
            "scriptPubKey_len": 25,
            "scriptPubKey": '76a91415c307a88533528de8414fc2fc96b4e67ac0e0ef88ac'
        },
    ],
    "locktime": 0
}


47304402202cbc1e887dd4a374b6c55f76705441b654e2df22ee83971cae556ab9bc10943102205911b9f028eaf20dd670d2641fe13427aef707de1c58c8029325a21dcbba30b6012103786af4b32017ec640dba2d2a7e1fd5aa4a231a658e4cbc114d51c031576e19b

01
00000003
efdad76b8da190878c1de4c92fd4aaa0a287984171a4398c1140df11663cb84c
01000000
6b
483045022065db71606b84edc291eb2ec55e49ee2fd44afef8b20b4ef88fc2a01c2ba6e963022100dfb24228f2f80574d64a3a2964c5b3d054c14f0bf18c409f72345331271b5020012102a1e806a0c19aaf32363eb19e91a901eafdfc513d13f632f4e2a39f3cb894ad27
ffffffff
670fa789f11df8b202f380ebc6b4f76fa312f6bfb11494811f00411d7bbb0ae0
01000000
6b
4830450221009b5fe2b2bff2a9801725351ae2a8eb410b10b6fecb44edb442ee750e6825f1a4022038e19b3b0e3a95b4a3952dde87efc049d4a72a4424872ab768f7fb3220be4c1e0121032256cb5a8e6d3c9354da72369b939a35febb80d35e6afb50e6f348c20c6c6c05
ffffffff
52dd5a0965f2d36850f3d2ddeb1457cd72e1cd5a325656af44a3c6ba9f2d42fa
01000000
6c
4930460221008a9bf9a1ba9b4125ac9b8cf10423447ad8c7ede3414028237c4c0e0b3b3dc4fd0221009f94721c04b7d4eb33bb1aad61daf98b6ed05dfbf5e3225ae9b3afe24b8924d50121028b04194cb938044761bb93d3917abcce13f910a0500c08e61bdaaf5ea29b5ca0
ffffffff

02
b0c39203
00000000
19
76a9148a81571528050b80099821ed0bc4e48ed33e5e4d88ac
1f6ab80a
01000000
19
76a914963f47c50eaafd07c8b0a8a505c825216a4fee6d88ac
00000000

01
00000003
efdad76b8da190878c1de4c92fd4aaa0a287984171a4398c1140df11663cb84c
01000000
6b
483045022065db71606b84edc291eb2ec55e49ee2fd44afef8b20b4ef88fc2a01c2ba6e963022100dfb24228f2f80574d64a3a2964c5b3d054c14f0bf18c409f72345331271b5020012102a1e806a0c19aaf32363eb19e91a901eafdfc513d13f632f4e2a39f3cb894ad27
ffffffff
670fa789f11df8b202f380ebc6b4f76fa312f6bfb11494811f00411d7bbb0ae0
01000000
6b
4830450221009b5fe2b2bff2a9801725351ae2a8eb410b10b6fecb44edb442ee750e6825f1a4022038e19b3b0e3a95b4a3952dde87efc049d4a72a4424872ab768f7fb3220be4c1e0121032256cb5a8e6d3c9354da72369b939a35febb80d35e6afb50e6f348c20c6c6c05
ffffffff
52dd5a0965f2d36850f3d2ddeb1457cd72e1cd5a325656af44a3c6ba9f2d42fa
01000000
6c
4930460221008a9bf9a1ba9b4125ac9b8cf10423447ad8c7ede3414028237c4c0e0b3b3dc4fd0221009f94721c04b7d4eb33bb1aad61daf98b6ed05dfbf5e3225ae9b3afe24b8924d50121028b04194cb938044761bb93d3917abcce13f910a0500c08e61bdaaf5ea29b5ca0
ffffffff
02
b0c3920300000000
19
76a9148a81571528050b80099821ed0bc4e48ed33e5e4d88ac
1f6ab80a01000000
19
76a914963f47c50eaafd07c8b0a8a505c825216a4fee6d88ac
00000000




