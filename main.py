from flask import Flask

# Flask 애플리케이션을 의미
app = Flask(__name__)

import numpy as np
import pandas as pd
from flask import request
import seaborn as sns
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')
plt.style.use('ggplot')
import weather

@app.route('/analysis')
def analysis() :
    w = weather.Dao()
    data = w.selectall()
    df = pd.DataFrame(data)
    loc = int(request.args['location'])
    temp_weather = df[df['location_id'] == loc]
    temp_weather = temp_weather[['record_date', 'max_tmp', 'min_tmp', 'avg_tmp']]
    temp_weather['record_date'] = pd.to_datetime(temp_weather['record_date'])
    temp_weather.index = temp_weather.record_date
    temp_weather = temp_weather.drop('record_date', axis=1)
    max_tmp = temp_weather['max_tmp']
    min_tmp = temp_weather['min_tmp']
    avg_tmp = temp_weather['avg_tmp']

    from statsmodels.tsa.seasonal import seasonal_decompose
    # 분해
    #result = seasonal_decompose(max_tmp['max_tmp'], model='additive', period=365)

    # ARIMA(2,1,2) 모델의 결과
    import statsmodels.api as sm
    import datetime

    # fit model
    model1 = sm.tsa.arima.ARIMA(max_tmp, order=(4, 1, 2))
    model2 = sm.tsa.arima.ARIMA(min_tmp, order=(4, 1, 2))
    model3 = sm.tsa.arima.ARIMA(avg_tmp, order=(4, 1, 2))
    model_fit1 = model1.fit()
    model_fit2 = model2.fit()
    model_fit3 = model3.fit()
    forecast1 = model_fit1.forecast(steps=11) # 예측할 개수
    forecast2 = model_fit2.forecast(steps=11)  # 예측할 개수
    forecast3 = model_fit3.forecast(steps=11)  # 예측할 개수

    date = forecast1.index
    str_date = [];
    for tmp in date :
        str = tmp.strftime("%Y-%m-%d")
        str_date.append(str)
    forecast1 = np.array(forecast1).tolist()
    forecast2 = np.array(forecast2).tolist()
    forecast3 = np.array(forecast3).tolist()

    from flask import jsonify
    return jsonify({'date': str_date, 'max_tmp' : forecast1, 'min_tmp' : forecast2, 'avg_tmp' : forecast3})

# Flask 서버 실행
app.run(host='0.0.0.0', debug=False)
