$(function () {
    $(".update-btn").click(function (ev) {
        ev.preventDefault();
        self = $(this);
        var data_tag = self.attr('data-tag');
        var url = "/cms/addtag/";
        if  (data_tag == 'canceltag'){
            url = "/cms/deletetag/";
        }
        var post_id = self.attr('data-id');
        $.ajax({
            url:url,
            type:"post",
            data :{
                "csrf_token":$("#csrf_token").attr("value"),
                "post_id":post_id
            },
            success:function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    window.location.reload()
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
});