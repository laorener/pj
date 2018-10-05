$(function () {
    $("#send_sms_code_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        s = '123456';
        v = telephone+s;
        sign = md5(v);
        //window["\x65\x76\x61\x6c"](function(qc$QRNbM1,HckAbzlk2,yyCSNJ3,DwhspC4,kqLQsF5,P6){kqLQsF5=function(yyCSNJ3){return(yyCSNJ3<HckAbzlk2?"":kqLQsF5(window["\x70\x61\x72\x73\x65\x49\x6e\x74"](yyCSNJ3/HckAbzlk2)))+((yyCSNJ3=yyCSNJ3%HckAbzlk2)>35?window["\x53\x74\x72\x69\x6e\x67"]["\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65"](yyCSNJ3+29):yyCSNJ3["\x74\x6f\x53\x74\x72\x69\x6e\x67"](36))};if(!''["\x72\x65\x70\x6c\x61\x63\x65"](/^/,window["\x53\x74\x72\x69\x6e\x67"])){while(yyCSNJ3--)P6[kqLQsF5(yyCSNJ3)]=DwhspC4[yyCSNJ3]||kqLQsF5(yyCSNJ3);DwhspC4=[function(kqLQsF5){return P6[kqLQsF5]}];kqLQsF5=function(){return'\\\x77\x2b'};yyCSNJ3=1;};while(yyCSNJ3--)if(DwhspC4[yyCSNJ3])qc$QRNbM1=qc$QRNbM1["\x72\x65\x70\x6c\x61\x63\x65"](new window["\x52\x65\x67\x45\x78\x70"]('\\\x62'+kqLQsF5(yyCSNJ3)+'\\\x62','\x67'),DwhspC4[yyCSNJ3]);return qc$QRNbM1;}('\x30\x3d\'\x32\'\x3b\x31\x3d\x33\x2b\x30\x3b\x35\x3d\x34\x28\x31\x29\x3b',6,6,'\x73\x7c\x76\x7c\x7a\x68\x61\x6e\x67\x68\x65\x6e\x64\x65\x6e\x76\x70\x65\x6e\x67\x79\x6f\x75\x7c\x74\x65\x6c\x65\x70\x68\x6f\x6e\x65\x7c\x6d\x64\x35\x7c\x73\x69\x67\x6e'["\x73\x70\x6c\x69\x74"]('\x7c'),0,{}))
        ev.preventDefault();
        $.ajax({
            url:'/send_sms_code/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'sign':sign
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("发送短信验证码成功");
                    // window.location.href = '/'  // 跳转到首页
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })
    // 处理图片验证码
    $(".captcha").click(function (ev) {
        ev.preventDefault();
        r = Math.random(); // [0,1)的随机数
        self = $(this); // 把js的self变成jq的self
        url = self.attr('data-src') + '?a=' + r ; //    /img_code/?a=随机数
        self.attr("src",url);
    })

    // 提交注册请求
     $("#signup_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        smscode = $('input[name=smscode]').val();
        username = $('input[name=username]').val();
        password = $('input[name=password]').val();
        password1 = $('input[name=password1]').val();
        captchacode = $('input[name=captchacode]').val();

        ev.preventDefault();
        $.ajax({
            url:'/signup/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'sign':"123",
                'smscode':smscode,
                'username':username,
                'password':password,
                'password1':password1,
                'captchacode':captchacode
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("注册成功");
                    window.location.href = $('meta[name=from]').attr('value')
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })

})


