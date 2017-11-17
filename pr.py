from flask import Flask,render_template,request
import psycopg2
import pandas
import datetime
from bokeh.plotting import figure,output_file,show
from bokeh.embed import components
from bokeh.resources import CDN

#DATABASE FOR POULTRY FARMING##################################################################################################
def create_table_farming():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS farming(general_date date ,screening text,cartel int ,dates text,looses int,actual int,paste int,weight int,poultry int,patch real,total_looses int,poultry_looses int,total_paste int)")
    conn.commit()
    conn.close()


def insert_farming(general_date,screening,cartel,dates,looses,actual,paste,weight,poultry,patch):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("INSERT INTO farming VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(general_date,screening,cartel,dates,looses,actual,paste,weight,poultry,patch))
    conn.commit()
    conn.close()

def sum_column_looses_farming(cartel,screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE farming  set total_looses = (SELECT SUM(looses)  FROM farming WHERE cartel = %s AND screening = %s) WHERE dates = %s",(cartel,screening,dates))
    conn.commit()
    conn.close()

def balance_poultry_looses_farming(cartel,screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE farming  set poultry_looses = (SELECT SUM(poultry-looses)  FROM farming WHERE cartel = %s And screening = %s) WHERE dates = %s",(cartel,screening,dates))
    conn.commit()
    conn.close()

def total_paste(cartel,screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE farming SET total_paste = (SELECT SUM(paste) FROM farming WHERE cartel = %s AND screening = %s) WHERE dates = %s",(cartel,screening,dates))
    conn.commit()
    conn.close()


def search_farming(screening,cartel):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM farming WHERE screening = %s AND cartel = %s",(screening,cartel))
    rows = cur.fetchall()
    conn.close()
    return rows


def view_farming():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT * FROM farming")
    rows = cur.fetchall()
    conn.close()
    return rows

#Table FOR FINANCE#######################################################################################################################

def create_table_spendings():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS spendings(screening text,dates text,gas real,straw real,working real,logistics real,cleaning real,disinfectant real,injection real,medicine real,alimony real,oil real,waste real\
    ,gas_final real,paste_final real,poultry_final real,straw_final real,working_final real,piastika_final real,electricity_final real,logistics_final real,cleaning_final real,disinfectant_final real,injection_final real,medicine_final real,alimony_final real,oil_final real,total_spendings_final real\
    ,value_incomes real,waste_final real,fpa real,aggregate real,total_incomes real,fpa_debit real,final_incomes real,taxes real,final_incomes_taxes real)")
    conn.commit()
    conn.close()

def insert_spendings(screening,dates,gas,straw,working,logistics,cleaning,disinfectant,injection,medicine,alimony,oil,waste):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("INSERT INTO spendings VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(screening,dates,gas,straw,working,logistics,cleaning,disinfectant,injection,medicine,alimony,oil,waste))
    conn.commit()
    conn.close()

def gas_results(screening,dates):
    conn = psycopg2.connect("dbname='alekarios' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET gas_final = ((SELECT SUM(gas) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(gas) FROM spendings WHERE screening = %s)*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def paste_results(screening,dates):
    conn = psycopg2.connect("dbname='alekarios' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET paste_final = ((SELECT SUM(paste) FROM farming WHERE screening = %s)*0.405+((SELECT SUM(paste) FROM farming WHERE screening = %s)*0.405)*0.13)\
     WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def poultry_results(screening,dates):
    conn = psycopg2.connect("dbname='alekarios' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET poultry_final = ((SELECT SUM(poultry) FROM farming WHERE screening = %s)*0.48+((SELECT SUM(poultry) FROM farming WHERE screening = %s)*0.48)*0.24)\
     WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def straw_results(screening,dates):
    conn = psycopg2.connect("dbname='alekarios' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET straw_final = ((SELECT SUM(straw) FROM spendings WHERE screening = %s)+(SELECT SUM(straw) FROM spendings WHERE screening = %s)*0.24)\
     WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def working_results(screening,dates):
    conn = psycopg2.connect("dbname='alekarios' user='postgres' password='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET working_final = (SELECT SUM(working) FROM spendings WHERE screening = %s) WHERE dates = %s",(screening,dates))
    conn.commit()
    conn.close()

def piastka_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET piastika_final = ((SELECT SUM(poultry-looses) FROM farming WHERE screening = %s)*0.032\
    +(SELECT SUM(poultry-looses) FROM farming WHERE screening = %s)*0.03228*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def electricity_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET electricity_final = ((SELECT SUM(poultry) FROM farming WHERE screening = %s)*0.03) WHERE dates = %s",(screening,dates))
    conn.commit()
    conn.close()

def logistics_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET logistics_final = (SELECT SUM(logistics) FROM spendings WHERE screening = %s) WHERE dates = %s",(screening,dates))
    conn.commit()
    conn.close()

def cleaning_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET cleaning_final = ((SELECT SUM(cleaning) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(cleaning) FROM spendings WHERE screening = %s)*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def disinfectant_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET disinfectant_final = ((SELECT SUM(disinfectant) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(disinfectant) FROM spendings WHERE screening = %s)*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def injection_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET injection_final = ((SELECT SUM(injection) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(injection) FROM spendings WHERE screening = %s)*0.13) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def medicine_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET medicine_final = ((SELECT SUM(medicine) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(medicine) FROM spendings WHERE screening = %s)*0.13) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def alimony_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET alimony_final = ((SELECT SUM(alimony) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(alimony) FROM spendings WHERE screening = %s)*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def oil_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET oil_final = ((SELECT SUM(oil) FROM spendings WHERE screening = %s)\
    +(SELECT SUM(oil) FROM spendings WHERE screening = %s)*0.24) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def total_spendings(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET total_spendings_final = (SELECT SUM(gas_final+paste_final+poultry_final+straw_final+working_final+piastika_final+electricity_final+logistics_final+cleaning_final+disinfectant_final+injection_final+medicine_final+alimony_final+oil_final)\
     FROM spendings WHERE dates = %s AND screening = %s) WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def select_spendings():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT MAX(dates),MAX(gas_final),MAX(paste_final),MAX(poultry_final),MAX(straw_final),MAX(working_final),MAX(piastika_final),MAX(electricity_final),MAX(logistics_final),MAX(cleaning_final),MAX(disinfectant_final),MAX(injection_final),MAX(medicine_final),MAX(alimony_final),MAX(oil_final),MAX(total_spendings_final) FROM spendings")
    rows = cur.fetchall()
    conn.close()
    return rows


def view_insert_spendings():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT screening,dates,gas,straw,working,logistics,cleaning,disinfectant,injection,medicine,alimony,oil,waste FROM spendings")
    rows = cur.fetchall()
    conn.close()
    return rows

def view_insert_spendings_screen(screening):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT screening,dates,gas,straw,working,logistics,cleaning,disinfectant,injection,medicine,alimony,oil,waste FROM spendings\
     WHERE screening = %s",(screening))
    rows = cur.fetchall()
    conn.close()
    return rows

def value_incomes(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET value_incomes = ((SELECT SUM(weight) FROM farming WHERE screening = %s)*1.155) WHERE dates = %s",(screening,dates))
    conn.commit()
    conn.close()

def waste_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET waste_final = (((SELECT SUM(weight) FROM farming WHERE screening = %s)*1.155)\
    -(SELECT SUM(waste) FROM spendings WHERE screening = %s)) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def fpa_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET fpa = ((((SELECT SUM(weight) FROM farming WHERE screening = %s)*1.155)\
    -(SELECT SUM(waste) FROM spendings WHERE screening = %s))*0.13) WHERE dates = %s",(screening,screening,dates))
    conn.commit()
    conn.close()

def aggregate_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET aggregate = (SELECT SUM(waste_final+fpa) FROM spendings WHERE dates = %s AND screening = %s)\
     WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def total_incomes_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET total_incomes = (SELECT SUM(aggregate-total_spendings_final) FROM spendings WHERE dates = %s AND screening = %s)\
     WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def fpa_debit_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET fpa_debit = ((SELECT SUM(fpa) FROM spendings WHERE dates = %s AND screening = %s)-((SELECT SUM(gas) FROM spendings WHERE screening = %s)*0.24)\
    -(((SELECT SUM(poultry) FROM farming WHERE screening = %s)*0.48)*0.24)-(((SELECT SUM(paste) FROM farming WHERE screening = %s)*0.405)*0.13)-((SELECT SUM(straw) FROM spendings WHERE screening = %s)*0.24)\
    -((SELECT SUM(poultry-looses) FROM farming WHERE screening = %s)*0.03228*0.24)-((SELECT SUM(cleaning) FROM spendings WHERE screening =%s)*0.24)-((SELECT SUM(disinfectant) FROM spendings WHERE screening = %s)*0.24)\
    -((SELECT SUM(injection) FROM spendings WHERE screening = %s)*0.13)-((SELECT SUM(medicine) FROM spendings WHERE screening = %s)*0.13)-((SELECT SUM(alimony) FROM spendings WHERE screening = %s)*0.24)\
    -((SELECT SUM(oil) FROM spendings WHERE screening = %s)*0.24)) WHERE dates = %s",(dates,screening,screening,screening,screening,screening,screening,screening,screening,screening,screening,screening,screening,dates))
    conn.commit()
    conn.close()

def final_incomes_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET final_incomes = (SELECT SUM(-(total_incomes-fpa_debit)) FROM spendings WHERE dates = %s AND screening = %s)\
     WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def taxes_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET taxes = ((SELECT SUM(final_incomes) FROM spendings WHERE dates = %s AND screening = %s)*0.27)\
     WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def final_incomes_taxes_results(screening,dates):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("UPDATE spendings SET final_incomes_taxes = (SELECT SUM(final_incomes-taxes) FROM spendings WHERE dates = %s AND screening = %s)\
     WHERE dates = %s",(dates,screening,dates))
    conn.commit()
    conn.close()

def select_incomes():
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT dates,value_incomes,waste_final,fpa,aggregate,fpa_debit,taxes,total_incomes,final_incomes,final_incomes_taxes FROM spendings")
    rows = cur.fetchall()
    conn.close()
    return rows

def select_incomes_screen(screening):
    conn = psycopg2.connect("dbname ='alekarios' user ='postgres' password ='postgres123' host='localhost' port='5432'")
    cur = conn.cursor()
    cur.execute("SELECT dates,value_incomes,waste_final,fpa,aggregate,fpa_debit,taxes,total_incomes,final_incomes,final_incomes_taxes\
     FROM spendings WHERE screening = %s",(screening,))
    rows = cur.fetchall()
    conn.close()
    return rows

def charts():
    data = pandas.read_csv("574-A.csv",parse_dates = ['index'])
    p = figure(plot_width = 500, plot_height = 250,title = " stats",x_axis_type = "datetime",responsive = True)
    p.multi_line((data['index'],data['index'],data['index']),(data["Actual MZB"],data["Daily theoritical MZB"],data["Theoritical MZB"]),color = ["orange","blue","red"],alpha = [0.5,0.5,0.5])
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "Living weight"
    script1 , div1, = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    #output_file("templates/financies.html")
    #show(p)







#Flask code######################################################################################################################
app = Flask(__name__)
###########log in pafe#######################################

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/",methods=['GET','POST'])
def success():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['pass']
        if user == 'alekarios' and password == '12345':
            return render_template("success.html")
        else:
             return render_template("success1.html")

###########insert farming values html page############################################
l = []

@app.route("/success",methods=['GET','POST'])
def success1():
    global cartel
    d = {}
    if request.method == 'POST':
        screen = request.form['screen']
        looses = request.form['looses']
        real_MZB = request.form['real']
        poultry_number = request.form['poultry']
        patch = request.form['patch']
        cartel = request.form['cartel']
        paste = request.form['paste']
        weight = request.form['weight']
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+"-"+cartel
        time1 = datetime.datetime.now().strftime("%Y-%m-%d")


        if looses =="":
            looses = 0
        if real_MZB =="":
            real_MZB = 0
        if poultry_number=="":
            poultry_number = 0
        if patch =="":
            patch = 0
        if paste =="":
            paste=0
        if weight == "":
            weight=0


        create_table_farming()
        insert_farming(time1,screen,cartel,time,looses,real_MZB,paste,weight,poultry_number,patch)
        sum_column_looses_farming(cartel,screen,time)
        balance_poultry_looses_farming(cartel,screen,time)
        total_paste(cartel,screen,time)

        data_theoritical_MZB = [42,56,72,89,109,132,157,185,217,251,289,330,375,422,473,527,585,645,709,775,844,916,990,1066,1145,1226,1309,1393,1479,1567,1656,1746,1836,1928,2020,2113,2207,2300,2394,2488,2581,2674,2766,2859,2952,3044,3135,3226,3316,3405]
        df_theoritical_MZB = pandas.DataFrame(data_theoritical_MZB,columns = ["Theoritical MZB"])

        data_daily_MZB = [0,14,16,17,20,23,25,28,32,34,38,41,45,47,51,54,58,60,64,66,69,72,74,76,79,81,83,84,86,88,89,90,90,92,92,93,94,93,94,94,93,93,92,93,93,92,91,91,90,89]
        df_daily_MZB = pandas.DataFrame(data_daily_MZB,columns = ["Daily theoritical MZB"])

        df = pandas.DataFrame(search_farming(screen,cartel),columns = ['index','Screening','Cartel','Date','Looses','Actual MZB','Paste','Living weight','Poultry number','Acreage','Total looses','Poultry looses','Total paste'])
        df_all = pandas.DataFrame(view_farming(),columns = ['index','Screening','Cartel','Date','Looses','Actual MZB','Paste','Living weight','Poultry number','Acreage','Total looses','Poultry looses','Total paste'])
        ((df.join(df_theoritical_MZB)).join(df_daily_MZB)).to_csv("%s-%s.csv"%(cartel,screen),encoding='utf-8')
        (df_all.to_csv("all.csv",encoding='utf-8'))

        charts()


    return render_template("success.html")

#########insert spendings html page###################################################

@app.route("/spendings",methods=['GET', 'POST'])
def spendings():
    if request.method == 'POST':
        screen = request.form['screen']
        gas = request.form['gas']
        straw = request.form['straw']
        working = request.form['working']
        logistics = request.form['logistics']
        cleaning = request.form['cleaning']
        disinfectant = request.form['disinfectant']
        injection = request.form['injection']
        medicine = request.form['medicine']
        alimony = request.form['alimony']
        oil = request.form['oil']
        waste = request.form['waste']

        if gas =="":
            gas = 0
        if straw =="":
            straw =0
        if working =="":
            working = 0
        if logistics =="":
            logistics = 0
        if cleaning =="":
            cleaning = 0
        if disinfectant =="":
            disinfectant = 0
        if injection =="":
            injection = 0
        if medicine =="":
            medicine = 0
        if alimony =="":
            alimony = 0
        if oil =="":
            oil = 0
        if waste=="":
            waste = 0

        create_table_spendings()
        time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        insert_spendings(screen,time,gas,straw,working,logistics,cleaning,disinfectant,injection,medicine,alimony,oil,waste)
        gas_results(screen,time)
        paste_results(screen,time)
        poultry_results(screen,time)
        straw_results(screen,time)
        working_results(screen,time)
        piastka_results(screen,time)
        logistics_results(screen,time)
        electricity_results(screen,time)
        cleaning_results(screen,time)
        disinfectant_results(screen,time)
        injection_results(screen,time)
        medicine_results(screen,time)
        alimony_results(screen,time)
        oil_results(screen,time)
        total_spendings(screen,time)
        value_incomes(screen,time)
        waste_results(screen,time)
        fpa_results(screen,time)
        aggregate_results(screen,time)
        total_incomes_results(screen,time)
        fpa_debit_results(screen,time)
        final_incomes_results(screen,time)
        taxes_results(screen,time)
        final_incomes_taxes_results(screen,time)
        view_insert_spendings_screen(screen)

        df = pandas.DataFrame(view_insert_spendings(),columns = ['Screening','Date','Gas','Straw','Working','Losgistics','Cleaning','Disinfectant','Injection','Medicine','Alimony','Oil','Waste'])
        df.to_csv("output_spendings.csv",encoding = 'utf-8')

        df_screen = pandas.DataFrame(view_insert_spendings_screen(screen),columns = ['Screening','Date','Gas','Straw','Working','Losgistics','Cleaning','Disinfectant','Injection','Medicine','Alimony','Oil','Waste'])
        df_screen.to_csv("output_spendings-%s.csv"%(screen),encoding = 'utf-8')

        df_total_spendings_all = pandas.DataFrame(select_spendings(),columns = ['Date','Gas','Paste','Novice','Straw','Working','Piastika','Electricity','Logistics','Cleaning','Disinfectant','Injection','Medicine','Alimony','Oil','Total spendings'])
        df_total_spendings_all.to_csv("total_spendings.csv",encoding = 'utf-8')

        df_total_spendings = pandas.DataFrame(select_spendings(),columns = ['Date','Gas','Paste','Novice','Straw','Working','Piastika','Electricity','Logistics','Cleaning','Disinfectant','Injection','Medicine','Alimony','Oil','Total spendings'])
        df_total_spendings.to_csv("total_spendings-%s.csv"%(screen),encoding = 'utf-8')

        df_spendings_all = pandas.DataFrame(select_incomes(),columns = ['Date','Value','Waste','V.A.T','SUM','Debit V.A.T','Inland Revenue','Total','Final incomes','Final incomes including taxes'])
        df_spendings_all.to_csv("incomes.csv",encoding = 'utf-8')

        df_spendings = pandas.DataFrame(select_incomes_screen(screen),columns = ['Date','Value','Waste','V.A.T','SUM','Debit V.A.T','Inland Revenue','Total','Final Incomes','Final incomes including taxes'])
        df_spendings.to_csv("incomes-%s.csv"%(screen),encoding = 'utf-8')




    return render_template("spendings.html")


@app.route("/farming_table",methods = ['GET','POST'])
def farming_table():
    output = pandas.read_csv("all.csv")
    if request.method == 'POST':
        y = request.form['select_cartel']
        z = request.form['select_screen']
        output = pandas.read_csv("%s-%s.csv"%(y,z))
    return render_template("farming_table.html",text = output.to_html())

@app.route("/spendings_table",methods = ['GET','POST'])
def spendings_table():
    output = pandas.read_csv("output_spendings.csv")
    if request.method == 'POST':
        screen = request.form['screen']
        output = pandas.read_csv("output_spendings-%s.csv"%(screen))
    return render_template("spendings_table.html",text = output.to_html())

@app.route("/total_spendings",methods = ['GET','POST'])
def total_spendings_table():
    output = pandas.read_csv("total_spendings.csv")
    if request.method == 'POST':
        screen = request.form['screen']
        output = pandas.read_csv("total_spendings-%s.csv"%(screen))
    return render_template("total_spendings.html",text = output.to_html())

@app.route("/incomes",methods = ['GET','POST'])
def total_incomes_table():
    output = pandas.read_csv("incomes.csv")
    if request.method == 'POST':
        screen = request.form['screen']
        output = pandas.read_csv("incomes-%s.csv"%(screen))
    return render_template("incomes.html",text = output.to_html())

@app.route("/charts",methods = ['GET','POST'])
def plot():
    data = pandas.read_csv("574-A.csv",parse_dates = ['index'])
    if request.method == 'POST':
        screen = request.form['screen']
        cartel = request.form['cartel']
        data = pandas.read_csv("%s-%s.csv"%(cartel,screen),parse_dates = ['index'])
    p = figure(plot_width = 100, plot_height = 100,title = " stats",x_axis_type = "datetime",responsive = True)
    p.multi_line((data['index'],data['index'],data['index']),(data["Theoritical MZB"],data["Actual MZB"],data["Daily theoritical MZB"]),color = ["orange","blue","red"],alpha = [0.5,0.5,0.5])
    p.xaxis.axis_label = "Date"
    p.yaxis.axis_label = "weight"
    script1 , div1, = components(p)
    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("charts.html",script1 = script1,div1 = div1,cdn_css = cdn_css,cdn_js = cdn_js)

########

########

if __name__ == '__main__':
    app.debug=True
    app.run(host ='0.0.0.0',port = 5000)
