from flask import Flask,request,render_template
import random as rd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pypyodbc

app = Flask(__name__)


@app.route("/")
def index():

    return render_template('index.html')


@app.route('/processLogin', methods=['GET'])
def processLogin():
    userid = request.args.get('userid')
    password = request.args.get('pwd')
    print("Your usename:",userid)
    print("Your Password:",password)
    # Example Grammar rules
    name=userid
    pos=name.find("'");
    name=name[0:pos]
    table_name="dbo.test"
    rules = {
        "SQLAttack":[
            ["booleanAttack"],
            ["commentAttack"],
            ["piggyAttack"],
            ["unionAttack"]

        ],
        "unionAttack":[
            [userid.partition(' ')[0],"union","select"],
            [userid.partition(' ')[0],"select"]
        ],
        "piggyAttack":[
          [userid.partition(' ')[0],"semicolon","SHUTDOWN","semicolon","--"] ,
          [userid.partition(' ')[0],"semicolon","drop","table",table_name,"semicolon","--"],
          [userid.partition(' ')[0],"table",table_name,"semicolon","--"] ,
          [userid.partition(' ')[0],"SHUTDOWN","semicolon","--"] ,
          [userid.partition(' ')[0],"drop","table",table_name,"semicolon","--"],
            [userid.partition(' ')[0],"semicolon","SHUTDOWN","--"] ,
            [userid.partition(' ')[0],"semicolon","drop","table",table_name,"--"],
            [userid.partition(' ')[0],"table",table_name,"--"] ,
            [userid.partition(' ')[0],"SHUTDOWN","--"] ,
            [userid.partition(' ')[0],"drop","table",table_name,"--"]
        ],
        "semicolon":[
          ";"
        ],
        "commentAttack":[
            [name,"'--"]
        ],
        "booleanAttack":[
            [userid.partition(' ')[0],"booleanTrueExpr"],
        ],

        "opOr": [
            ["or",],
        ],
        "booleanTrueExpr": [
            ["opOr","unaryTrue"],
            ["opOr","binaryTrue"],
            ["unaryTrue"],
            ["binaryTrue"]

        ],
        "unaryTrue": [
            ["1","opEqual","1","hyphen"],
            ["2","opEqual","2","hyphen"],
            ["3","opEqual","3","hyphen"],
            ["4","opEqual","4","hyphen"],
            ["5","opEqual","5","hyphen"],
            ["6","opEqual","6","hyphen"],
            ["7","opEqual","7","hyphen"],
            ["8","opEqual","8","hyphen"],
            ["9","opEqual","9","hyphen"],
            ["0","opEqual","0","hyphen"],
            ["squote","1","squote","opEqual","squote","1","squote","hyphen"],
            ["squote","2","squote","opEqual","squote","2","squote","hyphen"],
            ["squote","3","squote","opEqual","squote","3","squote","hyphen"],
            ["squote","4","squote","opEqual","squote","4","squote","hyphen"],
            ["squote","5","squote","opEqual","squote","5","squote","hyphen"],
            ["squote","6","squote","opEqual","squote","6","squote","hyphen"],
            ["squote","7","squote","opEqual","squote","7","squote","hyphen"],
            ["squote","8","squote","opEqual","squote","8","squote","hyphen"],
            ["squote","9","squote","opEqual","squote","9","squote","hyphen"],
            ["squote","0","squote","opEqual","squote","0","squote","hyphen"],


        ],
        "binaryTrue":[
            ["parOpen","1","opEqual","1","parClose","hyphen"],
            ["parOpen","2","opEqual","2","parClose","hyphen"],
            ["parOpen","3","opEqual","3","parClose","hyphen"],
            ["parOpen","4","opEqual","4","parClose","hyphen"],
            ["parOpen","5","opEqual","5","parClose","hyphen"],
            ["parOpen","6","opEqual","6","parClose","hyphen"],
            ["parOpen","7","opEqual","7","parClose","hyphen"],
            ["parOpen","8","opEqual","8","parClose","hyphen"],
            ["parOpen","9","opEqual","9","parClose","hyphen"],
            ["parOpen","0","opEqual","0","parClose","hyphen"],
            ["parOpen","squote","1","squote","opEqual","squote","1","squote","parClose","hyphen"],
            ["parOpen","squote","2","squote","opEqual","squote","2","squote","parClose","hyphen"],
            ["parOpen","squote","3","squote","opEqual","squote","3","squote","parClose","hyphen"],
            ["parOpen","squote","4","squote","opEqual","squote","4","squote","parClose","hyphen"],
            ["parOpen","squote","5","squote","opEqual","squote","5","squote","parClose","hyphen"],
            ["parOpen","squote","6","squote","opEqual","squote","6","squote","parClose","hyphen"],
            ["parOpen","squote","7","squote","opEqual","squote","7","squote","parClose","hyphen"],
            ["parOpen","squote","8","squote","opEqual","squote","8","squote","parClose","hyphen"],
            ["parOpen","squote","9","squote","opEqual","squote","9","squote","parClose","hyphen"],
            ["parOpen","squote","0","squote","opEqual","squote","0","squote","parClose","hyphen"],
            ["parOpen","squote","","squote","opEqual","squote","","squote","parClose","hyphen"],

        ],
        "parOpen":[
            ["("]
        ],
        "parClose":[
            [")"]
        ],
        "opEqual":[
            ["="]
        ],
        "hyphen":[
            ["--"]
        ],
        "squote":[
            ["'"]
        ]

    }
    def generate_items(items):
        for item in items:
            if isinstance(item, list):
                for subitem in generate_items(item):
                    yield subitem
            else:
                yield item

            # Our expansion algo
    def expansion(start):
        for element in start:
            if element in rules:
                loc = start.index(element)
                start[loc] = rd.choice(rules[element])
            result = [item for item in generate_items(start)]

        for item in result:
            if not isinstance(item, list):
                if item in rules:
                    result = expansion(result)

        return result


    def to_string(result):
        return ''.join(result)
    final=[]
    pos=0;
    name=userid
    if(name.find("'")!=-1):
        pos=name.find("'")
    name=name[pos:len(name)]
    ml=list(name.split(" "))

    machine=list(userid.split(" "))
    machine.pop(0)
    sep=""
    mlsep=" "
    machinecheck=mlsep.join(machine)
    mlcheck=sep.join(ml)
    if mlcheck.find("'--")!=-1 or mlcheck.find("--")!=-1 or mlcheck.find("drop"+table_name)!=-1 or mlcheck.find("unionselect")!=-1 :
            for i in range(0,500):
                result = ["SQLAttack"]
                result = expansion(result) # Expand our starting list
                final.append(to_string(result))
            print(final, sep="\n")
            x = list(userid.split(" "))
            y = sep.join(x)
            print(y)
            if y in final:
                print("pattern found in cfg")
            else:
                print("not found in cfg")

            nltk.download('stopwords')

            documents = ["or 123=123",
                         "or '@@'='@@'",
                         "or 'rishi'='rishi'",
                         "or '::'='::'",
                         "or '#$%'='#$%'",
                         "or '98654'='98654'",
                         "or '  '='  ''",
                         "or 18790=18790",
                         "or '!@#$%^&*9'='!@#$%^&*9'",
                         "or 1234567890=1234567890",
                         "drop truncate delete insert from where select into drop where",
                         "union select insert union where select from drop select where insert drop into from delete",
                         "union modify drop select union from select into insert drop truncate ",
                         "union select union where from insert into drop truncate where union delete select from insert drop",
                         "union  where select insert drop truncate delete union where truncate delete select from",
                         "union select union where drop truncate delete from where insert select into delete where",
                         "union select where from delete truncate drop where insert into select from",
                         "select from insert into delete where drop select union delete where truncate",
                         "union select where from insert into drop where delete truncate from into",
                         "union select from insert where into drop  delete where truncate",
                         "union select where from insert into where drop insert drop into where insert from insert",
                         "union insert into where select from select where insert into drop insert into drop",
                         "union drop where select from select insert into  select where insert into drop insert",
                         "union insert into where select from select  into select from where insert into drop from",
                         "union where  update from select where insert select from drop where select insert drop into from",
                         "union modify where drop select  from select where into insert from where select insert drop from",
                         "union select where from insert into select from select drop insert select where insert from into",
                         "union insert where  into select from select insert into select insert drop insert from inot",
                         "union modify select from select insert drop select from drop insert from into drop",
                         "union select from select from select select insert from into drop  insert into"
                         ]
            stop = set(stopwords.words('english'))
            stop.remove(('or'))
            stop.remove(('from'))
            stop.remove(('into'))
            stop.remove(('where'))
            vectorizer = TfidfVectorizer(stop)
            X = vectorizer.fit_transform(documents)

            true_k = 2
            model = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1)
            model.fit(X)

            # prediction=2
            # if(machinecheck!=""):
            print("Prediction")
            first_test=machinecheck
            print(first_test)
            Z = vectorizer.transform([first_test])
            prediction = model.predict(Z)
            if("union" in first_test):
                print(userid," :","union attack",prediction)
            elif("or" in first_test):
                print(userid," :","boolean attack",prediction)
            elif(userid.find("drop") or userid.find("insert") or userid.find("modify") or userid.find("update") or userid.find("delete")):
                print(userid," :","piggy based attack",prediction)
            else:
                print(userid," :","comment attack",prediction)


            if y in final or (prediction==0 or prediction==1):
                    print('found attack pattern')
                    return render_template('index.html')


    else:
            print('attack pattern not found')# Print the final result



    conn1 = pypyodbc.connect('Driver={SQL Server};Server=DESKTOP-H8DJFBD\MSSQLSERVER01;Integrated_Security=true;Database=sqli', autocommit=True)

    cur1 = conn1.cursor()

    sqlcmd1 = "SELECT * FROM dbo.Users WHERE username = '"+userid+"' AND password = '"+password+"'";


    #SELECT * FROM dbo.Users WHERE username = 'rishi'-- AND password = 'ksdahfhkhfa'"
    print(sqlcmd1)


    cur1.execute(sqlcmd1)

    row = cur1.fetchone()



    if not row:

        return render_template('index.html')

    return render_template('dashboard.html')

if __name__ == "__main__":

    app.run()

