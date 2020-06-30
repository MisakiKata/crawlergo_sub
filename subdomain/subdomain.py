from ESD import EnumSubDomain
import requests
import os

class subdomain(object):

    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                'Referer':'https://www.baidu.com',
                'X-Auth':'404 notfound'}
                
    def save(self, domain):
        try:
            r = requests.get('http://'+domain, timeout=3, headers=self.headers, verify=False)
            if r.status_code == 404 or r.status_code == 200 or r.status_code == 302:
                with open('target_tmp.txt', 'a') as ff:
                    ff.write(r.url+'\n')
        except Exception as e:
            print(e)
            pass

    def filter(self):
        list_a = []
        with open('target_tmp.txt', 'r') as f:
            list_one = set(list(f.readlines()))
            for i in list_one:
                if i.strip().rstrip('/') not in list_a:
                    list_a.append(i.strip().rstrip('/'))
        for i in list_a:
            with open('target.txt', 'a') as f:
                f.write(i+'\n')
        
    def remove(self):
        if os.path.exists('target_tmp.txt'):
            f = open('target_tmp.txt','w')
            f.truncate()
            f.close()
        if os.path.exists('target.txt'):
            f = open('target.txt','w')
            f.truncate()
            f.close()

    def main(self):
        threads = []
        self.remove()

        with open('domain.txt', 'r') as f:
            for sub in f.readlines():
                try:
                    domains = EnumSubDomain(sub.strip()).run()
                    for i in domains.keys():
                        if domains[i][0] == "0.0.0.1" or domains[i][0] == '127.0.0.1':
                            continue
                        else:
                            self.save(i)
                except Exception as e:
                    print(e)
                    pass

        self.filter()


   
    # main()
