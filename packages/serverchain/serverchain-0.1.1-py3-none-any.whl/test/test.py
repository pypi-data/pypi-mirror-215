from serverchain import ServerChian
from serverchain.channel import Channels

# secret = 'SCU114xxxxx'
secret = 'SCTxxxx'
serverchain = ServerChian(secret)
response = serverchain.push(title="test", desp='just for test', channel='{}|{}'.format(Channels.WECHAT_SERVICE_ACCOUNT, Channels.PUSHDEER))
print(response.text)
print(response.text.encode().decode('unicode_escape'))