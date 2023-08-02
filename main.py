import PermanentCalendar 
from flask import (
    Flask,
    make_response,
    jsonify,
    request,
    send_file,
    send_from_directory,
    abort,
)
from flask_cors import CORS
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import pandas as pd
from datetime import datetime
app = Flask(__name__)
CORS(app)
@app.route('/Calendar', methods=['POST'])
def get_Perpetualcalendar():
    data = request.get_json()
    year = data['Year']
    month = data['Month']
    day =data['Day']
    solarday = Solar(year, month, day)
    solarday_data = {
    'year': solarday.year,
    'month': solarday.month,
    'day': solarday.day
}
    lunarday = Converter.Solar2Lunar(solarday)
    lunarday_data = {
    'year': lunarday.year,
    'month': lunarday.month,
    'day': lunarday.day
}
    daycanchi = PermanentCalendar.get_next_can_chi(year,month,day)
    tietkhi = PermanentCalendar.get_solar_term(year,month,day)
    truc =  PermanentCalendar.TwelveBranches(year,month,day)
    ZhugeLiangday = PermanentCalendar.find_day_khongminh(year,month,day)
    hoangdaoday = PermanentCalendar.goodday(year,month,day)
    canchiday = PermanentCalendar.get_next_can_chi(year, month, day)
    canchiyear = PermanentCalendar.tim_nam_can_chi(year)
    nhithapbattu = PermanentCalendar.nhithapbattu(year,month,day)
    Chinese_Zodiac_Compatibility = PermanentCalendar.tuoixung(year, month, day)
    good_hour = PermanentCalendar.find_hour(year, month, day)
    taithan = PermanentCalendar.Taithan(year, month, day)
    Hythan = PermanentCalendar.Hythan(year, month, day)
    NguyetKy = PermanentCalendar.NguyetKy(lunarday.day)
    sevenkillstar = PermanentCalendar.sevenkillstar(year, month, day)
    lysao = PermanentCalendar.sevenkillstar(year, month, day)
    tamnuong= lunarday.day
    return jsonify({'Solarday': solarday_data,'Lunarday': lunarday_data,'Sexagenary_Cycle_Day':canchiday,'Sexagenary_Cycle_Year':canchiyear,'Solarterm Day': tietkhi,'BranchesDay':truc,'ZhugeLiang day':ZhugeLiangday,'Good_day':hoangdaoday,'Chinese_Zodiac_Compatibility':Chinese_Zodiac_Compatibility,'Twenty-Eight Lunar Mansions Day':nhithapbattu,
                   'Goodhour':good_hour,'luckyDirection':{'Tai_than':taithan,'Hy_Than':Hythan},'NguyetKy':NguyetKy,'sevenkillstar':sevenkillstar,'Tam_nuong':tamnuong,'Ly_sao':lysao})
if __name__ == '__main__':
    app.run()   
