from flask import Flask, render_template, session, request
from flask_mail import Mail, Message
import random


app = Flask(__name__)

app.config['MAIL_SERVER'] ="smtp.gmail.com"
app.config['MAIL_PORT']= 587
app.config['MAIL_USERNAME'] = "Your Email"
app.config["MAIL_PASSWORD"] =" " '''your app password here which is located at gmail setting and after two step verifitction you will search app password '''
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False


def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

mail = Mail(app)


@app.route("/sendOtp", methods=["POST"])
def otp_send():
    if request.method == "POST":
        print(request.form) 
        email = request.form.get("email")
        otp = generate_otp()
        session["otp"] = otp
        msg = Message("otp", sender="Your Email", recipients=[email])
        msg.body = f"Your OTP is {otp}"
        mail.send(msg)
        return "otp Sent successfully...!"
    else:
        return "error"


@app.route("/verifyotp", methods = ["POST"])
def verifyotp():
    user_otp = request.form['otp']
    if session and session['otp'] == user_otp:
        session.pop("otp", None)
        return "Otp verified Succesfully"
    else:
        return "Invalid OTP"
    
@app.route("/", methods = ["POST" , "GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.secret_key = "12345678"
    app.run(debug=True)