
$(function () {
 $('#resetpwdbtn').click(function (ev) {
        oldpwd = $('#oldpwd').val();
        newpwd = $('#newpwd').val();
        newpwd2 = $('#newpwd2').val();
        csrf = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        $.ajax({
            url:'/cms/resetpwd/',
            type:'post',
            data:{
                'oldpwd':oldpwd,
                'newpwd':newpwd,
                'csrf_token':csrf,
                'newpwd2':newpwd2
            },
            success:function (data) {
                if (data.code == 200) {
                   xtalert.alertSuccessToast("修改密码成功");
                    $('#oldpwd').val('');
                    $('#newpwd').val('');
                    $('#newpwd2').val('');
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })
})



