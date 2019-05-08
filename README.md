### 解压源码
```shell
mkdir aleth && tar -xvf aleth.tar.gz -C ./aleth
unzip gkc_vote-server.zip 
```
### 开启节点
```shell
sudo ./aleth/bin/aleth  -m on -a 0x944d3721E19fEcbF52A7C1721308d2B9208A9c53
```
### 开启生成账户服务
```shell
cd gkc_vote-server/genarate_key
sudo java -jar generate-private.jar
```
### 测试生成账户服务
```shell
curl 127.0.0.1:9527
```
### 运行投票服务
```shell
cd gkc_vote-server
python3.7 -m venv venv
source venv/bin/activate
sudo apt-get install  python3.7-dev #(如果报错使用 sudo apt -f install &&sudo  apt-get install  python3.7-dev)
pip install -r requirements.txt
python main.py 
```
