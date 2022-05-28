from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Settings
app.secret_key = 'mysecretkey'


class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(200))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(200))


@app.route('/')
def Index():
    contacts = Contacts.query.all()
    return render_template('index.html', contacts=contacts)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        contact = Contacts(fullname=fullname, phone=phone, email=email)
        db.session.add(contact)
        db.session.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('Index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    Contacts.query.filter_by(id=int(id)).delete()
    db.session.commit()
    flash('Contact Deleted Successfully')
    return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    data = Contacts.query.filter_by(id=int(id))
    return render_template('edit-contact.html', contact=data[0])


@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        contact = Contacts.query.filter_by(id=int(id)).first()
        contact.fullname = request.form['fullname']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        db.session.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('Index'))


if __name__ == '__main__':
    app.run(debug=True)