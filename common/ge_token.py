import jwt
import time


class JwtToken():
    def __init__(self, user_id=24, role_id=18, name='陈雪峰', feishu='ou_a1806ef5110e6362377d81ca58efd028'):
        self.headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        self.salt = 'very_secret'

        self.payload = {"identity": {
            "user_id": user_id,
            "role_id": role_id,
            "user_name": name,
            "feishu_open_id": feishu,
            "uuid": str(user_id),
            "role": "super",
            "permission": []},
            "type": "access",
            "exp": int(time.time() + 19000)}

    def get_admin_token(self):

        token = jwt.encode(payload=self.payload, key=self.salt, algorithm='HS256', headers=self.headers).encode('utf-8')
        admin_toke = str(token)[1:]
        admin_toke = admin_toke.replace("'", "")
        # print(admin_toke)
        return admin_toke

    def token_info(self):
        token = self.get_admin_token()
        info = jwt.decode(token, self.salt, algorithms='HS256')
        if self.payload != info:
            print("无效token")
        else:
            print(True)
            print(info)
