import jwt
from django.conf import settings

def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        print("Le jeton a expiré.")
    except jwt.InvalidTokenError:
        print("Le jeton est invalide.")
    except Exception as e:
        print("Une erreur s'est produite lors du décodage du jeton :", str(e))

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMDMyOTQyNywiaWF0IjoxNzEwMjQzMDI3LCJqdGkiOiJlZGI1NTEyMGQ1ZTU0ZjlkYjhiNTVhMjE5ODI5MTcxYSIsInVzZXJfaWQiOiJ0ZXN0MDFAZ21haWwuY29tIiwiZW1haWwiOiJ0ZXN0MDFAZ21haWwuY29tIiwiaWQiOjF9.QN-kCkImk1nhdsNJzMmmetXiCraJnrCPBOvoeqYvoWY"
decoded_token = decode_token(access_token)
print(decoded_token)