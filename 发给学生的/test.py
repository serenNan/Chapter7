import json

## 读取json文件
def readjsonfile(filename):
    with open(filename,'r',encoding="utf-8") as f:
        jsonobj=json.load(f) ##从文件中读取json
        print(json.dumps(jsonobj,ensure_ascii=False,indent=4)) ##格式化输出json对象


## 写入文件
def writefile(filename):
    with open(filename,'w',encoding="utf-8") as f:
        f.write("hello world") ##字符串写入
        lines=["hello\n","world\n"]
        f.writelines(lines) ##批量写入


## json对象操作
def handlerjson():
    jsonobj={} ##声明一个json对象
    jsonobj["username"]="李文杰" ##给json增加一个key value键值对
    jsonobj["age"]=23

    print(jsonobj["username"]) ##获取json某个key的值

    parentjson={}
    parentjson["childnode"]=jsonobj ##可以将json作为value赋值给另一个json对象

    print(json.dumps(parentjson,ensure_ascii=False,indent=4))



if __name__ == '__main__':
    handlerjson()
