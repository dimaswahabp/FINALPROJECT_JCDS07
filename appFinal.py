from flask import Flask, render_template, url_for, request, send_from_directory
import numpy as np
import pandas as pd
import joblib
import datetime

# ['Lyft', 'Uber', 'Black', 'Black SUV', 'Lux', 'Lux Black',
#        'Lux Black XL', 'Lyft.1', 'Lyft XL', 'Shared', 'UberPool', 'UberX',
#        'UberXL', 'WAV', 'Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday',
#        'Tuesday', 'Wednesday', '0', '1', '2', '3', '4', '5', '6', '7', '8',
#        '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
#        '21', '22', '23', 'distance']

app = Flask(__name__)

desti = pd.read_csv('cab_rides.csv')
desti.dropna(inplace= True)
ds = desti['destination'].unique()
sr = desti['source'].unique()
awal = []
tujuan = []
jarak = []
for i in ds:
    for j in sr:
        if i != j:
            a = j
            b = i
            km = round((desti[(desti['destination'] == i) & (desti['source'] == j)]['distance'].mean()),2)
            awal.append(a)
            tujuan.append(b)
            jarak.append(km)
        else:
            break
dfJarak = pd.DataFrame()
dfJarak['jemput'] = awal
dfJarak['tujuan'] = tujuan
dfJarak['jarak'] = jarak
dfJarak.dropna(inplace= True)
dfJarak.sort_values('jemput', inplace=True)

@app.route("/")
def home():
    return render_template("prediksi.html")

@app.route("/stats")
def stats():
    return render_template("stats.html")

@app.route('/storage/<path:x>')
def storage(x):
    return send_from_directory("storage", x)

@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        input = request.form
        #Cab
        cab = input["cab"]
        strcab = ""
        if cab == "uber":
            cc = [0, 1]
            strcab = "Uber"
        else:
            cc = [1, 0]
            strcab = "Lyft"
        #Tanggal
        tgl = input["book"]
        hari = ['2', '6', '7', '5', '1', '3', '4']
        b = tgl.split("-")
        tahun = (b[0])
        bulan = (b[1])
        tanggal = (b[2])
        c = tahun + " " + bulan + " " + tanggal
        indekshari = datetime.datetime.strptime(c, '%Y %m %d').weekday()
        #Jam
        jam = input["jam"]
        if jam[:2] == "00":
            jj = list(np.ones(1)) + list(np.zeros(23))
        if jam[:2] == "01":
            jj = list(np.zeros(1)) + list(np.ones(1)) + list(np.zeros(22))
        if jam[:2] == "02":
            jj = list(np.zeros(2)) + list(np.ones(1)) + list(np.zeros(21))
        if jam[:2] == "03":
            jj = list(np.zeros(3)) + list(np.ones(1)) + list(np.zeros(20))
        if jam[:2] == "04":
            jj = list(np.zeros(4)) + list(np.ones(1)) + list(np.zeros(19))
        if jam[:2] == "05":
            jj = list(np.zeros(5)) + list(np.ones(1)) + list(np.zeros(18))
        if jam[:2] == "06":
            jj = list(np.zeros(6)) + list(np.ones(1)) + list(np.zeros(17))
        if jam[:2] == "07":
            jj = list(np.zeros(7)) + list(np.ones(1)) + list(np.zeros(16))
        if jam[:2] == "08":
            jj = list(np.zeros(8)) + list(np.ones(1)) + list(np.zeros(15))
        if jam[:2] == "09":
            jj = list(np.zeros(9)) + list(np.ones(1)) + list(np.zeros(14))
        if jam[:2] == "10":
            jj = list(np.zeros(10)) + list(np.ones(1)) + list(np.zeros(13))
        if jam[:2] == "11":
            jj = list(np.zeros(11)) + list(np.ones(1)) + list(np.zeros(12))
        if jam[:2] == "12":
            jj = list(np.zeros(12)) + list(np.ones(1)) + list(np.zeros(11))
        if jam[:2] == "13":
            jj = list(np.zeros(13)) + list(np.ones(1)) + list(np.zeros(10))
        if jam[:2] == "14":
            jj = list(np.zeros(14)) + list(np.ones(1)) + list(np.zeros(9))
        if jam[:2] == "15":
            jj = list(np.zeros(15)) + list(np.ones(1)) + list(np.zeros(8))
        if jam[:2] == "16":
            jj = list(np.zeros(16)) + list(np.ones(1)) + list(np.zeros(7))
        if jam[:2] == "17":
            jj = list(np.zeros(17)) + list(np.ones(1)) + list(np.zeros(6))
        if jam[:2] == "18":
            jj = list(np.zeros(18)) + list(np.ones(1)) + list(np.zeros(5))
        if jam[:2] == "19":
            jj = list(np.zeros(19)) + list(np.ones(1)) + list(np.zeros(4))
        if jam[:2] == "20":
            jj = list(np.zeros(20)) + list(np.ones(1)) + list(np.zeros(3))
        if jam[:2] == "21":
            jj = list(np.zeros(21)) + list(np.ones(1)) + list(np.zeros(2))
        if jam[:2] == "22":
            jj = list(np.zeros(22)) + list(np.ones(1)) + list(np.zeros(1))
        if jam[:2] == "23":
            jj = list(np.zeros(23)) + list(np.ones(1))
        #Days
        day = hari[indekshari]
        strday = ""
        if day == "1":
            dd = [1, 0, 0, 0, 0, 0, 0]
            strday = "Friday"
        elif day == "2":
            dd = [0, 1, 0, 0, 0, 0, 0]
            strday = "Monday"
        elif day == "3":
            dd = [0, 0, 1, 0, 0, 0, 0]
            strday = "Saturday"
        elif day == "4":
            dd = [0, 0, 0, 1, 0, 0, 0]
            strday = "Sunday"
        elif day == "5":
            dd = [0, 0, 0, 0, 1, 0, 0]
            strday = "Thursday"
        elif day == "6":
            dd = [0, 0, 0, 0, 0, 1, 0]
            strday = "Tuesday"
        elif day == "7":
            dd = [0, 0, 0, 0, 0, 0, 1]
            strday = "Wednesday"
        #Jemput
        pick = input["awal"]
        strpick = ""
        if pick == "bb":
            strpick = "Back Bay"
        elif pick == "bh":
            strpick = "Beacon Hill"
        elif pick == "bu":
            strpick = "Boston University"
        elif pick == "fw":
            strpick = "Fenway"
        elif pick == "fd":
            strpick = "Financial District"
        elif pick == "hs":
            strpick = "Haymarket Square"
        elif pick == "ne":
            strpick = "North End"
        elif pick == "ns":
            strpick = "North Station"
        elif pick == "ss":
            strpick = "South Station"
        elif pick == "td":
            strpick = "Theatre District"
        elif pick == "we":
            strpick = "West End"
        #Antar
        des = input["tujuan"]
        strdes = ""
        if des == "bb":
            strdes = "Back Bay"
        elif des == "bh":
            strdes = "Beacon Hill"
        elif des == "bu":
            strdes = "Boston University"
        elif des == "fw":
            strdes = "Fenway"
        elif des == "fd":
            strdes = "Financial District"
        elif des == "hs":
            strdes = "Haymarket Square"
        elif des == "ne":
            strdes = "North End"
        elif des == "ns":
            strdes = "North Station"
        elif des == "nu":
            strdes = "Northeastern University"
        elif des == "ss":
            strdes = "South Station"
        elif des == "td":
            strdes = "Theatre District"
        elif des == "we":
            strdes = "West End"
        #Jarak Antar Jemput
        kira = float(dfJarak[(dfJarak['jemput'] == strpick) & (dfJarak['tujuan'] == strdes)]['jarak'])
        #Cab Name
        nem = input["name"]
        strnem = ""
        if nem == "black":
            nn = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            strnem = "Black"
        elif nem == "blacksuv":
            nn = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            strnem = "Black SUV"
        elif nem == "lux":
            nn = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            strnem = "Lux"
        elif nem == "luxblack":
            nn = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
            strnem = "LuxBlack"
        elif nem == "luxblackxl":
            nn = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
            strnem = "LuxBlack XL"
        elif nem == "lyft":
            nn = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            strnem = "Lyft"
        elif nem == "lyftxl":
            nn = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
            strnem = "Lyft XL"
        elif nem == "shared":
            nn = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
            strnem = "Shared"
        elif nem == "uberpool":
            nn = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
            strnem = "UberPool"
        elif nem == "uberx":
            nn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
            strnem = "UberX"
        elif nem == "uberxl":
            nn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
            strnem = "UberXL"
        elif nem == "wav":
            nn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
            strnem = "WAV"
        #Distance
        # dis = float(input["distance"])
        #Result
        datainput = cc + nn + dd + jj + [kira]
        print(datainput)
        pred = round((model.predict([datainput])[0]),2)
        return render_template(
            "hasil.html", day= strday, cab= strcab, 
            nem= strnem, result= pred, jemput= strpick, antar= strdes, 
            jarak= kira, date= tgl, jam= jam
        )


if __name__ == "__main__":
    model = joblib.load("modelPrediksi")
    app.run(debug=True, port=8000)