!/bin/bash
# while true
# do 
    # curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{"sender": "0xCB8C72c8eAc53CB16E08B8897b1AaD4E335baFe4", "operate_type":1, "to": "0x29951e1A0F07A626730009062bcdFF3Be635EEab", "amount": 1}' http://127.0.0.1:3333/transfer
    # curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:3333/get_balance?address=0x29951e1A0F07A626730009062bcdFF3Be635EEab
    # sleep 1s

# done

# while true
# do 

#     curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{"sender": "0xCB8C72c8eAc53CB16E08B8897b1AaD4E335baFe4", "operate_type":1, "to": "0xf70638B7369f208E2B256b62D3655dADA5740c69", "amount": 1}' http://127.0.0.1:4444/transfer
#     curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:4444/get_balance?address=0xf70638B7369f208E2B256b62D3655dADA5740c69
#     sleep 1s

# done

test_time=1000
for index in $(seq 0 $test_time)
do 
    curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d  '{"sender": "0xCB8C72c8eAc53CB16E08B8897b1AaD4E335baFe4", "operate_type":1, "to": "0x29951e1A0F07A626730009062bcdFF3Be635EEab", "amount": 1}' http://127.0.0.1:2222/transfer
    curl -H "Accept: application/json" -H "Content-type: application/json"  http://127.0.0.1:2222/get_balance?address=0x29951e1A0F07A626730009062bcdFF3Be635EEab
    sleep 1s
done

