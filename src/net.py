import requests

for i in range(400):
    with open(r"12345.txt", "w") as f:
        for j in range(100):
            f.write(str(i*100+j))
            f.write(' ')
    f = open(r"12345.txt", "rb")  # 其中23020241154022.txt为自己的查询结果文件
    files = {'file': f}
    r = requests.post(url="http://121.37.1.35:5001/detectfile",files=files)#服务器地址不要修改
    k = float(r.text[11:])
    if k != 0:
        print(i,j)
        break
    else:
        print('fail')
print(r.text)
print(r.text[11:])
