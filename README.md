# gw-ckb-wallet-balance

run in docker
```
docker run -d -it -p 3000:3000 -e godwoken_rpc=https://v1.mainnet.godwoken.io/rpc -e godwoken_wallet=0xdf7ba4e47c4669cec08dee38a6d69d69495139ac jiangxianliang/gw-ckb-balance:0.1

curl http://127.0.0.1:3000/metrics/balance
```
