### 添加xhy user
```shell
sudo adduser xhy
sudo usermod -aG sudo xhy
su xhy 
```
### 解压链的可运行文件
```shell
sudo tar -xvf aleth.tar.gz -C ./aleth
```
### 开启节点
```shell
sudo /home/xhy/aleth/bin/aleth  --db-path /home/xhy/testData --ipcpath /home/xhy/testData -m on -a 0x944d3721E19fEcbF52A7C1721308d2B9208A9c53
```
### 运行投票服务
```shell
git clone https://github.com/mxito3/gkc_vote
cd gkc_vote
python3.7 -m venv venv
source venv/bin/activate
git checkout remotes/origin/server -b server
sudo apt-get install  python3.7-dev (如果报错使用 sudo apt -f install &&sudo  apt-get install  python3.7-dev)
pip install -r requirements.txt
python main.py 
