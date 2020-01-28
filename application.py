from flask import Flask, request, jsonify, make_response
import jwt
import datetime
from functools import wraps

application = Flask(__name__)

secret_key = "chavesecreta" #essa chave fica guardada, o hacker não pode ter acesso a ela.
informacao_tokenizada = "1234567890" #a informação pode ser decodificada, mas o hacker não poderá alterar ela.
token = ""  #token conterá header . payload . signature

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #pegamos o token da URL (query string)
        token = request.args.get('token')
        try:
            data = jwt.decode(token, secret_key)
            return f(*args, **kwargs)
        except:
            return jsonify({"mensagem": "token invalido"})
    return decorated

#rota que não precisa de token
@application.route("/desprotegido")
def desprotegido():
    return jsonify({"mensagem": "desprotegido"})


#rota que precisa de token
@application.route("/protegido")
@token_required
def protegido():
    return jsonify({"mensagem": "protegido"})



@application.route("/tokenizar")
def tokenizar():
    token = jwt.encode({"alguma_informacao": informacao_tokenizada, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=2)}, secret_key)
    return jsonify({"token": token.decode("UTF-8")})

@application.route("/decodificar")
def decodificar():
    return str(token.decode())



if __name__ == "__main__":
    application.run(debug=True)
