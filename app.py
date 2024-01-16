from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    table_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Reservation('{self.date}', '{self.time}', '{self.full_name}', '{self.phone_number}', '{self.num_people}', '{self.table_type}')"

with app.app_context():
    # Create the database tables
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Get form data
        date = request.form.get('date')
        time = request.form.get('time')
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')
        num_people = request.form.get('num_people')
        table_type = request.form.get('tableType')

        # Convert datetime to time
        time_obj = datetime.strptime(time, '%H:%M').time()

        # Create a new reservation object
        new_reservation = Reservation(
            date=datetime.strptime(date, '%Y-%m-%d'),
            time=time_obj,  # Use the time object
            full_name=full_name,
            phone_number=phone_number,
            num_people=int(num_people),
            table_type=table_type
        )

        # Add the reservation to the database
        db.session.add(new_reservation)
        db.session.commit()

        # Redirect to a success page or another route
        return redirect(url_for('success'))

    return render_template('reservation.html')

@app.route('/success')
def success():
    return 'Reservation successful!'

@app.route('/view_reservations')
def view_reservations():
    reservations = Reservation.query.all()
    return render_template('view_reservations.html', reservations=reservations)

@app.route('/about')
def about():
    return render_template('about.html')

# Run the application if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
