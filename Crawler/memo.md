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