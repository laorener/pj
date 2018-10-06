$(function () {
    $("#saveBanner").click(function (ev) {
        ev.preventDefault();
        var saveoradd = $(this).attr('from');
        if  (saveoradd == 1){
            var url = "/cms/updateboard/";
        }else {
            url = "/cms/addboard/";
        }
        $.ajax({
            url:url,
            type:"post",
            data :{
                "csrf_token":$("#csrf_token").attr("value"),
                "boardname":$("#boardName").val(),
                "id":$("#id").val()
            },
            success:function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    window.location = "/cms/board/"
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
    $('.update-btn').click(function () {
        self = $(this);
        $('#myModal').modal('show');// 让模态框出来
        $('meta[name=csrf_token]').attr("value");
        $("#data-bannerName").val(self.attr('data-bannerName'));
        $('#saveBanner').attr("from",'1');
        $('#id').val(self.attr('data-id'));
        console.log($('#id').val())
    });
     $('#myModal').on('hidden.bs.modal', function (e) {
         e.preventDefault();
         $('#saveBanner').attr("from",'0')
    });
     $('.delete-btn').click(function (ev) {
        ev.preventDefault();
         $.ajax({
            url:'/cms/deleteboard/',
            type:'post',
            data:{
                'csrf_token':$("#csrf_token").attr("value"),
                'id':$(this).attr('data-id')
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("删除成功");
                    window.location.reload(); //  重新加载这个页面
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
});