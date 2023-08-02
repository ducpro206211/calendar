from datetime import datetime
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
import ephem
import math
import pandas as pd
def is_leap_year(year):
    # Kiểm tra xem một năm có phải là năm nhuận hay không
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def get_next_can_chi(year, month, day):
    dic_lucthaphoagiap = {
        1: 'Giáp Tý', 2: 'Ất Sửu', 3: 'Bính Dần', 4: 'Đinh Mão', 5: 'Mậu Thìn', 6: 'Kỷ Tỵ', 7: 'Canh Ngọ', 8: 'Tân Mùi',
        9: 'Nhâm Thân', 10: 'Quý Dậu', 11: 'Giáp Tuất', 12: 'Ất Hợi', 13: 'Bính Tý', 14: 'Đinh Sửu', 15: 'Mậu Dần',
        16: 'Kỷ Mão', 17: 'Canh Thìn', 18: 'Tân Tỵ', 19: 'Nhâm Ngọ', 20: 'Quý Mùi', 21: 'Giáp Thân', 22: 'Ất Dậu',
        23: 'Bính Tuất', 24: 'Đinh Hợi', 25: 'Mậu Tý', 26: 'Kỷ Sửu', 27: 'Canh Dần', 28: 'Tân Mão', 29: 'Nhâm Thìn',
        30: 'Quý Tỵ', 31: 'Giáp Ngọ', 32: 'Ất Mùi', 33: 'Bính Thân', 34: 'Đinh Dậu', 35: 'Mậu Tuất', 36: 'Kỷ Hợi',
        37: 'Canh Tý', 38: 'Tân Sửu', 39: 'Nhâm Dần', 40: 'Quý Mão', 41: 'Giáp Thìn', 42: 'Ất Tỵ', 43: 'Bính Ngọ',
        44: 'Đinh Mùi', 45: 'Mậu Thân', 46: 'Kỷ Dậu', 47: 'Canh Tuất', 48: 'Tân Hợi', 49: 'Nhâm Tý', 50: 'Quý Sửu',
        51: 'Giáp Dần', 52: 'Ất Mão', 53: 'Bính Thìn', 54: 'Đinh Tỵ', 55: 'Mậu Ngọ', 56: 'Kỷ Mùi', 57: 'Canh Thân',
        58: 'Tân Dậu', 59: 'Nhâm Tuất', 60: 'Quý Hợi'
    }
    # Ngày mốc để tính lịch (22/1/2023 là 'Canh Thìn')
    base_year = 2023
    base_month = 1
    base_day = 22
    if is_leap_year(year):
        days_in_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # Tính số ngày chênh lệch
    delta_days = (year - base_year) * 365 + sum(days_in_month[i] for i in range(base_month, month)) + (day - base_day)

    # Xử lý năm nhuận
    for y in range(base_year, year):
        if is_leap_year(y):
            delta_days += 1
    # Xử lý số ngày trong tháng
    # Tìm vị trí của ngày Can Chi hiện tại
    current_position = list(dic_lucthaphoagiap.keys())[list(dic_lucthaphoagiap.values()).index('Canh Thìn')]
    # Tính vị trí của ngày Can Chi tiếp theo
    next_position = (current_position + delta_days) % 60
    # Lấy ngày Can Chi tiếp theo
    next_can_chi = dic_lucthaphoagiap[next_position]
    return next_can_chi
    
#Tính ngày hoàng/ hắc đạo #input là năm, tháng, ngày cần xem
def goodday(year,month,day): 
 # convert lịch dương sang lịch âm và lấy tháng âm 
 solar = Solar(year, month,day)
 lunar = Converter.Solar2Lunar(solar)
 typemonth =lunar.month
 canchi = get_next_can_chi(year, month,day)
 daylist = ["Thanh Long","Minh Đường","Thiên Hình","Chu Tước",'Kim Quỹ','Kim Cương','Bạch Hổ','Ngọc Đường','Thiên Lao','Huyền Vũ','Tư Mệnh','Câu Trần']
 giaplist = ["Tí","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
 start_index = daylist.index("Thanh Long")  # Vị trí của "Thanh Long" trong daylist
 giapindex = [0,2,4,6,8,10]
 if typemonth > 6:
    typemonth = typemonth-6
 for i in range(1,7):
    if i == typemonth:
        startgiapindex = giapindex[i-1]
 monthlist = dict(zip(sort_list_from_index(giaplist,startgiapindex),daylist))
 hoangdaoday = tim_gia_tri(monthlist,canchi)
 return hoangdaoday
    
def tim_gia_tri(dic,chuoi): 
 for key in dic:
    if key in chuoi:
        return dic[key]
 else : return "nope"
     
def sort_list_from_index(lst, index):
    if index >= len(lst):
        return lst
    else:
        return lst[index:] + lst[:index]
        
# Hàm tính hoàng đạo theo lục minh khổng giáp #Input (year,month,day)
def find_day_khongminh(year,month,day):
    solar = Solar(year, month,day)
    lunar = Converter.Solar2Lunar(solar)
    typemonth =lunar.month
    ngay_kiem_tra = lunar.day
    canchi = get_next_can_chi(year, month,day)
    lucgiapkhongminh = ["Đại An","Lưu Niên","Tốc Hỷ","Xích Khẩu","Tiểu Cát","Không Vong"]
    khongminhindex = [1,2,3,4,5,6]
    if typemonth > 6:
     typemonth = typemonth-6
    for i in range(1,7):
     if i == typemonth:
        lucgiapkhongminhindex = lucgiapkhongminh[i-1]
    daystart =lucgiapkhongminhindex
    index = lucgiapkhongminh.index(daystart)
    index_kiem_tra = (index + ngay_kiem_tra - 1) % len(lucgiapkhongminh)
    return lucgiapkhongminh[index_kiem_tra]
    
#Tính Thập nhị trực
def TwelveBranches(year,month,day):
 tietkhi = get_solar_term(year,month,day)
 diachi = get_name_day(get_next_can_chi(year,month,day))
 terms = ["Lập xuân", "Vũ thủy", "Kinh trập","Xuân phân", "Thanh minh", "Cốc vũ", "Lập hạ", "Tiểu mãn", "Mang chủng",
             "Hạ chí", "Tiểu thử", "Đại thử", "Lập thu", "Xử thử", "Bạch lộ",
             "Thu phân", "Hàn lộ", "Sương giáng", "Lập đông", "Tiểu tuyết", "Đại tuyết",
             "Đông chí", "Tiểu hàn", "Đại hàn"]
 baseterm = ["Lập xuân", "Kinh trập","Thanh minh", "Lập hạ","Mang chủng","Tiểu thử","Lập thu","Bạch lộ","Hàn lộ","Lập đông","Đại tuyết",
             "Tiểu hàn"]
 for j in range(len(terms)):
    if terms[j] == tietkhi:
        if j %2 == 1:
            index = int((j-1)/2)
        elif j%2 ==0:
            index = int(j /2) 
 catory =    baseterm[index]    
 
 thapnhitruc = ['Trực kiến','Trực Trừ','Trực Mãn','Trực Bình','Trực Định','Trực Chấp','Trực Phá','Trực Nguy','Trực Thành','Trực Thu',
               'Trực Khai','Trực Bế']
 trucindex = [0,1,2,3,4,5,6,7,8,9,10,11]
 giaptruclist = ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"]
 start_truc = thapnhitruc.index('Trực kiến') 
 
 for i in range(len(baseterm)):
    if baseterm[i] == catory:
        starttrucindex = trucindex[i]
 trucmonthlist = dict(zip(sort_list_from_index(giaptruclist,starttrucindex),thapnhitruc))
 return tim_gia_tri(trucmonthlist,diachi)
    
def get_solar_longitude(year, month, day):
    observer = ephem.Observer()
    observer.lat = '0'  
    observer.lon = '0'  
    observer.date = f'{year}/{month}/{day}'  
    sun = ephem.Sun()
    sun.compute(observer)
    sun_longitude = sun.ra
    sun_longitude_deg = math.degrees(sun_longitude)
    return sun_longitude_deg
#Tính toạ độ mặt trời   
def get_solar_term(year,month,day):
    solar_longitude_deg = get_solar_longitude(year, month, day)
    adjusted_longitude_deg = solar_longitude_deg  # Điều chỉnh toạ độ mặt trời

    terms = ["Xuân phân", "Thanh minh", "Cốc vũ", "Lập hạ", "Tiểu mãn", "Mang chủng",
             "Hạ chí", "Tiểu thử", "Đại thử", "Lập thu", "Xử thử", "Bạch lộ",
             "Thu phân", "Hàn lộ", "Sương giáng", "Lập đông", "Tiểu tuyết", "Đại tuyết",
             "Đông chí", "Tiểu hàn", "Đại hàn", "Lập xuân", "Vũ thủy", "Kinh trập"]

    term_index = int((adjusted_longitude_deg) / 15) % 24 

    return terms[term_index]

#Tính ngày nguyệt kỵ
def NguyetKy(lunarday):
    if lunarday in [5,14,23]:
     return True
    else : 
     return False
def get_first_word(string):
    # Tách chuỗi bởi khoảng cách đầu tiên
    words = string.split(' ', 1)
    
    # Trả về phần đầu của chuỗi
    if len(words) > 0:
        return words[0]
    else:
        return ''

#Tính sao thất sát
def sevenkillstar(year,month,day):
    canyear = get_first_word(tim_nam_can_chi(year))
    if canyear in ['Mậu','Quý']:
        listday = ['Thân','Dậu','Tí','Sửu']
    elif canyear in ['Ất','Canh']:
        listday = ['Thìn','Tỵ']
    elif canyear in ['Đinh','Nhâm']:
        listday = ['Dần','Mão','Tuất','Hợi']
    elif canyear in ['Bính','Tân']:
        listday = ['Dần','Mão','Ngọ','Mùi']
    elif canyear in ['Giáp','Kỷ']:
        listday = ['Ngọ','Mùi','Thân','Dậu']
    dia_day =get_name_day(get_next_can_chi(year,month,day))
    if dia_day in listday:
        return True
    else : return False 
        
def get_name_day(string):
    # Tách chuỗi bởi khoảng cách đầu tiên
    words = string.split(' ', 1)
    
    # Trả về phần sau của chuỗi
    if len(words) > 1:
        return words[1]
    else:
        return ''
def tim_nam_can_chi(year):
    dic_lucthaphoagiap = {
        1: 'Giáp Tý', 2: 'Ất Sửu', 3: 'Bính Dần', 4: 'Đinh Mão', 5: 'Mậu Thìn', 6: 'Kỷ Tỵ', 7: 'Canh Ngọ', 8: 'Tân Mùi',
        9: 'Nhâm Thân', 10: 'Quý Dậu', 11: 'Giáp Tuất', 12: 'Ất Hợi', 13: 'Bính Tý', 14: 'Đinh Sửu', 15: 'Mậu Dần',
        16: 'Kỷ Mão', 17: 'Canh Thìn', 18: 'Tân Tỵ', 19: 'Nhâm Ngọ', 20: 'Quý Mùi', 21: 'Giáp Thân', 22: 'Ất Dậu',
        23: 'Bính Tuất', 24: 'Đinh Hợi', 25: 'Mậu Tý', 26: 'Kỷ Sửu', 27: 'Canh Dần', 28: 'Tân Mão', 29: 'Nhâm Thìn',
        30: 'Quý Tỵ', 31: 'Giáp Ngọ', 32: 'Ất Mùi', 33: 'Bính Thân', 34: 'Đinh Dậu', 35: 'Mậu Tuất', 36: 'Kỷ Hợi',
        37: 'Canh Tý', 38: 'Tân Sửu', 39: 'Nhâm Dần', 40: 'Quý Mão', 41: 'Giáp Thìn', 42: 'Ất Tỵ', 43: 'Bính Ngọ',
        44: 'Đinh Mùi', 45: 'Mậu Thân', 46: 'Kỷ Dậu', 47: 'Canh Tuất', 48: 'Tân Hợi', 49: 'Nhâm Tý', 50: 'Quý Sửu',
        51: 'Giáp Dần', 52: 'Ất Mão', 53: 'Bính Thìn', 54: 'Đinh Tỵ', 55: 'Mậu Ngọ', 56: 'Kỷ Mùi', 57: 'Canh Thân',
        58: 'Tân Dậu', 59: 'Nhâm Tuất', 60: 'Quý Hợi'
    }
    
    index_diff = year - 2023
    if index_diff > 0:
        index = (40 + index_diff) % 60
    else:
        index = (40 + index_diff) % 60
    return dic_lucthaphoagiap[index]
def tuoixung(year,month,day):
    df = pd.read_csv("/Users/oraichain/Downloads/xungtuoi.csv",header = None)
    ngaycanchi = get_next_can_chi(year, month, day)
    result = df.loc[df[1] == ngaycanchi,3].values[0]
    return result
def nhithapbattu(year,month,day):
 df = pd.read_csv("/Users/oraichain/Downloads/thapnhibattu.csv",header = None)   
 startindex = 0
 startday = datetime(2023,6,29)
 nowday = datetime(year,month,day)
 deltaday = (nowday - startday).days
 index_order = (deltaday) % len(df)
 nhithapbattu = df.iloc[startindex+index_order,1]
 return nhithapbattu
#tìm giờ hoàng đạo
def find_hour(year, month, day):
    ten_con_giap = get_name_day(get_next_can_chi(year, month, day))
    data = {
    'Giờ': ['Tý - Ngọ', 'Sửu - Mùi', 'Dần - Thân','Mão - Dậu','Thìn - Tuất', 'Tỵ - Hợi'],
    'Giờ Tý (23-1h)': ['KIM QUỸ', 'Thiên Hình', 'THANH LONG', 'TƯ MỆNH', 'Thiên Lao', 'Bạch Hổ'],
    'Giờ Sửu (1-3h)': ['KIM ĐƯỜNG', 'Chu Tước', 'MINH ĐƯỜNG', 'Câu Trần', 'Nguyên Vũ', 'NGỌC ĐƯỜNG'],
    'Giờ Dần (3h-5h)': ['Bạch Hổ', 'KIM QUỸ', 'Thiên Hình', 'THANH LONG', 'TƯ MỆNH', 'Thiên Lao'],
    'Giờ Mão (5-7h)': ['NGỌC ĐƯỜNG', 'KIM ĐƯỜNG', 'Chu Tước', 'MINH ĐƯỜNG', 'Câu Trần', 'Nguyên Vũ'],
    'Giờ Thìn (7-9h)': ['Thiên Lao', 'Bạch Hổ', 'KIM QUỸ', 'Thiên Hình', 'THANH LONG', 'TƯ MỆNH'],
    'Giờ Tỵ (9-11h)': ['Nguyên Vũ', 'NGỌC ĐƯỜNG', 'KIM ĐƯỜNG', 'Chu Tước', 'MINH ĐƯỜNG', 'Câu Trần'],
    'Giờ Ngọ (11-13h)': ['TƯ MỆNH', 'Thiên Lao', 'Bạch Hổ','KIM QUỸ','Thiên Hình',  'THANH LONG'],
    'Giờ Mùi (13-15h)': ['Câu Trần', 'Nguyễn Vũ', 'NGỌC ĐƯỜNG', 'KIM ĐƯỜNG', 'Chu Tước', 'MINH ĐƯỜNG'],
    'Giờ Thân (15-17h)': ['THANH LONG', 'TƯ MỆNH', 'Thiên Lao','Bạch Hổ', 'KIM QUỸ', 'Thiên Hình'],
    'Giờ Dậu (17-19h)': ['MINH ĐƯỜNG', 'Câu Trần', 'Nguyễn Vũ', 'NGỌC ĐƯỜNG', 'KIM ĐƯỜNG', 'Chu Tước'],
    'Giờ Tuất (19-21h)': ['Thiên Hình', 'THANH LONG', 'TƯ MỆNH', 'Thiên Lao', 'Bạch Hổ', 'KIM QUỸ'],
    'Giờ Hợi (21-23h)': ['Chu Tước', 'MINH ĐƯỜNG', 'Câu Trần', 'Nguyên Vũ', 'NGỌC ĐƯỜNG', 'KIM ĐƯỜNG']
}
    df = pd.DataFrame(data)
    row = df[df['Giờ'].str.contains(ten_con_giap)].iloc[0, 1:]
    filtered_dict = {col: value for col, value in row.items() if value.isupper()}
    return filtered_dict
# Tính hướng tốt, hạc thần, Hỷ thần là 2 sao mang lại may mắn
def Taithan(year,month,day):
    canday = get_first_word(get_next_can_chi(year,month,day))
    if canday in ['Giáp', 'Ất']:
        Taithan = ['Hướng Đông Nam']
    elif canday in ['Bính', 'Đinh']:
        Taithan = ['Hướng Đông']
    elif canday in ['Canh', 'Tân']:
        Taithan = ['Hướng  Tây Nam']
    elif canday in ['Mậu']:
        Taithan = ['Hướng Bắc']
    elif canday in ['Kỷ']:
        Taithan = ['Hướng Nam']
    elif canday in ['Nhâm']:
        Taithan = ['Hướng Tây']
    elif canday in ['Quý']:
        Taithan = ['Tây Bắc']
    return Taithan
def Hythan(year,month,day):
    canday = get_first_word(get_next_can_chi(year,month,day))
    if canday in ['Mậu','Quý']:
        Hythan = ['Hướng Đông Nam, giờ Thìn(7h-9h)']
    elif canday in ['Ất','Canh']:
        Hythan = ['Hướng Tây Nam, giờ Mùi(13h-15h)']
    elif canday in ['Đinh','Nhâm']:
        Hythan = ['Hướng Nam, giờ Ngọ(11h-13h)']
    elif canday in ['Bính','Tân']:
        Hythan = ['Hướng Tây Bắc, giờ Tuất(19-21h)']
    elif canday in ['Giáp','Kỷ']:
        Hythan = ['Hướng Đông Bắc, giờ Dần(3-5h sáng)']
    return Hythan
