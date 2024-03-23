from flask import Blueprint, render_template, request, redirect, url_for, flash, session, make_response, json, jsonify
from . import db
from .models import Users
from .__init__ import set_password, check_password
from .email import send_email
from user.token import generate_token, confirm_token
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

auth = Blueprint('auth', __name__)

# 登入函式
@auth.route('/login', methods=['GET', 'POST'])
def login():
    d = {}
    
    if request.method == 'POST':
        data = request.json
        
        login_email = data['email']
        login_password = data['password']
        user = Users.query.filter_by(email=login_email).first()
        
        if user.is_confirmed:
        
            if check_password(user, login_password):
                session['email'] = login_email
                flash('Login Success', 'success')
                print('success')
                userId = str(user.id)
                # online: False => True
                user.online = True
                db.session.add(user)
                db.session.flush()
                db.session.commit()
                
                return jsonify({'userId': userId})
            else:
                flash('Login Failed, Please Check.', 'danger')
                return jsonify(['Login Failed, Please Check.'])
                    
        else:
            return redirect(url_for("auth.resend_confirmation", username=user.username))

# 註冊函式，註冊完成將會發送驗證信至註冊信箱中
@auth.route('/register2', methods=['GET', 'POST'])
def register():
    d = {}
    
    if request.method == 'POST':
        data = request.json
        
        username = data['username']
        gender = data['gender']
        email = data['email']
        password = data['password']
        
        print(username)
                
        user = Users.query.filter_by(email=email).first()
        
        if user is None:
                
            new_user = Users(username=username, 
                            gender=gender,
                            email=email,
                            password_hashed=set_password(password)
                            )
            
            try:
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
                
            except SQLAlchemyError as e:
                db.session.rollback()
                print(str(e))            
        
            subject = "Verify your account"
            token = generate_token(email)
            confirm_url = url_for("auth.confirm_email", token=token, _external=True)
            html = render_template("confirm_email.html", confirm_url=confirm_url)
            
            send_email(email, subject, html)
            
            return jsonify({'Message': 'Register Success'})
        
        else:
            return jsonify(['username already exist'])               

# 後臺管理系統table展示頁面
@auth.route('/manage', methods=['GET', 'POST'])
def manage():
    query = Users.query.all()
        
    return render_template('manage.html', query=query)

# 後臺管理系統table的資料刪除函式
@auth.route('/delete_datas', methods=['GET', 'POST'])
def delete_datas():
    if request.method == 'POST':
        users = request.form.getlist("row_check")
        for i in users:
            user_id = int(i)
            delete_user = Users.query.filter_by(id=user_id).first()
            db.session.delete(delete_user)
            db.session.commit()
        
        if request.values.get("select_all") == "select_all":
            delete_users = Users.query.all()
          
    return redirect(url_for('auth.manage'))

# 驗證信箱連結啟動
@auth.route('/confirm/<token>')
def confirm_email(token):
    
    email = confirm_token(token)
    user = Users.query.filter_by(email=email).first_or_404()
    
    if user.is_confirmed:
        flash("Account already confirmed.", "success")
        # return redirect(url_for("auth.login"))
    
    elif email == user.email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        response = make_response("You have confirmed your account. Please return login page.", "success")
        return response
    
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
        return jsonify(['Confirm Failed'])

# 重新發送驗證碼
@auth.route("/resend/<username>")
def resend_confirmation(username):
    
    current_user = Users.query.filter_by(username=username).first()
    
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for(""))
    else:
        token = generate_token(current_user.email)
        confirm_url = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(current_user.email, subject, html)
        
        flash("A new confirmation email has been sent.", "success")
    
    return render_template("inactive.html")