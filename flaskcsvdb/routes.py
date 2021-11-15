#https://www.youtube.com/watch?v=cYWiDiIUxQc&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=4
import os
from flask import render_template, url_for, flash, redirect, request, abort, send_file
from flaskcsvdb import app, db
from flaskcsvdb.forms import RegistrationForm, LoginForm, UpdateAccount, PostForm
from flaskcsvdb.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from pogoda import pobierzpogode

# @app.route("/")
# def hello():
#     return 'Hello'


@app.route("/base")
@login_required
def home():
    posts=Post.query.filter_by(user_id=current_user.id).all()
     #posts= Post.query.all()
   # df=pd.read_csv(r'flaskcsvdb/static/csv/'+posts.csv ,sep=';')
    return render_template('base.html', posts=posts)#, tables=[df.to_html(classes='data')], titles=df.columns.values)#, places=places,names_of_rows=names_of_rows,ilosc_kolumn=ilosc_kolumn)#,places=places)

@app.route("/pogoda")
def pokazpogode():
  temp,humid,weathertype,rain = pobierzpogode()
  return render_template("pogoda.html", temp=temp, humid=humid,weathertype=weathertype, rain=rain)

@app.route("/post/<int:post_id>/download")
@login_required
def download_file(post_id):
    #https://www.youtube.com/watch?v=sy1MNWt7om4
    post = Post.query.get_or_404(post_id)
    csv_path = 'static/csv/' + post.csv
    return send_file(csv_path)


@app.route("/post/<int:post_id>")
@login_required
def post(post_id):

    #https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    post=Post.query.get_or_404(post_id)
    df = pd.read_csv(r'flaskcsvdb/static/csv/' + post.csv, sep=r'\,|\t|\;|\ |\n',nrows=100 )
    # with open('flaskcsvdb/static/csv/'+post.csv,'r') as csv_file:
    #     data = csv_attribute.reader(csv_file, delimiter=';')
    #     places = []
    #     # with open('username.csv', 'r') as csv_file:
    #     #     data = csv.reader(csv_file, delimiter=';')
    #     #     for row in data:
    #     #         print(row)
    #     names_of_rows = []
    #     for row in data:
    #         ilosc_kolumn = len(row) - 1
    #         places.append({"Username": row[0],"Identifier": row[1],"First": row[2],"Last": row[3]})

    return render_template('csv.html',title=post.title, post=post, csv=post.csv, tables=[df.to_html(classes='data')], titles=df.columns.values)

# @app.route("/")
# def index():
#     # cwd = os.getcwd()  # Get the current working directory (cwd)
#     # files = os.listdir(cwd)  # Get all the files in that directory
#     # print("Files in %r: %s" % (cwd, files))
#
#     with open('flaskcsvdb/static/csv/username.csv','r') as csv_file:
#         data = csv_attribute.reader(csv_file, delimiter=';')
#         first_line = True
#         places = []
#         # with open('username.csv', 'r') as csv_file:
#         #     data = csv.reader(csv_file, delimiter=';')
#         #     for row in data:
#         #         print(row)
#         for row in data:
#             if not first_line:
#                 places.append({"Username": row[0],"Identifier": row[1],"First": row[2],"Last": row[3]})
#             else:
#                 first_line = False
#         return render_template('index.html', places=places,title='Index')



@app.route("/")
def about():
    return render_template('about.html', title='About')


@app.route("/register" , methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        #pass
        return render_template('about.html', title='About')
    form = RegistrationForm()
    if form.validate_on_submit():
        # sprawiałem by po dodaniu drugiego takeigo samego urzytkownika (all the same) nie było errora
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Konto zostało stworzone!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        #pass
        return render_template('about.html', title='About')
    form = LoginForm()
    if form.validate_on_submit():
        # sprawdza poprownośc danych z bazy
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Jesteś zalogowany!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Sprawdz popraność danych', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    flash(f'Wylogowałeś się!', 'success')
    return redirect(url_for('about'))

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Zaktualizowano Twój profil!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

def save_picture(from_pic):
    # random_hex = secrets.token_hex(8)
    # _, f_ext = os.path.splitext(from_csv.filename)
    # picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', from_pic.filename)
    from_pic.save(picture_path)
    return from_pic.filename

def save_csv(form_csv):
   # random_hex = secrets.token_hex(8)
    #_, f_ext = os.path.splitext(form_csv.filename)
    #csv_fn = random_hex + f_ext
    csv_path = os.path.join(app.root_path, 'static/csv', form_csv.filename)
    form_csv.save(csv_path)
    return form_csv.filename

@app.route("/csv/new", methods=['GET', 'POST'])
@login_required
def new_csv():
    form= PostForm()
    if form.validate_on_submit():
        if form.csv.data:
            csv_file = save_csv(form.csv.data)
            form.csv = csv_file
        csv = url_for('static', filename='csv/' + form.csv)
        post = Post(title=form.title.data, content=form.content.data,  author=current_user,csv=form.csv)
        db.session.add(post)
        db.session.commit()
        flash('Dodano csv!','success')
        return redirect(url_for('home'))
    return render_template('create_csv.html', title='New CSV', form=form , legend ='New CSV')



@app.route("/csv/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_csv(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content = form.content.data
        csv_file = save_csv(form.csv.data)
        post.csv= csv_file
        db.session.commit()
        flash('Twój csv został zaktualizowany', 'success')
        return  redirect(url_for('post', post_id=post.id))
    elif request.method =='GET':
        form.title.data=post.title
        form.content.data = post.content
        form.csv.data=post.csv
    return render_template('create_csv.html', title='Update CSV', form=form, legend ='Update CSV')#csv=csv

@app.route("/csv/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_csv(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Usunąłeś csv!', 'success')
    return redirect(url_for('home'))