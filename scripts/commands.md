### 投票
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{"sender": "0xCB8C72c8eAc53CB16E08B8897b1AaD4E335baFe4", "operate_type":1, "to": "0x29951e1A0F07A626730009062bcdFF3Be635EEab", "amount": 10}' http://127.0.0.1:3333/vote

### 签名交易发起
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{ "transaction": "0xf86d8201558307a120831e848094df96f2fc9e7ccd8a5cd517876391bcbb1cf315a1880de0b6b3a7640000801ba03b9474623bfed37c95315510c2c95f40f71ffad0a33ddad664d80eb27e936156a04f648bab4078e887ebcd642cc354abcfef7fdec95c7cb2a364e3fb16b2b42105"}' http://127.0.0.1:3333/send_signed_transaction


### transfer

curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{"sender": "0xCB8C72c8eAc53CB16E08B8897b1AaD4E335baFe4", "operate_type":1, "to": "0x29951e1A0F07A626730009062bcdFF3Be635EEab", "amount": 1}' http://127.0.0.1:3333/transfer

### 获得余额
curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:3333/get_balance?address=0x29951e1A0F07A626730009062bcdFF3Be635EEab


### 创建账户
curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:3333/create_account


### 交易是否被打包
curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:3333/is_mined?transaction_hash=
