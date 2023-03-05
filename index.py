from flask import Flask, request, render_template, json
# import traceback
# from werkzeug.wsgi import ClosingIterator
import math
import time
import threading
# from flask_executor import Executor

# class AfterResponse:
#     def __init__(self, app=None):
#         self.callbacks = []
#         if app:
#             self.init_app(app)

#     def __call__(self, callback):
#         self.callbacks.append(callback)
#         return callback

#     def init_app(self, app):
#         # install extension
#         app.after_response = self

#         # install middleware
#         app.wsgi_app = AfterResponseMiddleware(app.wsgi_app, self)

#     def flush(self):
#         for fn in self.callbacks:
#             try:
#                 fn()
#             except Exception:
#                 traceback.print_exc()

# class AfterResponseMiddleware:
#     def __init__(self, application, after_response_ext):
#         self.application = application
#         self.after_response_ext = after_response_ext

#     def __call__(self, environ, start_response):
#         iterator = self.application(environ, start_response)
#         try:
#             return ClosingIterator(iterator, [self.after_response_ext.flush])
#         except Exception:
#             traceback.print_exc()
#             return iterator

app = Flask(__name__)
# AfterResponse(app)
# executor = Executor(app)
# app.config['EXECUTOR_TYPE'] = 'thread'
client_info = {}    
@app.route('/')
def index():
    return render_template('index_calculator.html')

def logClientInformation(data,result,ip_addr):
    ts = time.time()
    if data.get('num2') is not None:
      information = [ts,data['num'],data['operator'],data['num2'], result,ip_addr]
    else:
      information = [ts,data['num'],data['operator'], result,ip_addr]
    global client_info
    if ip_addr in client_info:
      client_info[ip_addr].append(information)
    else:
      client_info[ip_addr]= [information]

@app.route('/calculate', methods=['POST'])
def calculate():
    ip_addr = request.remote_addr
    data = request.get_json()
    num2=0
    num = float(data['num'])
    if data.get('num2') is not None:
      num2 = float(data['num2']) 
    operator = data['operator']
    if client_info.get(ip_addr) is not None:
        response=[]
        if len(client_info[ip_addr]) > 4:
          response = app.response_class(
            response=json.dumps(client_info[ip_addr]),
            status=403,
            mimetype='application/json'
          ) 
          def lockUser(**kwargs):
            ip_address = kwargs.get('ip', {})
            starttime = time.time()
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))
            client_info.pop(ip_address)
            print("Ip address removed",client_info)

          thread = threading.Thread(target=lockUser, kwargs={
                    'ip': ip_addr})
          thread.start()
          return response
        
    match (operator):
      case '+':
        result = num + num2
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case '-':
        result = num - num2
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case '*':
        result = num * num2
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case '/':
        result = num / num2
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case '^':
        result = num ** num2
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case 'Sin':
        result = math.sin(math.radians(num))
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case 'Cos':
        result = math.cos(num)
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case '%':
        result = num/100
        response = app.response_class(
        response=json.dumps(result),
        status=200,
        mimetype='application/json'
        )
        logClientInformation(data,result,ip_addr)
        return response
      case default:
          return "Invalid Input"

if __name__ == '__main__':
    app.run(debug=True)
