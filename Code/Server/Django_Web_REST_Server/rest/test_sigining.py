from cryptography.hazmat.backends import default_backend
from jose import jws
import jose

if __name__ == '__main__':
    # print("hello")
    data = {
        "uuid": 12,
        "ip_rule_set": []
    }
    # #key = jwk.JWK.generate(kty='oct', size=512)
    #
    key = '97OhFFgOHNFHMiQ6wuqFfGn7atS0mtm1BLFlu7vsRTHlgP6FgUUp3b7_ETuzi5lsyqavKNko-TNOzbJ8UCViCg'

    # from cryptography.hazmat.primitives.asymmetric import ec
    #
    # key = ec.generate_private_key(ec.SECP521R1,default_backend())
    # print(key)
    # signed = jws.sign(data, key, algorithm='ES512')
    # print(signed)
    # data = jws.verify(signed, key, algorithms='ES512')
    # signed = jws.sign(data, key, algorithm='HS512')
    # print(signed)
    # data = jws.verify(signed, key, algorithms='HS512')
    # print(data)

    # key = b"""-----BEGIN PRIVATE KEY-----
    # MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQgsegINAr5xcE48BiD
    # yfXjsfQmEk1ReGtD7bSuKsKx04CgCgYIKoZIzj0DAQehRANCAASauMCp36D8FOF1
    # 5OGI1+fe5oeRoCbY5yGQ2Jk0Gi9P92ksyvC8LK7JDqtzKfEf18UsScYc+NWffEtt
    # v413G73q
    # -----END PRIVATE KEY-----"""
    # k = {'k': 'password'}
    #
    # signed = jws.sign(data, k, algorithm='ES256')
    # print(signed)
    # data = jws.verify(signed, k, algorithms='ES256')
    # print(data)



    jwk = {'k': 'password'}

    jws = jose.sign(data, jwk, alg='HS256')
    # JWS(header='eyJhbGciOiAiSFMyNTYifQ',
    # payload='eyJpc3MiOiAiaHR0cDovL3d3dy5leGFtcGxlLmNvbSIsICJzdWIiOiA0MiwgImV4cCI6IDEzOTU2NzQ0Mjd9',
    # signature='WYApAiwiKd-eDClA1fg7XFrnfHzUTgrmdRQY4M19Vr8')

    # issue the compact serialized version to the clients. this is what will be
    # transported along with requests to target systems.

    jwt = jose.serialize_compact(jws)
    # 'eyJhbGciOiAiSFMyNTYifQ.eyJpc3MiOiAiaHR0cDovL3d3dy5leGFtcGxlLmNvbSIsICJzdWIiOiA0MiwgImV4cCI6IDEzOTU2NzQ0Mjd9.WYApAiwiKd-eDClA1fg7XFrnfHzUTgrmdRQY4M19Vr8'

    jose.verify(jose.deserialize_compact(jwt), jwk, 'HS256')
    # JWT(header={u'alg': u'HS256'}, claims={u'iss': u'http://www.example.com', u'sub': 42, u'exp': 1395674427})