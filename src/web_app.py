from flask import Flask, render_template, request
from src import db_manager, config

app = Flask(__name__,
            template_folder=config.TEMPLATES_DIR,
            static_folder=config.STATIC_DIR)

db_manager.init_db()


@app.route('/')
def index():
    products = db_manager.get_products()[:2]
    return render_template('index.html', products=products)


@app.route('/catalog')
def catalog():
    products = db_manager.get_products()
    categories = db_manager.get_categories()
    return render_template('catalog.html', products=products, categories=categories)


@app.route('/category/<category_name>')
def category(category_name):
    products = db_manager.get_products(category_name)
    categories = db_manager.get_categories()
    return render_template('category.html', products=products, categories=categories, current_category=category_name)


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if name and email and message:
            db_manager.save_contact(name, email, message)
            return render_template('contacts.html', success=True)

    return render_template('contacts.html')


@app.route('/product/<int:product_id>')
def product(product_id):
    products = db_manager.get_products()
    product_data = next((p for p in products if p[0] == product_id), None)

    if product_data:
        return render_template('product.html', product=product_data)
    else:
        return "Товар не найден", 404


@app.route('/profile')
def profile():
    return render_template('profile.html')


def run():
    app.run(host=config.HOST, port=config.PORT, debug=True)