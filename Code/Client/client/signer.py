from jose import jws

KEY = '97OhFFgOHNFHMiQ6wuqFfGn7atS0mtm1BLFlu7vsRTHlgP6FgUUp3b7_ETuzi5lsyqavKNko-TNOzbJ8UCViCg'
def sign(data):
        signed = jws.sign(data, KEY, algorithm='HS512')
        return  signed

def verify(signed):
        jws.verify(signed, KEY, algorithms=['HS512'])