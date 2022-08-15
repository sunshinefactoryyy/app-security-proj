from requests_oauthlib import OAuth2Session
from app.config import Auth
import string
import secrets
import urllib.request
import os
from PIL import Image
from flask import current_app, url_for
from pathlib import Path
from flask_mail import Message
from flask_login import login_user
from app import db
import logging
from datetime import datetime, timedelta
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

login_logger = logging.getLogger("login")
login_logger.setLevel('DEBUG')
loginFormatter = logging.Formatter('%(levelname)s|%(asctime)s|%(message)s')
loginFH = logging.FileHandler('login.log')
loginFH.setFormatter(loginFormatter)
loginFH.setLevel('DEBUG')
login_logger.addHandler(loginFH)

def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth

def send_reset_email(user):
    token = user.get_reset_token()
    message = Mail(
        from_email='otp.vaporlab@gmail.com',
        to_emails=user.email,
        subject='Password Reset Request',
        html_content=f"To reset your password, visit the following link:\n{url_for('reset_token', token=token, _external=True)}\nIf you did not make this request then simply ignore this email and no changes will be made."
    )
    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
    response = sg.send(message)

def generate_password():
    alphabet = string.ascii_letters + string.digits
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password

def download_picture(pic_url):
    while True:
        fn = secrets.token_hex(8)
        fp = f'{current_app.root_path}/static/src/profile_pics/{fn}.jpeg'
        if not os.path.exists(fp):
            with open(fp, 'w'): pass
            break
    urllib.request.urlretrieve(pic_url, fp)
    i = Image.open(fp)
    i.save(fp)
    return f'{fn}.jpeg'

def save_picture(form_picture, path, seperate=False):
    if seperate:
        form_pictures = form_picture
        folder_fn = secrets.token_hex(8)
        folder_path = os.path.join(current_app.root_path, Path(path), folder_fn)
        os.mkdir(folder_path)
        for form_picture in form_pictures:
            random_hex = secrets.token_hex(8)
            _, f_ext = os.path.splitext(form_picture.filename)
            picture_fn = random_hex + f_ext
            picture_path = os.path.join(folder_path, picture_fn)
            output_size = (256, 256)
            i = Image.open(form_picture)
            i.thumbnail(output_size)
            i.save(picture_path)
        return folder_fn
    else:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, Path(path), picture_fn)
        output_size = (256, 256)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn


def log_event(level, event, address, details):
    message = "address:{};event:{};{}".format(address, event, details)
    if level=='debug':
        login_logger.debug('%s', message)
    elif level=='info':
        login_logger.info('%s', message)
    elif level=='warning':
        login_logger.warning('%s', message)
    elif level=='error':
        login_logger.error('%s', message)
    elif level=='critical':
        login_logger.critical('%s', message)

def calcDataP8(past8log):
    weeks = []
    for week in past8log:
        debugCount, infoCount, warningCount, errorCount, criticalCount = 0, 0, 0, 0, 0
        for log in week:
            if log['level'].lower() == 'debug':
               debugCount += 1
            elif log['level'].lower() == 'info':
                infoCount += 1
            elif log['level'].lower() == 'warning':
                warningCount += 1
            elif log['level'].lower() == 'error':
                errorCount += 1
            elif log['level'].lower() == 'critical':
                criticalCount += 1
        week = [debugCount, infoCount, warningCount, errorCount, criticalCount]
        weeks.append(week)
    levels = []
    for i in range(5):
        tmp = []
        for week in weeks:
            tmp.append(week[i])
        levels.append(tmp)
    return levels
        
        

def calcDataMnW(monthlog, weeklog):
    debugCount, infoCount, warningCount, errorCount, criticalCount = 0, 0, 0, 0, 0
    for log in monthlog:
        if log['level'].lower() == 'debug':
            debugCount += 1
        elif log['level'].lower() == 'info':
            infoCount += 1
        elif log['level'].lower() == 'warning':
            warningCount += 1
        elif log['level'].lower() == 'error':
            errorCount += 1
        elif log['level'].lower() == 'critical':
            criticalCount += 1
    mData = [debugCount, infoCount, warningCount, errorCount, criticalCount]
    debugCount, infoCount, warningCount, errorCount, criticalCount = 0, 0, 0, 0, 0
    for log in weeklog:
        if log['level'].lower() == 'debug':
            debugCount += 1
        elif log['level'].lower() == 'info':
            infoCount += 1
        elif log['level'].lower() == 'warning':
            warningCount += 1
        elif log['level'].lower() == 'error':
            errorCount += 1
        elif log['level'].lower() == 'critical':
            criticalCount += 1
    wData = [debugCount, infoCount, warningCount, errorCount, criticalCount]
    return mData, wData


def splitLogs():
    mainlog = retMainLog()
    monthlog = []
    weeklog = []
    ascnow = datetime.now()
    for key in mainlog:
        if abs((datetime.strptime(mainlog[key]['datetime'], r"%Y-%m-%d %H:%M:%S,%f")-ascnow).days) < 30:
            monthlog.append(mainlog[key])
    for key in mainlog:
        if abs((datetime.strptime(mainlog[key]['datetime'], r"%Y-%m-%d %H:%M:%S,%f")-ascnow).days) < 7:
            weeklog.append(mainlog[key])
    past8log = []
    for i in range(7, 57, 7):
        templog = []
        for key in mainlog:
            if (i-7) <= abs((datetime.strptime(mainlog[key]['datetime'], r"%Y-%m-%d %H:%M:%S,%f")-ascnow).days) < i:
                templog.append(mainlog[key])
        past8log.append(templog)
    past8log.reverse()
    return monthlog, weeklog, past8log


def retMainLog():
    mainlog = {}
    readcount = 0
    with open('login.log') as logs:
        logs = logs.readlines()
    for line in logs:
        readcount+=1
        tmplog = {}
        temp = line.split('|')
        tmplog['level'] = temp[0]
        tmplog['datetime'] = temp[1]
        message = temp[2].split(';')
        for i in message:
            tmpmsg = i.split(':')
            try:
                tmplog[tmpmsg[0]] = tmpmsg[1]
            except IndexError:
                tmplog['unknown'] = i
        mainlog[readcount] = tmplog
    return mainlog


def retPMLogs():
    time = None
    with open('app/static/passMonitorTime.txt', 'r') as t:
        lines = t.readlines()
    try:
        time = datetime.strptime(lines[0], r"%Y-%m-%d %H:%M:%S,%f")
    except:
        pass
    main = retMainLog()
    def timekey(record):
        return datetime.strptime(record['datetime'], r"%Y-%m-%d %H:%M:%S,%f")
    if time is not None:
        filtered = []
        for key in main:
            if datetime.strptime(main[key]['datetime'], r"%Y-%m-%d %H:%M:%S,%f") > time:
                if 'event' in main[key]:
                    if main[key]['event']=='CUST_LOGIN_FAIL_WRONGPASS' or main[key]['event']=='EMP_LOGIN_FAIL_WRONGPASS':
                        filtered.append(main[key])
        before = []
        with open('passmonitor.log') as logs:
            logs = logs.readlines()
        for line in logs:
            tmplog = {}
            temp = line.split('|')
            tmplog['level'] = temp[0]
            tmplog['datetime'] = temp[1]
            message = temp[2].split(';')
            for i in message:
                tmpmsg = i.split(':')
                tmplog[tmpmsg[0]] = tmpmsg[1]
            before.append(tmplog)
        tempTime = time - timedelta(minutes=5)
        overlap = []
        for key in main:
            if tempTime < datetime.strptime(main[key]['datetime'], r"%Y-%m-%d %H:%M:%S,%f") <= time:
                if 'event' in main[key]:
                    if main[key]['event']=='CUST_LOGIN_FAIL_WRONGPASS' or main[key]['event']=='EMP_LOGIN_FAIL_WRONGPASS':
                        overlap.append(main[key])
        for i in overlap:
            if i not in before:
                before.append(i)
        before.sort(key=timekey)
        splitAcc = before + filtered
    else:
        splitAcc = []
        for key in main:
            if 'event' in main[key]:
                if main[key]['event']=='CUST_LOGIN_FAIL_WRONGPASS' or main[key]['event']=='EMP_LOGIN_FAIL_WRONGPASS':
                        splitAcc.append(main[key])
    newTime = main[len(main)]['datetime']
    with open('app/static/passMonitorTime.txt', 'w') as t:
        t.write(newTime)
    unique_emails = []
    for i in splitAcc:
        if i['email'] not in unique_emails:
            unique_emails.append(i['email'])
    uniqueAccDict = {}
    for i in unique_emails:
        uniqueAccDict[i] = []
    for i in splitAcc:
        uniqueAccDict[i['email']].append(i)
    # Analysis starts here
    for key in uniqueAccDict:
        attackList = []
        current = uniqueAccDict[key]
        tempTime = datetime.strptime(current[0]['datetime'], r"%Y-%m-%d %H:%M:%S,%f")
        tempList = []
        for record in current:
            if datetime.strptime(record['datetime'], r"%Y-%m-%d %H:%M:%S,%f") < (tempTime + timedelta(minutes=5)):
                tempList.append(record)
            elif datetime.strptime(record['datetime'], r"%Y-%m-%d %H:%M:%S,%f") > (tempTime + timedelta(minutes=5)):
                tempTime = datetime.strptime(record['datetime'], r"%Y-%m-%d %H:%M:%S,%f")
                if len(tempList) > 1:
                    attackList.append(tempList)
                tempList = []
                tempList.append(record)
        if len(tempList) > 1: # final check
                    attackList.append(tempList)
        if len(attackList) > 0:
            uniqueAccDict[key] = attackList
        else:
            uniqueAccDict[key] = []
    fullAttackList = []
    def attemptkey(attack):
        return len(attack)
    for key in uniqueAccDict:
        if len(uniqueAccDict[key]) > 0:
            for i in uniqueAccDict[key]:
                fullAttackList.append(i)
    fullAttackList.sort(key=attemptkey, reverse=True)
    returnDict = {}
    for i in range(len(fullAttackList)):
        tempDict = {}
        event = fullAttackList[i][0]['event']
        if event == 'CUST_LOGIN_FAIL_WRONGPASS':
            tempDict['account_type'] = 'CUSTOMER'
        else:
            tempDict['account_type'] = 'EMPLOYEE'
        tempDict['email'] = fullAttackList[i][0]['email']
        tempDict['attempts'] = len(fullAttackList[i])
        tempDict['data'] = fullAttackList[i]
        returnDict[i] = tempDict
    # Saving everything in passmonitor.log
    fullRecords = []
    for i in fullAttackList:
        for j in i:
            fullRecords.append(j)
    fullRecords.sort(key=timekey)
    lines = []
    for i in fullRecords:
        message = "WARNING|{}|address:{};event:{};email:{};entered_pass:{}".format(i['datetime'], i['address'], i['event'], i['email'], i['entered_pass'])
        lines.append(message)
    with open('passmonitor.log', 'w') as p:
        p.writelines(lines)
    newTime = fullRecords[-1]['datetime']
    return returnDict, fullRecords[-1]['datetime']


