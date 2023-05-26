from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, abort
from flask_restx import Api, Resource, fields
from database import db, Cars, initialize_database



app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Инициализация объекта Api
#api = Api(app, version='1.0', title='Car API', description='API for managing car data')

# # Определение модели студента
# car_model = api.model('Car', {
#     'full_name': fields.String(required=True, description='Full name of the car'),
#     'mark': fields.String(required=True, description='Mark of study'),
#     'fuel': fields.Integer(required=True, description='Semester number'),
#     'grade': fields.Integer(required=True, description='Grade'),
#     'start_year': fields.Integer(required=True, description='Year of enrollment'),
#     'age': fields.Integer(required=True, description='Age of the car')
# })

# # Пример данных о студентах
# cars = []

# # Конечная точка для получения всех студентовА
# @api.route('/cars')
# class CarsResource(Resource):
#     @api.doc('get_all_cars')
#     @api.marshal_list_with(car_model)
#     def get(self):
#         return cars

#     @api.doc('create_car')
#     @api.expect(car_model)
#     @api.marshal_with(car_model, code=201)
#     def post(self):
#         payload = request.json
#         name = payload['full_name']
#         mark = payload['mark']
#         semester = payload['fuel']
#         grade = payload['grade']
#         year = payload['start_year']
#         age = payload['age']
#         new_car = {
#             'full_name': name,
#             'mark': mark,
#             'fuel': semester,
#             'grade': grade,
#             'start_year': year,
#             'age': age
#         }
#         cars.append(new_car)
#         return payload, 201
'''
@api.route('/cars/<string:full_name>')
@api.doc(params={'full_name': 'Full name of the car'})
class CarResource(Resource):
    @api.doc('get_car')
    @api.marshal_with(car_model)
    def get(self, full_name):
        for car in cars:
            if car['full_name'] == full_name:
                return car
        api.abort(404, f'Car {full_name} not found')

    @api.doc('update_car')
    @api.expect(car_model)
    @api.marshal_with(car_model)
    def put(self, full_name):
        for car in cars:
            if car['full_name'] == full_name:
                payload = request.json
                car['full_name'] = payload['full_name']  # Обновление имени студента
                car['mark'] = payload['mark']
                car['fuel'] = payload['fuel']
                car['grade'] = payload['grade']
                car['start_year'] = payload['start_year']
                car['age'] = payload['age']
                return car
        api.abort(404, f'Car {full_name} not found')

    @api.doc('delete_car')
    @api.response(204, 'Car deleted')
    def delete(self, full_name):
        for car in cars:
            if car['full_name'] == full_name:
                cars.remove(car)
                return '', 204
        abort(404, f'Car {full_name} not found')
'''
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    mark = db.Column(db.String(120), nullable=False)
    fuel = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    @staticmethod
    def get_all_sorted(attribute):
        if attribute == 'name':
            return Car.query.order_by(Car.full_name).all()
        elif attribute == 'age':
            return Car.query.order_by(Car.age).all()
        elif attribute == 'gpa':
            return Car.query.order_by(Car.grade.desc()).all()
        elif attribute == 'mark':
            return Car.query.order_by(Car.mark).all()
        elif attribute == 'fuel':
            return Car.query.order_by(Car.fuel).all()
        elif attribute == 'start_year':
            return Car.query.order_by(Car.start_year).all()
        else:
            return Car.query.all()

    def __repr__(self):
        return f'<Car {self.full_name}>'


@app.route('/cars', methods=['GET'])
def get_all_cars():
    car = Car.query.all()
    return render_template('all_cars.html', cars=car)


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        name = request.form['full_name']
        mark = request.form['mark']
        semester = request.form['fuel']
        grade = request.form['grade']
        year = request.form['start_year']
        age = request.form['age']
        new_car = Car(full_name=name, mark=mark, fuel=semester, grade=grade, start_year=year,
                              age=age)
        db.session.add(new_car)
        db.session.commit()
        flash('Car added successfully')
        return redirect(url_for('get_all_cars'))
    return render_template('add_car.html')


@app.route('/cars/stats')
def get_car_stats():
    grades = [s.grade for s in Car.query.all()]
    average_grade = sum(grades) / len(grades)
    max_grade = max(grades)
    min_grade = min(grades)
    oldest_car = Car.query.order_by(Car.age.desc()).first()
    youngest_car = Car.query.order_by(Car.age.asc()).first()
    return render_template('stats.html', average_grade=average_grade, max_grade=max_grade, min_grade=min_grade,
                           oldest_car=oldest_car, youngest_car=youngest_car)


@app.route('/sort', methods=['GET', 'POST'])
def sort_cars():
    if request.method == 'POST':
        attribute = request.form.get('attribute')
        cars = Car.get_all_sorted(attribute)
        return render_template('all_cars.html', cars=cars)
    else:
        cars = Car.query.all()
        return render_template('sort_cars.html', cars=cars)


@app.route('/update_car', methods=['GET', 'POST'])
def update_car():
    if request.method == 'POST':
        old_full_name = request.form['old_full_name']
        new_full_name = request.form['new_full_name']
        car = Car.query.filter_by(full_name=old_full_name).first()
        if not car:
            flash(f'Car {old_full_name} not found')
            return redirect(url_for('update_car'))
        car.full_name = new_full_name
        car.age = request.form['age']
        car.grade = request.form['grade']
        car.mark = request.form['mark']
        car.fuel = request.form['fuel']
        car.start_year = request.form['start_year']
        db.session.commit()
        flash(f'Car {old_full_name} updated successfully')
        return redirect(url_for('get_all_cars'))
    else:
        return render_template('update_car.html')



@app.route('/delete_car', methods=['GET', 'POST'])
def delete_car():
    if request.method == 'POST':
        full_name = request.form['full_name']
        car = Car.query.filter_by(full_name=full_name).first()
        if not car:
            flash(f'Car {full_name} not found')
            return redirect(url_for('delete_car'))
        db.session.delete(car)
        db.session.commit()
        flash(f'Car {full_name} deleted successfully')
        return redirect(url_for('get_all_cars'))
    else:
        return render_template('delete_car.html')




# @app.route('/api')
# def api():
#     return redirect(url_for('swagger_ui', path='swagger.json'))


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    initialize_database(app)
    app.run(debug=True)