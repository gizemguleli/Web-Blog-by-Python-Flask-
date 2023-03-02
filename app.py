from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import sqlite3
import datetime

app = Flask(__name__)

DATABASE = 'DB.db'
app.secret_key = 'mysecretkey'



@app.route("/index")
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Execute the SELECT query
    c.execute("SELECT title, context, date,name,post_id,u.ID FROM posts p ,user u where u.ID = p.user_id ")

    # Fetch all the rows from the result set
    rows = c.fetchall()

    # Close the connection
    conn.close()

    return render_template('index.html',posts=rows)

@app.route('/post/<int:id>/', methods=['POST','GET'])
@app.route('/post', methods=['POST','GET'])

def post(id=None):
    if request.method == 'POST':
        title = request.form['title'] 
        context = request.form['context'] 
        post_id = request.form['postId'] 
        userId = session['Id']
        current_date = datetime.date.today()

        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()


        if post_id:
            c.execute('UPDATE posts SET title=?, context=?, date=? WHERE post_id=?',(title, context, current_date, post_id))

        else :
            # Execute the INSERT query
            c.execute("INSERT INTO posts (title, context, user_Id, date) VALUES (?, ?, ?, ?)", (title, context, userId, current_date))
       

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        return redirect(url_for('index'))


        
    if id:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        # Execute the SELECT query
        c.execute("SELECT title, context,post_id FROM posts  where post_id = ? ", (id,))

        # Fetch all the rows from the result set
        row = c.fetchone()

        # Close the connection
        conn.close()

        return render_template('post.html',post=row)
    return render_template('post.html',post=None)

@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        fname = request.form['fname'] 
        lname = request.form['lname']
        Address = request.form['Address']
        Phone = request.form['Phone']
        
        psw = request.form['psw']

        # saving the data into our sql database
        # create a cursor object
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        # execute the INSERT query
        cur.execute("UPDATE user SET name=?,surname=?, adress=?, phone=?, password=? WHERE ID=?", (fname, lname, Address,Phone, psw, session['Id']))
   
        # commit the transaction
        conn.commit()

        # close the cursor and database connection
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    user_id = session['Id']

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Execute the SELECT query
    c.execute("SELECT name,surname,email,adress,phone,username,password FROM user where ID =?",(user_id,))

    # Fetch all the rows from the result set
    row = c.fetchone()

    # Close the connection
    conn.close()

    return render_template('profile.html',user=row)

@app.route('/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        uname = request.form['uname'] 
        psw = request.form['psw']
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("SELECT ID,name FROM user WHERE username = ? AND password = ?", (uname, psw))
        user = cur.fetchone()
        cur.close()
        conn.close()
        print(user)
        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            session['Id'] = user[0]

            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        fname = request.form['fname'] 
        lname = request.form['lname']
        Address = request.form['Address']
        Phone = request.form['Phone']
        email = request.form['email']
        uname = request.form['uname']
        psw = request.form['psw']

        # saving the data into our sql database
        # create a cursor object
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()

        # execute the INSERT query
        cur.execute("INSERT INTO user (name, surname, email, adress, phone, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)", (fname,lname,Address,Phone,email,uname,psw))

        # commit the transaction
        conn.commit()

        # close the cursor and database connection
        cur.close()
        conn.close()

    return render_template('register.html')

@app.route('/deletePost/<int:id>/', methods=['GET'])
def deletePost(id=None):
    # connect to database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # execute the delete query
    c.execute('DELETE FROM posts WHERE post_id=?', (id,))
    # commit the changes to the database
    conn.commit()
    # close the database connection
    conn.close()
    return redirect(url_for('index'))

@app.route('/like', methods=['POST'])
def like():
    # Get the post ID from the request data
    post_id = request.form['post_id']

    # Increment the like count for the post
    if post_id in post_likes:
        post_likes[post_id] += 1
    else:
        post_likes[post_id] = 1

    # Return the updated like count for the post
    return jsonify({'post_id': post_id, 'likes': post_likes[post_id]})


if __name__ == "__main__":
    app.run()

