import sys
import json

# if __name__ == '__main__':
#     from nwebclient import runner
#     runner.main(custom_job)

def execute_data(data, jobexecutor):
    result = {'jobs': []}
    counter = 0 
    for job in data['jobs']:
        job_result = jobexecutor(job)
        result['jobs'].append(job_result)
        counter = counter + 1
    return result

def execute_file(jobexecutor, infile, outfile = None):
    try:
        data = json.load(open(infile))
        result = execute_data(data, jobexecutor)
        outcontent = json.dumps(result)
        print(outcontent)
        if not outfile is None:
            with open(outfile, 'w') as f:
                f.write(outcontent)
    except Exception as e:
        print("Error: " + str(e))
        print("Faild to execute JSON-File "+str(infile))

def execute_rest(jobexecutor, port = 8080):
    print("Starting webserver")
    from flask import Flask, render_template, request, response
    from flask import session, copy_current_request_context
    app = Flask(__name__)
    #@app.route('/')
    #def home():
    #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
    app.add_url_rule('/', 'home', view_func=lambda: json.dumps(execute_data(request.form.to_dict(), jobexecutor)))
    app.run(host='0.0.0.0', port=port)

        
def main(jobexecutor):
    if len(sys.argv)>2:
        infile = sys.argv[1]
        outfile = sys.argv[2]
        if infile == 'rest':
            execute_rest(jobexecutor)
        else:
            execute_file(jobexecutor, infile, outfile)
    else:
        print("Usage: infile outfile")
        print("Usage: rest api")
        