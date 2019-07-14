$(function () {
//   验证密码时候一致
//    给确认密码框设置一个 内容改变事件
    $("#confirm_pwd").change(function () {
        //长度验证..


        // alert("xxxx")
        //    获取到输入框中的值
        pwd1 = $("#pwd").val()
        pwd2 = $("#confirm_pwd").val()
        // alert(pwd1 + "&" + pwd2)

        if (pwd1 == pwd2) {
            //    提示 两次输入的密码一致
            $("#message").html("两次输入的密码一致")
            $("#message").css("color", "green")
        } else {
            //    提示 两次输入的密码不一致
            $("#message").html("两次输入的密码不一致,请重新输入")
            $("#message").css("color", "red")
        }
    })

    //监听用户名输入框的改变
    $("#username").change(function () {
        // alert("用户名")
        // ajax 请求服务器
        myusername = $(this).val()
        $.getJSON("/axf/checkUser",{"username":myusername},function (data) {
            // console.log(data)
            // console.log(data["msg"])
            if(data["code"] == "200"){ //可用
                $("#username_info").html(data["msg"]).css("color","rgb(0,255,0)")
            }else if (data["code"] == "901"){ //不可用
                $("#username_info").html(data["msg"]).css("color","rgb(255,0,0)")
            }

        })

    })



})


//验证输入的内容是否合法,
//如果合法 则 返回 true表示可以提交
// 如果不合法 则 返回 false,表示不可以提交
function check_input() {
    /*//合法判断
    * 1.用户名没有被注册---请求服务器判断
    * 2.密码长度大于 6  *合法的字符
    * 3. 密码与确认密码必须一致
    * 4.提交的md5处理后的
    * */
    pwd$ = $("#pwd")
    password = pwd$.val()
    password2 = $("#confirm_pwd").val()
    color = $("#username_info").attr("color")
    if(color == "rgb(255,0,0)"){
        return false;
    }


    if (password.length < 6) {
        //提示:密码长度至少6位
        return false;
    }

    if (password != password2) {
        //提示:两次输入的密码不一致
        return false
    }

    //将密码进行md5处理
    result = md5(password)
    //将结果设置到密码输入框中去
    pwd$.val(result)
    //排除法,输入合法
    return true

    // alert("xxx")
    //获得密码值
    /* pwd1 =  $("#pwd").val()
     //进行md5处理啊
     result = md5(pwd1)


     alert(result)*/
    // return false;
}











