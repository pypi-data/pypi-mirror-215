import subprocess
from flask import Flask, request, jsonify, Response
import json
import base64
import sys
from . import utils

app = Flask(__name__)
port=5000
grpcurlpath='empty'
if(len(sys.argv) > 1):
    port=sys.argv[1]

@app.route('/invoke_grpc',methods = ['POST'])
def invoke_grpc():
    data = json.dumps(request.json)
    headers = request.headers
    args=request.args
    arglist=args.keys()
    server=headers['Server-Name']
    service=headers['Service-Name']
    method=headers['Method-Name']
    metadata_string=""
    if(len(arglist)>0):
        for key in arglist:
            if (key.lower().startswith("-") and (" " in key.lower().strip())):
                metadata_string += " "+key.split(" ")[0]+" "+key.split(" ")[1]+":"+args[key]
            elif (key.lower().startswith("-") and (" " not in key.lower())):
                metadata_string += " "+key
            else:
                metadata_string += " -rpc-header "+key+":"+args[key]
        grpcurl_command=grpcurlpath+'grpcurl -d \''+data+'\''+metadata_string+' '+server+' '+service+"/"+method
    else:
        grpcurl_command=grpcurlpath+'grpcurl -d \''+data+'\''+server+' '+service+"/"+method
    command_output=subprocess.getoutput(grpcurl_command)
    try:
        json.loads(command_output)
        return Response(command_output, status=200, mimetype='application/json')
    except:
        if("@value" in command_output):
            command_output = json.loads("{"+command_output.split("{")[1])  
            command_output['decrypted_error']=str(base64.b64decode(command_output['@value']))
            return command_output
        else:
            return Response("{\"error\":"+command_output+"}", status=500, mimetype='application/json')

def main():
    global grpcurlpath
    grpcurlpath=utils.identify_platform()
    print("Path:"+grpcurlpath)
    app.run(host='0.0.0.0', port=port)
