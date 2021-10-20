from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2  # pip install psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "Secret Key"

DB_HOST = "localhost"
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)


# This is the index route where we are going to
# query on all our book data
@app.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    b = "SELECT b.book_id,b.book_title, b.book_desc, b.book_price, a.author_name, a.author_id, g.genre_id, " \
        "g.genre_type from book b inner join author a on a.author_id = b.author_id " \
        "inner join genre g on b.genre_id = g.genre_id"
    cur.execute(b)  # Execute the SQL
    list_books = cur.fetchall()
    a = "SELECT * FROM author"
    cur.execute(a)  # Execute the SQL
    list_authors = cur.fetchall()
    g = "SELECT * FROM genre"
    cur.execute(g)  # Execute the SQL
    list_genres = cur.fetchall()
    print(list_books)
    return render_template('index.html', list_books=list_books, list_authors=list_authors, list_genres=list_genres)


@app.route('/insert', methods=['POST'])
def insert():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        btitle = request.form['btitle']
        bdesc = request.form['bdesc']
        bprice = request.form['bprice']
        author = request.form['author']
        genre = request.form['genre']
        cur.execute("INSERT INTO book (book_title, book_desc, book_price, author_id, genre_id) VALUES (%s,%s,%s,%s,%s)",
                    (btitle, bdesc, bprice, author, genre))
        conn.commit()

        flash("Book details inserted Successfully")

        return redirect(url_for('Index'))


# this is our update route where we are going to update book details
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form['id']
        btitle = request.form['btitle']
        bdesc = request.form['bdesc']
        bprice = request.form['bprice']
        author = request.form['author']
        genre = request.form['genre']

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        sql_update_query = """update book set book_title = %s, book_desc = %s, book_price = %s, author_id =%s, 
                                  genre_id =%s where book_id = %s"""
        cur.execute(sql_update_query, (btitle, bdesc, bprice, author, genre, id))
        flash('Book Updated Successfully')
        conn.commit()

        return redirect(url_for('Index'))


# This route is for deleting book details
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute('DELETE FROM book WHERE book_id = {0}'.format(id))
    conn.commit()
    flash('Book Removed Successfully')

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')
