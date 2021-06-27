from flask import Flask,render_template,request,flash
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = "mysecretkey"

@app.route('/',methods = ['GET', 'POST'])
def home():
    if request.method=="POST":
        try:
            location = request.form.get("location")
            mintemp = float(request.form.get("mintemp"))
            maxtemp = float(request.form.get("maxtemp"))
            rainfall = float(request.form.get("rainfall"))
            evaporation = float(request.form.get("evaporation"))
            sunshine = float(request.form.get("sunshine"))
            windgustdir = request.form.get("windgustdir")
            windgustspeed = float(request.form.get("windgustspeed",type=str))
            winddir9am = request.form.get("winddir9am")
            winddir3pm = request.form.get("winddir3pm")
            windspeed9am = float(request.form.get("windspeed9am"))
            windspeed3pm = float(request.form.get("windspeed3pm"))
            humidity9am = float(request.form.get("humidity9am"))
            humidity3pm = float(request.form.get("humidity3pm"))
            pressure9am = float(request.form.get("pressure9am"))
            pressure3pm = float(request.form.get("pressure3pm"))
            cloud9am = float(request.form.get("cloud9am"))
            cloud3pm = float(request.form.get("cloud3pm"))
            temp9am = float(request.form.get("temp9am"))
            temp3pm = float(request.form.get("temp3pm"))
            raintoday = request.form.get("raintoday")


            primary_array = np.array([location,mintemp,maxtemp,rainfall,evaporation,sunshine,windgustdir,windgustspeed,winddir9am,winddir3pm,windspeed9am,windspeed3pm,humidity9am,humidity3pm,pressure9am,pressure3pm,cloud9am,cloud3pm,temp9am,temp3pm,raintoday],dtype=object)
            
            Location = primary_array[0]
            WindGustDir = primary_array[6]
            WindDir9am = primary_array[8]
            WindDir3pm = primary_array[9]
            RainToday = primary_array[-1]

            model = pickle.load(open("./static/pickles/cat.pkl",'rb'))
            le_in = pickle.load(open("./static/pickles/lebl_encod_features.pkl",'rb'))
            le_out = pickle.load(open("./static/pickles/lebl_encod_rain_tom.pkl",'rb'))

            Location_NUM = le_in[0].transform([Location])
            WindGustDir_NUM = le_in[1].transform([WindGustDir])
            WindDir9am_NUM = le_in[2].transform([WindDir9am])
            WindDir3pm_NUM = le_in[3].transform([WindDir3pm])
            RainToday_NUM = le_in[4].transform([RainToday])

            secondary_array = np.array([Location_NUM, mintemp, maxtemp, rainfall, evaporation, sunshine, WindGustDir_NUM, windgustspeed, WindDir9am_NUM,WindDir3pm_NUM,windspeed9am,windspeed3pm, humidity9am, humidity3pm, pressure9am, pressure3pm, cloud9am, cloud3pm, temp9am,temp3pm, RainToday_NUM],dtype=object)

            reshaped_array = secondary_array.reshape(1,-1)
            
            prediction_NUM = model.predict(reshaped_array)

            prediction_CATE = le_out.inverse_transform(prediction_NUM)

            if prediction_CATE=="No":
                flash("No. It will be sunny day tomorrow")
            else:
                flash("Yes. It will rain tomorrow")
        except:
            flash("Something went wrong !")                 

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)