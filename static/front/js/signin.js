$(function () {
    $("#signin_btn").click(function (ev) {
        telephone = $('input[name=telephone]').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        password = $('input[name=password]').val();
        ev.preventDefault();
        $.ajax({
            url:'/signin/',
            type:'post',
            data:{
                'telephone':telephone,
                'csrf_token':csrf,
                'password':password,
                "rember":$("#remberme").prop("checked")?1:2
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("登录成功");
                    window.location = $('meta[name=from]').attr('value')
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })
})

