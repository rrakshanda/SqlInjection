from flask import Flask,request,render_templateimport pypyodbc app = Flask(__name__) @app.route("/")def index():    return render_template('index.html')@app.route('/processLogin', methods=['GET'])def processLogin():    userid= request.args.get('userid')    password= request.args.get('pwd')    print("Your username"+userid)    print("Your password"+password)    conn1 = pypyodbc.connect('Driver={SQL Server};Server=DESKTOP-H8DJFBD\MSSQLSERVER01;Integrated_Security=true;Database=sqli', autocommit=True)    cur1 = conn1.cursor()    sqlcmd1 = "SELECT * FROM Users WHERE username = '"+userid+"' AND password = '"+password+"'";    print(sqlcmd1)    cur1.execute(sqlcmd1)    row = cur1.fetchone()    if not row:        return render_template('index.html')    return render_template('dashboard.html')if __name__ == "__main__":    app.run()