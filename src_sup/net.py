import requests
# import os
# print(os.listdir())
f = open(r"37220222203885.txt", "rb")  # 其中23020241154022.txt为自己的查询结果文件
files = {'file': f}
r = requests.post(url="http://121.37.1.35:5001/detectfile",files=files)#服务器地址不要修改
print(r.text)
print(r.text[11:])
