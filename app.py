from flask import Flask,redirect,render_template,request
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///shopping.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class UserInfo(db.Model):
    user_email=db.Column(db.String(50),primary_key=True)
    user_name=db.Column(db.String(50),nullable=False)
    user_password=db.Column(db.String(50),nullable=False)
    user_address=db.Column(db.String(500),nullable=False)
    
class Review(db.Model):
    user_email=db.Column(db.String(50),primary_key=True)
    user_name=db.Column(db.String(50),nullable=False)
    user_review=db.Column(db.String(500),nullable=False)

class Transactions(db.Model):
    user_email=db.Column(db.String(50),primary_key=True)
    user_name=db.Column(db.String(50),nullable=False)
    product_id=db.Column(db.Integer,nullable=False)
    product_cost=db.Column(db.Float,nullable=False)

class Products(db.Model):
    product_id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(50),nullable=False)
    product_desc=db.Column(db.String(100),nullable=False)

name_of_user=None

@app.route("/")
def index():
    return render_template("index.html",name_of_user=name_of_user)

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['passwd']
        data1=UserInfo.query.filter_by(user_email=email).first()
        global name_of_user
        try:
            if data1.user_password!=password:
                return render_template('login.html',err_id=2,name_of_user=name_of_user)
            else:
                name_of_user=data1.user_name
                return redirect("/")
        except:
            return render_template('login.html',err_id=1,name_of_user=name_of_user)
    return render_template('login.html',err_id=0,name_of_user=name_of_user)


@app.route('/signup',methods=["GET","POST"])
def signup():
    if request.method=="POST":
        user_name=request.form['username']
        user_email=request.form['email']
        passwd=request.form['passwd']
        addr=request.form['address']
        global name_of_user
        try:
            data1=UserInfo(user_name=user_name,user_email=user_email,user_password=passwd,user_address=addr)
            db.session.add(data1)
            db.session.commit()
            name_of_user=user_name
            return redirect("/")
        except:
            return render_template("signup.html",err_id=1,name_of_user=name_of_user)
    return render_template("signup.html",err_id=0,name_of_user=name_of_user)


@app.route('/products')
def products():
    return render_template("products.html",n=list(range(1,10,3)))


@app.route('/logout')
def logout():
    global name_of_user
    name_of_user=None
    return redirect("/")



if __name__=="__main__":
    app.run(debug=True)