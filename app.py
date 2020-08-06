from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    salary = db.Column(db.Integer)

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def __repr__(self):
        return f"EmpCode:{self.id}_{self.name}"

class EmployeeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Employee

employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

@app.route('/')
def index():
    return "hello world"

@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        emp = Employee(name, salary)
        db.session.add(emp)
        db.session.commit()
    else:
        employees = Employee.query.all()
        return employees_schema.dumps(employees)

@app.route('/employee/<id>', methods=['GET', 'PUT', 'DELETE'])
def rud_employee(id):
    if request.method == 'PUT':
        emp = Employee.query.get(id)
        emp.name = request.form['name']
        emp.salary = request.form['salary']
        db.session.commit()
        return f"Employee Updated : {employee_schema.dump(emp)}"
    elif request.method == 'DELETE':
        emp = Employee.query.get(id)
        db.session.delete(emp)
        db.session.commit()
        return f"Employee Deleted : {employee_schema.dump(emp)}"
    else:
        emp = Employee.query.get(id)
        return employee_schema.dump(emp)

# @app.route('/employee', methods=['POST'])
# def get_employees():
#     employees = Employee.query.all()
#     return employees_schema.dump(employees)

if __name__ == "__main__":
    db.create_all()
    emp_one = Employee('jithin',50000)
    db.session.add(emp_one)
    db.session.commit()
    app.run(debug=True)