import mysql.connector as sql
from flask import Flask, render_template,request,redirect
from flask_socketio import SocketIO, emit
import os

a=''
b=''
sql1="SELECT * FROM messages"

username=''
name1=''
sql5="SELECT * FROM user_information"
messages=''
sql23="INSERT INTO messages(username,username01,msg) VALUES('{}','{}','{}')"
online=[]




b=''
l=[]
li=['a']

length_users=0
    
app = Flask(__name__)
userlength01=''

app.config[ 'SECRET_KEY' ] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )
username01=[]

    
    
@app.route( '/' )
def hello():
    return render_template('./dev.html')
    


def messageRecived():
  print( 'message was received!!!' )


def msg():
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    

    cursor.execute(sql1)
    mesg1=[]
    message1=cursor1.fetchall()
    
    for a11 in message1:
        mesg1.append(' '+a11[3])
    
    return str(mesg1)
    conn.close()


    
    
    
        
  
        
    
@socketio.on('users')
def user(username):
    conn1=sql.connect(host='localhost',user="root",passwd='',database='friends')
    cursor1=conn1.cursor()
    
    
    user01=username['online']
    sql8="SELECT * FROM {}"
    users=[]
    cursor1.execute(sql8.format(user01))
    user=cursor1.fetchall()
    
       
    userlength=cursor1.rowcount
    
    for users01 in user:
        
        users.append(users01[1])
    usernames={'users':users}
   
    socketio.emit('display',usernames)
    conn1.close()




   

    

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    print( 'recived my event: ' + str( json ) )
    
    try:
        b=json['user_name']
        e=json['user_selected']
        a=json['message']
        if json['message']!='':
            cursor.execute(sql23.format(b,e,a))
            socketio.emit( 'my response',json, callback=messageRecived )
            conn.commit()
    except Exception as e:
        pass
    conn.close()
@socketio.on( 'userselected' )
def userselected(json):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    
    try:
        cursor.execute(sql1)
        mesg=[]
        user012=[]
        user0123=[]
        message=cursor.fetchall()
        for a1 in message:
            if (json['user_name']==a1[1]and  json['user_selected']==a1[2])or (json['user_selected']==a1[1]and  json['user_name']==a1[2]):
                user012.append(a1[1])
                user0123.append(a1[2])
                mesg.append(a1[3])
        length_users=len(mesg)
        messages=str(mesg)
        json1={'user_selected':json['user_selected'],'lenght':length_users,'messages':messages,'user_name':json['user_name'],'username':str(user012),'username01':str(user0123)}
        conn.close()
        socketio.emit('incoming',json1)
    except Exception as e:
        pass
@socketio.on( 'useronline' )
def useronline(json10):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    
    cursor=conn.cursor()
    conn1=sql.connect(host='localhost',user="root",passwd='',database='friends')
    cursor1=conn1.cursor()
    

    p=json10['online']
    notification=[]
    notifications=[]
    
    users=[]
    friend=[]
    cursor.execute(sql5)
    user=cursor.fetchall()
    userlength=cursor.rowcount
    sql9="SELECT * FROM {}"
    sql10="SELECT * FROM notifications"
    cursor1.execute(sql9.format(p))
    friends=cursor1.fetchall()
    cursor.execute(sql10)
    noti=cursor.fetchall()
    for a in range(0,len(noti)):
        notifications.append(noti[a][1])
        notification.append(noti[a][2])
    
    
   
   
    for j in range(0,len(friends)):
        friend.append(friends[j][1])
    for i in range(0,userlength):
        if user[i][1] not in friend:
            if(p not in notification) and (user[i][1] not in notifications) or  (p not in notifications) and (user[i][1] not in notification):
                users.append(user[i][1])
    conn.close()
    conn1.close()
       
        
            
                
                
        
    json10={'users':users}
    socketio.emit('friendadd',json10)

@socketio.on('friendrequest')
def dev(dev):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    
    sql4="INSERT INTO notifications(username,username01) VALUES('{}','{}')"
    a=dev['username']
    b=dev['friendreq']
    
    cursor.execute(sql4.format(a,b))
    conn.commit()
    conn.close()
    
@socketio.on('showfriend')
def showfriend(friends01):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    sql5='SELECT * FROM notifications'
    cursor.execute(sql5)
    friends=cursor.fetchall()
    
    l=[]
    
    for a in friends:
        
        if friends01['useronline']==a[2]:
            l.append(str(a[1]))
    friend={'list':l}
            
    socketio.emit('showlist',friend)
    conn.close()
@socketio.on('accepted')
def accepted(name):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    
    conn1=sql.connect(host='localhost',user="root",passwd='',database='friends')
    cursor1=conn1.cursor()
    username=name['username']
    username01=name['username01']
    
    
    sql6="INSERT INTO {}(username) VALUES('{}')"
    sql7="INSERT INTO {}(username) VALUES('{}')"
    cursor1.execute(sql6.format(username,username01))
    cursor1.execute(sql6.format(username01,username))
    conn1.commit()
    sql8="DELETE FROM notifications WHERE username01='{}'"
    cursor.execute(sql8.format(username))
    conn.commit()
    conn.close()
    conn1.close()
@socketio.on('userlo')
def usert(l):
    
    online.append(l['online'])
    
@app.route( '/friendrequest' )
def great():
   return render_template('./friendrequest.html')
@app.route('/login')
def diy():
    return render_template('./page1.html')
@app.route('/done')
def diy01():
    
    return render_template('./page2.html')

@socketio.on('login')
def user(dev):
    conn=sql.connect(host='localhost',user="root",passwd='',database='user')
    cursor=conn.cursor()
    sql7="SELECT * FROM user_information"
    
    cursor.execute(sql7)
    users=cursor.fetchall()
    password=dev['password']
    username=dev['username']
    
   
    for a in range(len(users)):
        if username==users[a][1] and  password==users[a][2]:
               
                
                username1={'user':username}
                socketio.emit('user',username1)
    conn.close()



 
    
@socketio.on('removed')
def ght(y):
    global online
    online.remove(y['online'])
    i={'userremove':y['online']}
    socketio.emit('removeuser',i)
  
    
    
    
@socketio.on('online')
def onlinename(t):
    conn1=sql.connect(host='localhost',user="root",passwd='',database='friends')
    cursor1=conn1.cursor()
    user2=t['online']
    sql8="SELECT * FROM {}"
    users=[]
    users1=[]
    users2=[]
    cursor1.execute(sql8.format(user2))
    user=cursor1.fetchall()
    
       
    userlength=cursor1.rowcount
    print(online)
    for users01 in user:
        users.append(users01[1])
    for a in range(0,len(online)):
        if online[a] in users:
            users1.append(online[a])
        else:
            users2.append(online[a])
    print(users2)
            
    username={'users':users1,'on':user2,'users2':users2}
    socketio.emit('usersonline',username)
@app.route('/signin')
def newuser():
    return render_template('./signup.html')
def gyet():
    username=request.form['username']
    password=request.form['pass']
    password1=request.form['pass1']
    phonenumber=request.form['phonenumber']
    if password1==password:
        pass
    else:
        return render_template('./signup.html',wrong="password not matched type again")
        
  
    

    
    

      
       


  
        
        
    
       
            
            
    
    







if __name__ == '__main__':
    socketio.run(app,debug=True)
     
