from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# import config file with MySQL Host, User, Password and Database
app.config.from_pyfile(os.path.join(".", "app.conf"), silent=False)
 
mysql = MySQL(app)

# serve index page
@app.route("/")
def index():
    return '''<h1>Inspections Web App - Home</h1><p>contact: webmaster@fireconsultancy.co.uk</p>'''

@app.route("/favicon.ico")
def favicon():
    return "200"

@app.route("/eb/bq/<asset_no>")
def asset_url(asset_no):

    #Creating a connection cursor
    cursor = mysql.connection.cursor()
    
    #Executing SQL Statements
    query = "SELECT PhotoSticker FROM Broad_Quay WHERE DoorNumber=" + str(asset_no)
    cursor.execute(query)
    for results in cursor.fetchall() :
        result = results[0]
        print("result=",result)
    
    #Closing the cursor
    cursor.close()

    ImageURL = "<img src=\"https://inspections-assets.s3.eu-west-2.amazonaws.com/images/" + result + "\" width=\"500\">"
    return ImageURL

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)