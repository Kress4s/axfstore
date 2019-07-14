$(function () {
    $("#type_container").hide()
     $("#allsortrule").hide()

//  给 全部类型 设置点击事件 控制隐藏
    $("#allType").click(function () {
        $("#type_container").show()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-up")
        $("#allsortrule").hide()
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-down")


    })

    $("#type_container").click(function () {
        $(this).hide()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    })


    $("#allsort").click(function () {
        $("#allsortrule").show()
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-up")
        $("#type_container").hide()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    })

    $("#allsortrule").click(function () {
        $("#allsortrule").hide()
        $("#sortrule_g").removeClass().addClass("glyphicon glyphicon-chevron-down")

    })


    // +  按钮(添加到购物车)
    $(".addShopping").click(function () {
        addele = $(this);
        goodsid = addele.attr("goodsid");
    // ajax请求
        $.getJSON("/axf/addToCart/",{"goodsid":goodsid},function (data){
            if (data["code"] == "901"){ //未登录,跳到登录页
                window.open("/axf/logoUser",target="_self")
            }else if (data["code"] == "200"){//添加购物车成功
                console.log(data["num"]);
                //跟新数量
                //  console.log("xxx")
                addele.prev().html(data["num"])
            }
        })

    });

      //将购物车中的该商品减少一个
    $(".subShopping").click(function(){
        subele = $(this);
        goodsid = subele.attr("goodsid");
        $.getJSON("/axf/subToCart",{"goodsid":goodsid},function (data){
            if (data["code"] == "901"){ //未登录,跳到登录页
                window.open("/axf/logoUser",target="_self")
            }else if (data["code"] == "200"){//添加购物车成功
                subele.next().html(data["num"])
            }
        })

    })

})






