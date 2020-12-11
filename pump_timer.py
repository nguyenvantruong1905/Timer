from flask import Flask
from flask_apscheduler import APScheduler
from datetime import datetime, date, time
from flask import request, jsonify
from flask_restful import Api, Resource
from firebase import firebase

app = Flask(__name__)
api = Api(app)
scheduler = APScheduler()
firebase = firebase.FirebaseApplication('https://vietlongpro1999-default-rtdb.firebaseio.com/', None)
def update_status_onl():
  firebase.put('/controller/', 'faucet', 0)
  firebase.put('/controller/', 'pump', 1)

  print("turn onl")
def update_status_off():
  firebase.put('/controller/', 'faucet', 1)
  firebase.put('/controller/', 'pump', 0)
  print("turn off")
class Timer(Resource):
    def post(self):
      time_request = request.json
      datetime_start = datetime.strptime(time_request['start'], "%m-%d-%Y %H:%M:%S")
      scheduler.add_job(id='example', func=update_status_onl,trigger="date", run_date=datetime_start)
      datetime_stop = datetime.strptime(time_request['stop'], "%m-%d-%Y %H:%M:%S")
      scheduler.add_job(id="example1", func=update_status_off,trigger="date", run_date=datetime_stop)
scheduler.start()
api.add_resource(Timer, '/timer')

if __name__ == "__main__":
  app.run(host="0.0.0.0")

