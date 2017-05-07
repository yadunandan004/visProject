from flask import Flask
from flask import render_template
import processing as ps
app=Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/getData")
def provideData():
	return ps.prepData()	

if __name__=="__main__":
	app.run(host='127.0.0.1',port=5000,debug=True)