kali recent version update

upbit api change to project for lib

 - cralwer.py
0. using rss service, excute thered by rss if throw some error control therad and restart th
1. get content from url, check the type(base domain), check of type is crypto
2. analyer of data(split using konlypy)
3. send to data



 - hdh.coin.ai
1. start training
2. make rpc runing(create mq python lib)
3. send to svc.db


- request msg

{
"content" : ["word list"],
"coin" : "BTC",
"uuid" : "uuid base time"
"detect_at" : timestamp
}

- response msg
{
"result" : {
	preplight : [1|0|-1], // is mean up : 1, down : -1, 0 : stay
	score : "",
	etc....,
}
"uuid" : "uuid base time"
}


rss or cralwer => ai => svc.db => db

svc.price_watcher => scan => checking(happen feedpack on preflight result) => happen trade

### for memo
1. build with docker
2. korean frist

### reference ###
python scheduler : https://medium.com/wasd/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%8A%A4%ED%81%AC%EB%A6%BD%ED%8A%B8-%EC%8A%A4%EC%BC%80%EC%A4%84%EB%A7%81%ED%95%98%EA%B8%B0-720dcc47b7e7