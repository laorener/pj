$(function () {
    $('#myModal').on('hidden.bs.modal', function (e) {
        $("#bannerName").val("");
        $('#imglink').val("");
        $('#link').val("");
        $('#priority').val("");
        $('#saveBanner').val("");
        $('#id').val("")
    })

    $('#saveBanner').click(function (ev) {
        var csrf = $('meta[name=csrf_token]').attr("value");
        var bannerName = $("#bannerName").val();
        var imglink=$('#imglink').val();
        var link=$('#link').val();
        var priority = $('#priority').val();
        var id = $('#id').val();
        ev.preventDefault();
        self = $(this);
        url = '/cms/addbanner/';
        if(id != null&& id != ""){
            url = '/cms/updatebanner/';
        }
        console.log(id)
        $.ajax({
            url:url,
            type:'post',
            data:{
                'csrf_token':csrf,
                'bannerName':bannerName,
                'imglink':imglink,
                'link':link,
                'priority':priority,
                'id':id
            },
            success:function (data) {
                if (data.code == 200) {
                     $('#myModal').modal('hide');
                     xtalert.alertSuccessToast("添加成功");
                     setTimeout(function(){ window.location.reload()},1000);
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            },
            error:function (err) {
                xtalert.alertErrorToast('请检查网络');
            }
        })
    })

    $('.delete-btn').click(function (ev) {
        var csrf = $('meta[name=csrf_token]').attr("value");
        ev.preventDefault();
        self = $(this);
        id = self.attr('data-id');
         $.ajax({
            url:'/cms/deletebanner/',
            type:'post',
            data:{
                'csrf_token':csrf,
                'id':id
            },
            success:function (data) {
                if (data.code == 200) {
                     xtalert.alertSuccessToast("删除成功");
                     setTimeout(function(){ window.location.reload()},1000);//  重新加载这个页面

                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })
    $('.update-btn').click(function () {
        self = $(this);
        $('#myModal').modal('show');// 让模态框出来
        $('meta[name=csrf_token]').attr("value");
        $("#bannerName").val(self.attr('data-bannerName'));
        $('#imglink').val(self.attr('data-imglink'));
        $('#link').val(self.attr('data-link'));
        $('#priority').val(self.attr("data-priority"));
        $('#id').val(self.attr('data-id'))
    })
})