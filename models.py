from flask import session

def whoIs():
    sessions = sessionCheck()

    if 2 in sessions:
        who = 'admin'
    elif 1 in sessions:
        who = 'user'
    else:
        who = ''

    return who

def sessionCheck():
    sessionList = []
    if session.get('user_token'):
        token = str(session.get('user_token'))
        tokenCheckAdmin = Admin.query.filter_by(token=token).first()
        tokenCheckUser = User.query.filter_by(token=token).first()
        if tokenCheckAdmin:
            sessionList.append(2)
        if tokenCheckUser:
            sessionList.append(1)
    return sessionList

def Admin():
    return(print('Admin'))

def User():
        return(print('User'))
