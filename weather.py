import pymysql

class Dao :
    # mysql 연결함수
    def connect(self):
        self.con = pymysql.connect(host='localhost', port=3306, db='weather',
                                   user='hk', passwd='3241', charset='utf8')
        self.cursor = self.con.cursor()

    # mysql 접속 해제 함수
    def close(self):
        self.con.close()

    # flaskitem 테이블의 모든 데이터 가져오기
    def selectall(self):
        self.connect()
        self.cursor.execute('select * from record')
        data = self.cursor.fetchall()
        li = []
        for imsi in data :
            dic = {}
            dic['record_id'] = imsi[0]
            dic['location_id'] = imsi[1]
            dic['record_date'] = imsi[2]
            dic['avg_tmp'] = imsi[3]
            dic['min_tmp'] = imsi[4]
            dic['max_tmp'] = imsi[5]
            dic['rain_hours'] = imsi[6]
            dic['day_rain'] = imsi[7]
            dic['max_insta_windspeed'] = imsi[8]
            dic['max_windspeed'] = imsi[9]
            dic['avg_windspeed'] = imsi[10]
            dic['avg_humid'] = imsi[11]
            dic['day_snow'] = imsi[12]
            dic['accumul_snow'] = imsi[13]

            li.append(dic)
        self.close()
        return li
