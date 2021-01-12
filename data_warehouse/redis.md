## 连接redis
redis-cli -h ip_addr -p port -a pwd

## 查询
keys *aaa*

get key

## 删除
del key

## key 类型
type key

## 备份
save
bgsave
config get dir 

## 查询剩余有效期
TTL key
PTTL key

## 设置过期时间
expire_key seconds
prexpire milliseconds
persist key // 移除过期时间

## 订阅
pubsub subcommand
publish channel msg // 消息发送到指定频道
subscribe channel // 订阅
psubscribe pattern1 //订阅一个或者多个频道
unsubscribe channel1 //取消订阅
punsubscribe pattern1 // 退订所有

