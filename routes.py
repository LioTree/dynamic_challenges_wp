import os
from flask import Blueprint,render_template,request
from CTFd.utils.decorators import authed_only
from CTFd.utils.user import get_current_user
from . import models,utils
from CTFd.plugins import bypass_csrf_protection


writeup_blueprint = Blueprint("writeup", __name__)

@writeup_blueprint.route('/writeup', methods=['POST'])
@authed_only
def uplaod_writeup():
    # try:
    file = request.files['writeup']
    cid = request.form.get("cid")
    challenge = models.query_challenge(cid).name
    username = get_current_user().name
    uid = get_current_user().id

    challenge,username,filename = map(utils.secure_filename,[challenge,username,file.filename])
    folder = os.path.sep.join(['writeups',challenge,username])
    if not os.path.isdir(folder):
        os.makedirs(folder)
    path = os.path.sep.join([folder,filename])
    file.save(path)
    models.insert_writeup(cid,uid,path)
    return 'Success'
    # except:
        # return 'Error'

@writeup_blueprint.route('/writeup',methods=['GET'])
@authed_only
def writeup_status():
    cid = request.args.get("cid")
    uid = get_current_user().id
    wp = models.query_writeup(cid,uid)
    if wp:
        return 'Uploaded'
    else:
        return 'Not uploaded'