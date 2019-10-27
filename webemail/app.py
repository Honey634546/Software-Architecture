from flask import Flask
from myemail import webEmail
from flask import Flask, request, render_template, flash, url_for, redirect, escape
from flask_wtf import FlaskForm, CsrfProtect
from wtforms import *
from wtforms.validators import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "123456"


# app.config["WTF_CSRF_ENABLED"] = True
# CsrfProtect(app)


class emailForm(FlaskForm):
    email = StringField(label="电子邮箱地址",
                        validators=[DataRequired()])
    title = StringField(label="邮件标题", validators=[DataRequired()])
    body = TextAreaField(label="邮件内容", validators=[DataRequired()])
    file = FileField(label="上传附件")
    submit = SubmitField(label="提交")


@app.route('/')
def hello_world():
    name = request.args.get("name", "world")
    return f'Hello,{escape(name)} '


@app.route('/index', methods=["GET", "POST"])
def index():
    form = emailForm()
    if request.method == "GET":
        return render_template("index.html", form=form)
    elif request.method == "POST":
        print(request.json)
        url = request.form.get("email")
        title = request.form.get("title")
        body = request.form.get("body")
        file = request.files['file']
        print(file)
        if not file.filename:
            file = None
        if not form.validate_on_submit():
            return render_template('index.html', form=form)
        myemail = webEmail()
        urls = url.split(';')
        if len(url) == 1:
            url = urls[0]
            result, e = myemail.sendEmail(url, title, body, file)
        else:
            result, e = myemail.sendEmailBatch(urls, title, body, file)
        if result == "Y":
            # flash('successfully')
            return redirect(url_for('index'))
        elif result == 'N':
            flash(e)
            return render_template('index.html', form=form)


@app.route('/email', methods=['POST', 'GET'])
def email():
    data = eval(request.data.decode())
    print(data)
    url = data.get('url')
    title = data.get('title')
    body = data.get('body')
    myemail = webEmail()
    result, e = myemail.sendEmail(url, title, body, None)
    return f'{result,e}'


if __name__ == '__main__':
    app.run()
