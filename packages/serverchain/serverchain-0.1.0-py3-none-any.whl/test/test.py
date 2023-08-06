from serverchain import ServerChian

# secret = 'SCU114xxxxx'
secret = 'SCTxxxx'
serverchain = ServerChian(secret)
response = serverchain.push(title="test", desp='just for test')
print(response.text)
print(response.text.encode().decode('unicode_escape'))