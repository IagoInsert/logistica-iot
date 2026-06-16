from flask import Flask
app=Flask(__name__)
@app.route("/")
def home(): return "Tracking Service"
app.run(port=5001)