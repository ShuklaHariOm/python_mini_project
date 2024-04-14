from market import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market.models import Item, User, stocks
from flask_login import login_user, logout_user, login_required, current_user
from nsepython import index_info, nsetools_get_quote
from datetime import datetime


def get_company_data():
    with app.app_context():
        company_list = ["TCS", "Reliance", "HDFCBANK", "INFY", "ICICIBANK", "HINDUNILVR", "KOTAKBANK", "ITC",
                        "BAJAJFINSV", "ASIANPAINT"]
        company_data = []
        for company in company_list:
            quote = nsetools_get_quote(company)
            company_data.append((quote['symbol'], quote['lastPrice'], quote['change'], quote['pChange'],
                                 quote['previousClose'], quote['open'], quote['dayHigh'], quote['dayLow']))
        company_data.sort(key=lambda x: x[2], reverse=True)
        return company_data


def fetch_stock(stock_name):
    try:
        data1 = index_info(stock_name)
        if data1 is not None:
            stock_value = data1['last']
            variation = data1['variation']
            percent_change = data1['percentChange']
            data = [stock_name, stock_value, variation, percent_change]
            return data
        else:
            print(f"No data available for stock symbol {stock_name}")
    except KeyError:
        print(f"Unable to fetch data for stock symbol {stock_name}")


def check_stock_exists(data):
    with db.session.begin():
        stock = stocks.query.filter_by(stock_name=data[0]).first()
        if stock:
            # Update the existing stock record
            stock.stock_value = data[1]
            stock.variation = data[2]
            stock.percent_change = data[3]
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            stock.date_time = date_time
            db.session.commit()
            print(f"Updated stock record for {data[0]}")
        else:
            # Create a new stock object and insert it into the database
            now = datetime.now()
            date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
            new_stock = stocks(stock_name=data[0], stock_value=data[1], variation=data[2],
                               percent_change=data[3], date_time=date_time)
            db.session.add(new_stock)
            db.session.commit()
            print(f"Inserted new stock record for {data[0]}")


@app.route('/auto-suggestion')
def auto_suggest():
    query = request.args.get("q")
    db.query.execute('SELECT symbol FROM company WHERE symbol LIKE ?', ('%' + query + '%',))
    results = db.fetchall()
    return jsonify(results)


@app.route('/')
@app.route('/home')
def home():
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_timeout': 10}
    with app.app_context():
        data1 = fetch_stock("NIFTY 50")
        data2 = fetch_stock("NIFTY BANK")
        data3 = fetch_stock("NIFTY NEXT 50")
        data5 = fetch_stock("NIFTY MIDCAP SELECT")
        company_data = get_company_data()
        if data1[1] and data2[1] is not None:
            check_stock_exists(data1)
            check_stock_exists(data2)
        else:
            print(f"Unable to insert/update data for stock symbol {data1[0]} or {data2[0]}")
    return render_template('home.html', datas=[data1, data2, data3, data5], company_data=company_data)


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for ₹{p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}!", category='danger')
        return redirect(url_for('market'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)


@app.route('/register', methods=['GET', 'POST'])
def register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_add=form.email_add.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market'))
    if form.errors != {}:  # if there are no errors from the validations
        for err_msg in form.errors.values():
            flash(f'there was an error while creating user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash("Username or Password do not match! please try again..", category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))


@app.route('/trending_stocks')
def trending_stocks():
    company_data = get_company_data()
    return render_template('trending_stocks.html', company_data=company_data)


@app.route('/tax_calculator', methods=['GET', 'POST'])
def tax_calculator():

     if request.method == 'POST':
         income = request.form['income']
         tax_rate = request.form['tax_rate']
         tax = float(income) * float(tax_rate) / 100
         return render_template('tax_calculator.html', tax=tax)
     else:
        return render_template('tax_calculator.html')


@app.route('/brokerage_calculator', methods=['GET', 'POST'])
def brokerage_calculator():
    if request.method == 'POST':
            buy_price = request.form['buy_price']
            sell_price = request.form['sell_price']
            quantity = request.form['quantity']
            brokerage_rate = request.form['brokerage_rate']
            brokerage = (float(buy_price) * float(quantity) * float(brokerage_rate) / 100) + (float(sell_price) * float(quantity) * float(brokerage_rate) / 100)
            return render_template('brokerage_calculator.html', brokerage= brokerage)
    else:
            return render_template('brokerage_calculator.html')


# @app.route('/verify-email', methods=['GET', 'POST'])
# def verify_email():
#     form = RegisterForm()
#     if request.method == 'POST':
#         user_otp = form.email_otp.data
#         if user_otp == session['otp']:
#             # Create user account
#             user = User(username=form.username.data, email_add=form.email_add.data, password=form.password1.data)
#             db.session.add(user)
#             db.session.commit()
#             flash('Account created successfully! You can now login.', category='success')
#             return redirect(url_for('login'))
#         else:
#             flash('Invalid OTP! Please try again.', category='danger')
#     return render_template('verify_email.html', form=form)