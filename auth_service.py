from flask import Flask
app=Flask(__name__)
@app.route("/")
def home(): return "Auth Service"
app.run(port=5000)