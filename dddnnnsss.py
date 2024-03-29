 
from dns import resolver #dnspython导入方法
import os
import httplib2
 
iplist=[]#定义域名ip列表变量
appdomain = 'www.baidu.com'#定义业务域名
 
def get_iplist(domain=""):  ##解析域名为函数，解析成功将追加到iplist
    try:
        A = resolver.query(domain,'A')#解析A记录类型
    except Exception as e:
        print('dns resolver error:' + str(e))
        return
    for i in A:
            iplist.append(i)#追加ip到iplist
    return True
 
def checkip(ip):#对iplist中IP进行可用检测
    checkurl = str(ip) + ":80"
    getcontent=""
    httplib2.socket.setdefaulttimeout(5)#定义http连接时间超时为5秒
    conn = httplib2.HTTPConnectionWithTimeout(checkurl)#创建http连接对象
 
    try:
        conn.request("GET","/",headers = {"HOST": appdomain}) #发起url请求，添加主机头 ##通过构造html头访问目标业务主机
        response = conn.getresponse()
        getcontent = response.read(15)#获取url前15个字符，做校验用
    finally:
        if getcontent == b"<!DOCTYPE html>" :     ##判断返回字符串是否与预期相同
                                                   #监控url一般事先定义好

            print(str(ip)+'[ok]')
        else:
            print(str(ip)+'[error]')#此处可方警告、邮件、短信等
if __name__ =="__main__":
    if get_iplist(appdomain) and len(iplist) > 0:#域名解析正确至少返回一个ip
        for ip in iplist:
            checkip(ip)
    else:
        print('dns resolve error')
