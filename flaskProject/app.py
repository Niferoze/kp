from flask import Flask, render_template, url_for, request, redirect, session, jsonify, send_from_directory
from db import BankDB

app = Flask(__name__, static_folder='static')
BankDB = BankDB('bank.bd')
app.secret_key = '1234'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/test')
def test():
    return render_template("test.html")


@app.route('/sign-in')
def sign_in():
    return render_template("sign-in.html")


@app.route('/sign-up')
def sign_up():
    return render_template("sign-up.html")


@app.route('/user_login', methods=['POST', 'GET'])
def user_login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = BankDB.user_exists(email, password)
        if result:
            session['email'] = email
            return redirect(url_for('user_panel'))
        else:
            error_message = "Ошибка при авторизации. Попробуйте ещё раз"
    return render_template("user_login.html", error_message=error_message)


@app.route('/org_login', methods=['POST', 'GET'])
def org_login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = BankDB.org_exists(email, password)
        if result:
            session['email'] = email
            return redirect(url_for('org_panel'))
        else:
            error_message = "Ошибка при авторизации. Попробуйте ещё раз"
    return render_template("org_login.html", error_message=error_message)


@app.route('/user_reg', methods=['POST', 'GET'])
def user_reg():
    error_message = None
    organizations = BankDB.get_organizations()  # Получение списка организаций
    if request.method == 'POST':
        name = request.form['orgName']
        email = request.form['email']
        password = request.form['password']
        result = BankDB.add_user(email, password, name)
        if result:
            session['email'] = email
            return redirect('user_panel')
        else:
            error_message = "Ошибка при регистрации. Попробуйте ввести другие данные"
    return render_template("user_reg.html", error_message=error_message, organizations=organizations)


@app.route('/org_reg', methods=['POST', 'GET'])
def org_reg():
    error_message = None
    if request.method == 'POST':
        name = request.form['orgName']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        account_details = request.form['accountDetails']
        result = BankDB.add_org(email, password, name, city, account_details)
        if result:
            session['email'] = email
            return redirect('test')
        else:
            error_message = "Ошибка при регистрации. Попробуйте ввести другие данные"
    return render_template("org_reg.html", error_message=error_message)


@app.route('/org_panel', methods=['POST', 'GET'])
def org_panel():
    data = BankDB.get_transaction_info(session['email'])
    user_data = BankDB.get_users_info(session['email'])
    return render_template('org_panel.html', data=data, user_data=user_data)


@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    print('update')
    BankDB.update_transactions(data, session['email'])
    return "Updated"


@app.route('/delete', methods=['POST'])
def delete():
    data = request.get_json()
    print('delete')
    BankDB.delete_transaction(data, session['email'])
    return "Deleted"


@app.route('/add', methods=['POST'])
def add():
    data = request.get_json()
    print(data)
    BankDB.add_transaction(data, session['email'])
    return "Added"


@app.route('/updateUser', methods=['POST'])
def update_user():
    user_data = request.get_json()
    print('user_data')
    BankDB.update_users(user_data, session['email'])
    return "User Updated"


@app.route('/deleteUser', methods=['POST'])
def delete_user():
    user_data = request.get_json()
    print(user_data)
    BankDB.delete_users(user_data, session['email'])
    return "User Deleted"


@app.route('/addUser', methods=['POST'])
def add_user():
    print(session)
    user_data = request.get_json()
    print(user_data)
    BankDB.org_add_users(user_data[0], user_data[1], session['email'])
    return "User Added"


#export_completed = False


@app.route('/export', methods=['POST', 'GET'])
def export():
    save_directory = 'путь/к/директории/экспорта'  # Предопределённая директория для экспорта
    BankDB.export_db_to_files(save_directory)

    # Возвращаем URL для экспортированных файлов
    return jsonify({
        'files': [
            '/download/all_data.json',
            '/download/all_data.csv',
            '/download/all_data.xml'
        ]
    })

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    save_directory = 'path/to/export/directory'  # Same directory used in export
    return send_from_directory(save_directory, filename, as_attachment=True)


#@app.route('/export/status', methods=['GET'])
#def export_status():
 #   global export_completed
  #  return jsonify({'completed': export_completed})


@app.route('/import', methods=['POST'])
def import_file():
    file = request.files['file']
    BankDB.import_data(file, session['email'])
    return "Database imported"


@app.route('/user_panel', methods=['POST', 'GET'])
def user_panel():
    print(session['email'])
    org_mail = BankDB.get_organization_email(session['email'])
    data = BankDB.get_transaction_info(org_mail)
    return render_template('user_panel.html', data=data)


if __name__ == "__main__":
    app.run(debug=True)
