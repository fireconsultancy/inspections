import os
from datetime import datetime

from flask import Flask
from flask import render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# import config file with MySQL Host, User, Password and Database
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
mysql = MySQL(app)

# serve index page
@app.route("/")
def index():
    return render_template('index.html')

# serve index page
@app.route("/eb/bq/")
def building():
    return render_template('building.html')

@app.route("/favicon.ico")
def favicon():
    return "200"

@app.route("/eb/bq/<asset_no>")
def asset_url(asset_no):

    try:
        asset_no = int(asset_no)
    except ValueError:
        return render_template('building.html')

    if(asset_no<1 or asset_no>119):
        return render_template('building.html')

    #Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    #Executing SQL Statements
    query = "SELECT * FROM Broad_Quay WHERE DoorNumber=" + str(asset_no)
    cursor.execute(query)
    for data in cursor.fetchall() :
        print(data)
    cursor.close()
    
    return render_template('asset.html', data=data)

@app.route("/showAsset", methods=['POST'])
def showAsset():
    assetNumber = request.form['assetNumber']
    print("going to: ",assetNumber)
    assetURL = "/eb/bq/" + assetNumber
    return redirect(assetURL)
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8081, debug=True)