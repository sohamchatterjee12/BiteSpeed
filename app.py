from db_connector import update_db
from flask import Flask, request

app = Flask(__name__)

@app.route("/identify", methods=["POST"])
def identify():

    content = request.json
    email = content.get("email")
    phone_number = content.get("phoneNumber")
    
    res = update_db(email, phone_number)
    return res

if __name__ == "__main__":
    app.run(debug=True)


