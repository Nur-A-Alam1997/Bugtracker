import os
from uuid import uuid4
from werkzeug.utils import secure_filename
import json
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory, Response, jsonify

from Task.read_data import ReadData
from Task.totalwork import TotalWork
from Task.LeaveHolidayAbsent import LeaveHolidayAbsent
from Task.remove_csv import remove_csv

# import imghdr

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.csv', '.CSV']
UPLOAD_FOLDER = './temp/'
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
app.secret_key = 'BAD_SECRET_KEY'


session = {}


@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    upload_dir = app.config['UPLOAD_PATH']
    filename = secure_filename(uploaded_file.filename)
    filename = str(uuid4().int)+(filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        print(file_ext)
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return "Not a CSV", 400
        head = {'Date',
                'Employee Id',
                'First half end',
                'First half start',
                'Second half end',
                'Second half start'}

        uploaded_file.save(os.path.join(upload_dir, filename))
        
        df = pd.read_csv(os.path.join(upload_dir, filename))
        if set(df.columns) != head:
            table = df[:5].to_html(classes='mystyle', index=False).replace(
                'border="1"', 'border="0"')
            data = {"filename": filename, "table": table}
            return Response(json.dumps(data)),409

        table = df[:5].to_html(classes='mystyle', index=False).replace(
            'border="1"', 'border="0"')
        data = {"filename": filename, "table": table}
    return Response(json.dumps(data))


@app.route("/<filename>")
def data(filename):
    upload_dir = app.config['UPLOAD_PATH']
    file_ = upload_dir+filename
    file_exists = os.path.exists(upload_dir+filename)
    if file_exists:
        data = ReadData(file_)

        totalwork = TotalWork(data.read_data)
        total_work_in_month_values, total_work_in_month_bar \
            = [x[0] for x in totalwork.total_work_hour[0]],\
            [x[1] for x in totalwork.total_work_hour[0]]

        total_work_sum = totalwork.total_work_hour[1]

        bar_values, bar_labels = [x[0] for x in totalwork.overtime],\
            [x[1] for x in totalwork.overtime]

        LHA = LeaveHolidayAbsent(data.read_data)
        absent = LHA.absent
        holiday = LHA.holiday
        leave = LHA.leave
        present = LHA.present

        return render_template('bar_chart.html', title='attendance sheet',
                               max=17000, labels=bar_labels, values=bar_values,
                               absent=absent,
                               holiday=holiday,
                               leave=leave,
                               present=present,
                               total_work_in_month_bar=total_work_in_month_bar,
                               total_work_in_month_values=total_work_in_month_values,
                               total_work_sum=total_work_sum)
    return """
        <!DOCTYPE html>
            <html>
            <body>

            <h2>Please Upload a valid CSV file first</h2>
            <img src="https://github.com/Nur-A-Alam1997/Bugtracker/blob/framework-test/ss/forbidden.gif?raw=true" alt="Trulli" width="500" height="333">

            </body>
            </html>
        """


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
