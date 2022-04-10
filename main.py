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
    queryAssetInfo = "SELECT assets.assetID, assets.assetTagNo, assets.existingTag, asset_types.assetType, assets.floorNo, locations.location, assets.flatno\
                    FROM assets\
                    INNER JOIN asset_types ON assets.assetTypeID=asset_types.assetTypeID\
                    INNER JOIN locations ON assets.locationID=locations.locationID\
                    WHERE assets.assetTagNo=" + str(asset_no)

    cursor.execute(queryAssetInfo)
    for assetInfo in cursor.fetchall():
        break

    assetID = assetInfo[0]

    queryAuditInfo = "SELECT audits.auditID, MAX(audits.auditDate)AS latestAudit, results.result\
                        FROM audits\
                        INNER JOIN results ON audits.resultID = results.resultID\
                        WHERE assetID=" + str(assetID) +\
                        " GROUP BY auditID"

    cursor.execute(queryAuditInfo)
    for auditInfo in cursor.fetchall():
        break

    auditID = auditInfo[0]

    if (auditInfo[2] != "Compliant"):
        queryActions = "SELECT action_types.action, statuses.status\
                        FROM actions\
                        INNER JOIN action_types ON actions.actionID = action_types.actionID\
                        INNER JOIN statuses ON actions.statusID = statuses.statusID\
                        WHERE actions.auditID=" + str(auditID)

        cursor.execute(queryActions)

        actions = cursor.fetchall()
    else:
        actions = []

    queryImages = "SELECT images.filename, types.type\
                FROM images\
                INNER JOIN types on images.typeID=types.typeID\
                WHERE auditID=" + str(auditID)
    
    cursor.execute(queryImages)

    images = cursor.fetchall()

    cursor.close()
    
    return render_template('asset.html', assetInfo=assetInfo, auditInfo=auditInfo, actions=actions, images=images)

@app.route("/showAsset", methods=['POST'])
def showAsset():
    assetNumber = request.form['assetNumber']
    assetURL = "/eb/bq/" + assetNumber
    return redirect(assetURL)
    
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8081, debug=True)