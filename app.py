from flask import Flask,render_template,request,redirect
import pymysql as sql
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,precision_score, recall_score, confusion_matrix


app=Flask("__name__")
@app.route("/",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        print("method inside post")
        uname=request.form.get("username")   
        password=request.form.get("password")
        cnf_pass=request.form.get("cnf_pass")
        print(uname)
        print(password)
        print(cnf_pass)
        if password==cnf_pass:   
           try:
               conn=sql.connect(user="root",password="",host="localhost",port=3306,database="patient_details")
               cursor=conn.cursor()
               query="insert into  patient_cred(username,pass,cnf_pass) values(%s,%s,%s);"
               cursor.execute(query,(uname,password,cnf_pass))
               print("added in the database")
           except sql.err.IntegrityError as e:
            #   check condition for duplicate entrys
                if e.args[0] == 1062: 
                    war="this usename already exist" 
                    return render_template("signup.html",war=war)
                else:
                    war=f"there is {e}"
                    return render_template("signup.html",war=war)
           except Exception as e:
               msg=f"there is {e}"
               return render_template("signup.html",msg=msg)
           else:
               print("connection is close")
               conn.commit()
               conn.close()
               return redirect("/login")
        else:
            msg="password and confirm password not match"
            return render_template("signup.html",msg=msg)
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        print("yes methood is post in login")
        uname=request.form.get("uname")
        passw=request.form.get("password")
        try:
            conn=sql.connect(user="root",password="",host="localhost",port=3306,database="patient_details")       
            cursor=conn.cursor()
            query="select username,pass from patient_cred where username=%s AND pass=%s;"
            cursor.execute(query,(uname,passw))
            print("username and pass is passed")
            user=cursor.fetchone()
            if user:
                cursor.close()
                conn.close() 
                print("connection is close")
                # conn=sql.connect(user="root",password="",host="localhost",port=3306,database="filedata")       
                # cursor=conn.cursor()
                # q="select company_type from jaipur;"
                # cursor.execute(q)
                # com_types=cursor.fetchall()
                # print(com_types)
                return redirect("/home")
            
            else:
                msgg="invalid credentials"
                return render_template("login.html",msgg=msgg)
        except sql.Error as e:
            msg=f"there is {e}"
            return render_template("login.html",msg=msg) 
    return render_template("login.html")
@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        print("yes methood is post in home")
        age=request.form.get("age")
        sex=request.form.get("sex")
        cp=request.form.get("cp")
        trestbps=request.form.get("trestbps")
        chol=request.form.get("chol")
        fbs=request.form.get("fbs")
        restecg=request.form.get("restecg")
        thalach=request.form.get("thalach")
        exang=request.form.get("exang")
        oldpeak=request.form.get("oldpeak")
        slope=request.form.get("slope")
        ca=request.form.get("ca")
        thal=request.form.get("thal")
        print(f"age:{age}")
        print(f"sex:{sex}")
        print(f"cp:{cp}")
        print(f"trestbps:{trestbps}")
        print(f"chol:{chol}")
        print(f"fbs:{fbs}")
        print(f"restecg:{restecg}")
        print(f"thalach:{thalach}")
        print(f"exang:{exang}")
        print(f"oldpeak:{oldpeak}")
        print(f"slope:{slope}")
        print(f"ca:{ca}")
        print(f"thal:{thal}")
        heart_data=pd.read_csv("heart.csv")
        print(heart_data)
        X=heart_data.drop(columns="target")
        y=heart_data["target"]
        print(X)
        print(y)
        X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42)
        print(X_train)
        print(y_train)
        y_train=y_train==1
        model=RandomForestClassifier()
        model.fit(X_train,y_train)
        y_hat=model.predict(X_train)
        accuracy=int(accuracy_score(y_train,y_hat)*100)
        print(f"accuracy_score:{accuracy}")
        y_input_pred=model.predict([[age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])
        print(f"y_pred_output: {y_input_pred}")
        precision=int(precision_score(y_train,y_hat)*100)
        print(precision)
        recall= int(recall_score(y_train,y_hat)*100)
        print(recall)
        confusion_mat= confusion_matrix(y_train,y_hat)
        print(confusion_mat)
        return render_template("result.html",accuracy_sco=accuracy,result=y_input_pred, precision_sco= precision,recall_sco=recall, confusion_mat=confusion_mat)
        
    return render_template("home.html")
@app.route("/result",methods=["GET","POST"])
def result():
    return render_template("result.html")
app.run()

