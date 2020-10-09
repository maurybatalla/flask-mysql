from flask import Flask ,render_template,request,redirect,url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion mysql
app.config['MYSQL_HOST']='192.185.194.19'
app.config['MYSQL_USER']='sv1com_estudio'
app.config['MYSQL_PASSWORD']='xp01Adminxp02'
app.config['MYSQL_DB']='sv1com_contactos'
mysql = MySQL(app)

# VARIABLE DE SESSION
app.secret_key  = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html',contacts = data)

@app.route('/add_contact',methods = ['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s) ', (fullname,phone,email))
        mysql.connection.commit()
        flash('CONTACTO AGREGADO DE MANERA CORRECTA')
        return redirect(url_for('Index'))

@app.route('/update/<id>',methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s , phone =%s , email = %s WHERE id = %s',(fullname,phone,email,id))
        mysql.connection.commit()
        flash('CONTACTO  ACTUALIZADO CORRECTAMENTE')
        return redirect(url_for('Index'))


@app.route('/edit_contact/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts where id= %s',(id))
    data = cur.fetchall()

    return render_template('edit-contact.html',contact = data[0])



@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('CONTACTO ELIMINADO')
    return redirect(url_for('Index')) 
    

if __name__ == '__main__':
    app.run(port= 3000 , debug=True)