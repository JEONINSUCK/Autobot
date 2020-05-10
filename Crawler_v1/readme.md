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



# url list

### find url

### ENG SIDE

provider rss service

https://cointelegraph.com/rss/tag/altcoin
https://cointelegraph.com/rss/tag/bitcoin
https://cointelegraph.com/rss/tag/blockchain
https://cointelegraph.com/rss/tag/ethereum
https://cointelegraph.com/rss/tag/litecoin
https://cointelegraph.com/rss/tag/monero
https://cointelegraph.com/rss/tag/regulation
https://cointelegraph.com/rss/category/analysis
https://cointelegraph.com/rss/category/top-10-cryptocurrencies
https://cointelegraph.com/rss/category/market-analysis
https://cointelegraph.com/rss/category/weekly-overview

### KOR SIDE

RSS
http://www.coindeskkorea.com/rss/S1N8.xml
http://www.coindeskkorea.com/rss/allArticle.xml

cron
https://kr.investing.com/crypto/xrp/news interval of 1 hour
https://kr.investing.com/crypto/xrp/analysis interval of 1 hour
https://www.coindeskkorea.com once of day
http://m.coinreaders.com/b.html?sc=sc10
http://m.coinreaders.com/b.html?sc=sc6 once of day
https://cceeddcc.tistory.com/8


### find url
1. find url
https://kr.investing.com/crypto/xrp/news interval of 1 hour
https://kr.investing.com/crypto/xrp/analysis interval of 1 hour
https://www.coindeskkorea.com once of day
http://m.coinreaders.com/b.html?sc=sc10
http://m.coinreaders.com/b.html?sc=sc6 once of day

https://cceeddcc.tistory.com/8

eng side
provider rss service
https://cointelegraph.com/rss-feeds

http://www.coindeskkorea.com/rss/S1N8.xml
http://www.coindeskkorea.com/rss/allArticle.xml

### start RSS

xmlUrl="http://www.cryptocoinsnews.com/feed/"
xmlUrl="http://cryptocur.com/feed/"
xmlUrl="http://feeds.feedburner.com/CoinDesk"
xmlUrl="http://www.reddit.com/r/NuBits/.rss"
xmlUrl="http://le-coin-coin.fr/feed/"
xmlUrl="http://www.coinjockey.com/feed/"
xmlUrl="https://www.google.fr/alerts/feeds/03608699083601741120/2317463790769430578"
xmlUrl="http://bitsofproof.com/?feed=rss2"
xmlUrl="https://blog.conformal.com/category/bitcoin/feed/"
xmlUrl="http://crypto-news.com/feed/"
xmlUrl="http://cryptosource.org/feed/"
xmlUrl="http://www.reddit.com/r/opentransactions/.rss"
xmlUrl="http://blog.oleganza.com/rss"
xmlUrl="http://bitcoinexaminer.org/feed/"
xmlUrl="http://bitcoinsinsider.com/rss/"
xmlUrl="http://www.meetup.com/BdxCoin/events/rss/"
xmlUrl="http://www.coinspectator.com/feed/"
xmlUrl="http://thegenesisblock.com/feed/"
xmlUrl="http://www.thebitcoin.fr/feed/"
xmlUrl="http://www.reddit.com/r/peercoin/.rss"
xmlUrl="http://blog.lavoiedubitcoin.info/feed/atom"
xmlUrl="https://ripple.com/feed/"
xmlUrl="http://www.reddit.com/r/Peerbox/.rss"
xmlUrl="http://www.reddit.com/user/oleganza/.rss"
xmlUrl="http://otblog.net/feed/"
xmlUrl="http://bitcoinism.liberty.me/feed/"
xmlUrl="http://www.primecoiner.com/feed/"
xmlUrl="http://www.cryptocanard.com/feed/"
xmlUrl="http://cointelegraph.com/rss"

### start get content

