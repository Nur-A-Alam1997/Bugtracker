
from flask_ngrok import run_with_ngrok
from flask import Flask,render_template,request,redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import os
from test import ReadData
from totalwork import TotalWork
from LeaveHolidayAbsent import LeaveHolidayAbsent


# import imghdr

app=Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv','.CSV']
app.config['UPLOAD_PATH'] = './'
app.secret_key = 'BAD_SECRET_KEY'


session={}


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
def home():
    return render_template("preview.html")

@app.route('/',methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Not a CSV", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        session['FILE_NAME']=filename
    return '', 204



@app.route("/data")
def data():
    if session:
        data = ReadData(session['FILE_NAME'])

        totalwork = TotalWork(data.read_data)
        total_work_in_month_values, total_work_in_month_bar \
        = [x[0] for x in totalwork.total_work_hour[0]],\
        [x[1] for x in totalwork.total_work_hour[0]]

        total_work_sum = totalwork.total_work_hour[1]


        bar_values,bar_labels = [x[0] for x in totalwork.overtime],\
        [x[1] for x in totalwork.overtime]
        

        LHA = LeaveHolidayAbsent(data.read_data)
        absent = LHA.absent
        holiday = LHA.holiday
        leave = LHA.leave
        present = LHA.present

        return render_template('bar_chart.html', title='Bitcoin Monthly Price \
        in USD', max=17000, labels=bar_labels, values=bar_values,\
        absent = absent,\
        holiday = holiday,\
        leave = leave,\
        present = present,\
        total_work_in_month_bar = total_work_in_month_bar,\
        total_work_in_month_values = total_work_in_month_values,\
        total_work_sum =total_work_sum)
    return """
        <!DOCTYPE html>
            <html>
            <body>

            <h2>Please Upload a valid CSV file first</h2>
            <img src="https://github.com/Nur-A-Alam1997/Bugtracker/blob/framework-test/ss/forbidden.gif?raw=true" alt="Trulli" width="500" height="333">

            </body>
            </html>
        """

if __name__ =="__main__":
    run_with_ngrok(app)
    app.run()
    # app.run(debug=True)