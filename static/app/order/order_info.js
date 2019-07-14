$(function () {
    $("#payButton").click(function () {
    //  假装支付成功


        //进行修改状态的请求
    orderNumber = $(this).attr("orderNumber")
    $.getJSON("/axf/chageOrderStatus",{"status":2,"orderNumber":orderNumber},function (data) {
        if(data["code"] == 200){ //修改成功
               // 调到我的页面
            window.open("/axf/mine",target="_self")
        }
    })


    })
})






