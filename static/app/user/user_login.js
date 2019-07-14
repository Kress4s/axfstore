function  check_input() {
    password = $("#pwd").val()
    res = md5(password)
    $("#pwd").val(res)
}







