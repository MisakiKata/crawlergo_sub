from flask import Flask, request
import requests,datetime, json

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def xray_webhook():
    vuln = request.json
    #print(vuln)
    if "vuln_class" not in vuln:
        print(vuln)
        return "ok"
        
    elif "vuln_class" in vuln and vuln["detail"]["param"] != {}:
        content = """## xray 发现了新漏洞
url: {url}
插件: {plugin}
漏洞类型: {vuln_class}
漏洞参数：{vuln_name}
漏洞POC：{payload}
请求体：{request}
发现时间: {create_time}""".format(url=vuln["detail"]["url"], plugin=vuln["plugin"],vuln_class=vuln["vuln_class"] or "Default", vuln_name=vuln["detail"]["param"]["key"], payload=vuln["detail"]["payload"],request=vuln["detail"]["request"] or vuln["detail"]["request1"] or "none",create_time=str(datetime.datetime.fromtimestamp(vuln["create_time"] / 1000)))
        return slack(content)
        
    elif "vuln_class" in vuln and vuln["detail"]["param"] == {}:
        content = """## xray 发现了新漏洞
url: {url}
插件: {plugin}
漏洞类型: {vuln_class}
发现时间: {create_time}""".format(url=vuln["target"]["url"], plugin=vuln["plugin"],
               vuln_class=vuln["vuln_class"] or "Default",
               create_time=str(datetime.datetime.fromtimestamp(vuln["create_time"] / 1000)))
        return slack(content)
        

def slack(content):
    slack = "https://hooks.slack.com/services/xxxxx"
    data = '```{content}```'.format(content=content)
    text = {'text': data}
    r = requests.post(
        slack,
        headers = {"Content-Type":"application/json"},
        data = json.dumps(text)
    )
    return "OK"
        
if __name__ == '__main__':
    app.run()
