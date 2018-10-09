from celery_app import celery_server,app
from flask_mail import Message
from dysms_python.demo_sms_send import send_sms
from exts import mail
@celery_server.task
def setmail(data,r):
    with app.app_context():
        msg = Message("我的邮箱验证码", recipients=[data], body="验证码为" + r)
        mail.send(msg)
@celery_server.task
def setphone(data,rs):
    with app.app_context():
        r = send_sms(phone_numbers=data,
                              smscode=rs)
        # b'{"Message":"OK","RequestId":"26F47853-F6CD-486A-B3F7-7DFDCE119713","BizId":"102523637951132428^0","Code":"OK"}'
        # if json.loads(r.decode("utf-8"))['Code'] == 'OK':
        #     saveCache(data, rs, 30 * 60)
        #     return jsonify(respSuccess(msg="短信验证码发送成功，请查收"))
        # else:  # 发送失败
        #     return jsonify(respParamErr(msg="请检查网络"))