from flask import Flask, render_template, request, url_for, redirect
import mysql.connector
app = Flask(__name__, template_folder="kursov18var_templates")

def DB_connect(us:str, passw:str):
    try:
        conn = mysql.connector.connect(
            user = us, 
            password = passw, 
            host = "127.0.0.1",
            database = "kurs"
            )
    except:
        conn = None
    return conn

conn = DB_connect("root", "280500")
cursor = conn.cursor()

def checkReport(year):
    _SQL = """
        SELECT COUNT(*)
	        FROM genre_income
		        WHERE year = %(reportYear)s;
    """
    cursor.execute(_SQL, {"reportYear": year})
    result = cursor.fetchall()
    return result[0][0]

@app.route('/', methods=['post', 'get'])
def menu():
    try:
        ref = request.args['ref']
    except:
        ref = None

    if (ref == '1'):
        return redirect(url_for('request1'))
    if (ref == '2'):
        return redirect(url_for('request2'))
    if (ref == '3'):
        return redirect(url_for('request3'))
    if (ref == '4'):
        return redirect(url_for('request4'))
    if (ref == '5'):
        return redirect(url_for('request5'))
    if (ref == '6'):
        return redirect(url_for('request6'))
    if (ref == '7'):
        return redirect(url_for('request7'))
    if (ref == '7_show'):
        return redirect(url_for('request7_show'))

    if(ref == 'exit'):
        return 0
    return render_template('menu.html')

@app.route('/request1', methods=['post', 'get'])
def request1():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
      SELECT 
    delivery_list.idDel,
    cost_of_inst,
    SUM(number_of_inst) AS totalNum
FROM
    delivery_list
        INNER JOIN
    consignment ON consignment.idCons = delivery_list.idCons
WHERE
    MONTH(date_of_const) = 3
        AND YEAR(date_of_const) = 2017
GROUP BY idDel;
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["idDel", "cost_of_inst", "totalNum"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request1.html", Data = res)

@app.route('/request2', methods=['post', 'get'])
def request2():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
        SELECT 
    publishing_house.idPub, pub_name, SUM(full_cost) AS totalCost
FROM
    publishing_house
        INNER JOIN
    consignment ON consignment.idCons = publishing_house.idCons
WHERE
    MONTH(date_of_const) = 3
        AND YEAR(date_of_const) = 2017
        GROUP BY idPub;
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["idPub", "pub_name", "totalCost"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request2.html", Data = res)

@app.route('/request3', methods=['post', 'get'])
def request3():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    if (request.method == 'POST'):
        ID = request.form.get('ID')  

        data = (ID, ID)
        _SQL = """
            SELECT 
	publishing_house.idPub,
    address,
    pub_name,
    phone_number,
    full_name_of_cont,
    date_of_establishment,
    date_of_contract_forming
FROM
    publishing_house
        INNER JOIN
    delivery_list ON delivery_list.idDel = publishing_house.idDel
        INNER JOIN
    book ON book.idBook = publishing_house.idBook
        INNER JOIN
    consignment ON consignment.idCons = publishing_house.idCons
WHERE
    book.name = %s
       AND cost_of_inst = (SELECT 
            MAX(cost_of_inst)
        FROM
            publishing_house
                INNER JOIN
            delivery_list ON delivery_list.idDel = publishing_house.idDel
				INNER JOIN
			consignment ON consignment.idCons = publishing_house.idCons
        WHERE
            book.name = %s
                AND MONTH(date_of_const) = 3
                AND YEAR(date_of_const) = 2017)
        AND MONTH(date_of_const) = 3
        AND YEAR(date_of_const) = 2017;
        """
        cursor.execute(_SQL, data)
        result = cursor.fetchall()
        scheme = ["idPub", "address", "pub_name", "phone_number", "full_name_of_cont", "date_of_establishment", "date_of_contract_forming"]
        for client in result:
            res.append(dict(zip(scheme, client)))
    return render_template("request3.html", Data = res)

@app.route('/request4', methods=['post', 'get'])
def request4():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
       SELECT 
	publishing_house.idPub,
    address,
    pub_name,
    phone_number,
    full_name_of_cont,
    date_of_contract_forming,
    date_of_contract_forming
FROM
    publishing_house
        INNER JOIN
    delivery_list ON delivery_list.idDel = publishing_house.idDel
        INNER JOIN
    consignment ON consignment.idCons = publishing_house.idCons
WHERE
        full_cost = (SELECT 
            MAX(full_cost)
        FROM
            publishing_house
                INNER JOIN
            delivery_list ON delivery_list.idDel = publishing_house.idDel
				INNER JOIN
			consignment ON consignment.idCons = publishing_house.idCons
        WHERE
                MONTH(date_of_const) < 7
                AND YEAR(date_of_const) = 2017)
        AND MONTH(date_of_const) < 7
        AND YEAR(date_of_const) = 2017
        GROUP BY idPub;
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["idPub", "address", "pub_name", "phone_number", "full_name_of_cont", "date_of_establishment", "date_of_contract_forming"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request4.html", Data = res)

@app.route('/request5', methods=['post', 'get'])
def request5():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
        SELECT 
	publishing_house.idPub,
	address,
    pub_name,
    phone_number,
    full_name_of_cont,
    date_of_contract_forming,
    date_of_contract_forming
    FROM publishing_house
        LEFT JOIN consignment ON consignment.idCons = publishing_house.idCons
            WHERE consignment.idCons IS NULL;
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["idPub", "address", "pub_name", "phone_number", "full_name_of_cont", "date_of_establishment", "date_of_contract_forming"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request5.html", Data = res)

@app.route('/request6', methods=['post', 'get'])
def request6():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
        SELECT 
	publishing_house.idPub
    address,
    pub_name,
    phone_number,
    full_name_of_cont,
    date_of_establishment,
    date_of_contract_forming
FROM
    publishing_house
        LEFT JOIN
    (SELECT 
        *
    FROM
	consignment 
    WHERE
        MONTH(date_of_const) = 3
            AND YEAR(date_of_const) = 2017) AS tmp ON publishing_house.idPub = tmp.idPub
WHERE
    tmp.idCons IS NULL;
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["idPub", "address", "pub_name", "phone_number", "full_name_of_cont", "date_of_establishment", "date_of_contract_forming"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request6.html", Data = res)

@app.route('/request7', methods=['post', 'get'])
def request7():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    isExist = -1
    if (request.method == 'POST'):
        year = request.form.get('year')
        if(checkReport(year) > 0):
            isExist = 1
        else:
            isExist = 0
        
        data = (year, 0)
        if(isExist == 0):
            result = cursor.callproc('report', data)
            conn.commit()

    return render_template("request7.html", state = isExist)

@app.route('/request7_show', methods=['post', 'get'])
def request7_show():
    try:
        ref = request.args['ref']
    except:
        ref = None
    if (ref == 'back'):
        return redirect(url_for('/'))

    res = []
    _SQL = """
        SELECT *
	        FROM kurs.report
    """
    cursor.execute(_SQL)
    result = cursor.fetchall()
    scheme = ["genre", "income_from_cons", "year"]
    for client in result:
        res.append(dict(zip(scheme, client)))
    return render_template("request7_show.html", Data = res)

app.run()