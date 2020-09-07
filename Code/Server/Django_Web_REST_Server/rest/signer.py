from jose import jws

KEY = '97OhFFgOHNFHMiQ6wuqFfGn7atS0mtm1BLFlu7vsRTHlgP6FgUUp3b7_ETuzi5lsyqavKNko-TNOzbJ8UCViCg'
def sign(data):
        signed = jws.sign(data, KEY, algorithm='HS512')
        return  signed

def verify(signed):
       return jws.verify(signed, KEY, algorithms=['HS512'])

if __name__ == '__main__':
       tmp = verify("eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1dWlkIjoxMiwiaG9zdCI6Imh0dHBzOi8vZG5zLXJwei5jcy5obS5lZHU6ODAwMSIsImFwcGxpY2F0aW9ucyI6W3siaWQiOjEsIm5hbWUiOiJGaXJld2FsbC1pcHRhYmxlcyIsInZlcnNpb24iOjF9XX0.ZCOfU0q67QkSCj8pyYqHoTvJWIEobGYS5FWLpmmdtFTedNAPcx4UvTgbRJ1PZ70QYLKlJS665njIy84acve3nQ")
       print(tmp)