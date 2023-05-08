from flask import Flask, request, render_template
import datetime,random
import mysql.connector

app = Flask(__name__)

# create a MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Avengersendgame@123",
  database="personal_fast_tag"
)

@app.route('/allrecords')
def all_records():
    # retrieve all records from the fast_tag_details table
    cursor = mydb.cursor()
    sql = "SELECT * FROM fast_tag_details"
    cursor.execute(sql)
    records = cursor.fetchall()

    # render the allrecords.html template and pass in the records
    return render_template('allrecords.html', records=records)

@app.route('/', methods=['GET', 'POST'])
def vehicle_details():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        chassis_no = request.form['chassis_no']
        vehicle_type = request.form['vehicle_type']
        amount = request.form['amount']
        expiry_date = datetime.date.today() + datetime.timedelta(days=365)
        fast_id = ''.join([str(random.randint(0, 9)) for _ in range(10)]) # generate a unique 10-digit fast_id

        # insert the data into the fast_tag_details table
        cursor = mydb.cursor()
        sql = "INSERT INTO fast_tag_details (vehicle_registration_number, chassis_number, fast_id, vehicle_type, amount, expiry_date) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (reg_no, chassis_no, fast_id, vehicle_type, amount, expiry_date)
        cursor.execute(sql, val)
        mydb.commit()

        return render_template('success.html', reg_no=reg_no, chassis_no=chassis_no, vehicle_type=vehicle_type, amount=amount, expiry_date=expiry_date, fast_id=fast_id)
    return render_template('validation.html')

@app.route('/delete', methods=['POST'])
def delete_record():
    fast_id = request.form['fast_id']

    # delete the record with the given chassis number from the fast_tag_details table
    cursor = mydb.cursor()
    sql = "DELETE FROM fast_tag_details WHERE fast_id = %s"
    val = (fast_id,)
    cursor.execute(sql, val)
    mydb.commit()

    return render_template('delete.html', fast_id=fast_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
