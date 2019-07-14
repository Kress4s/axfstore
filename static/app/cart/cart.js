$(function () {
//   购物车中 点击 商品前的是否选中 按钮 即 勾
    $(".is_chooice").click(function () {
        //获得cartid
        currentChooice = $(this)
        cartid = currentChooice.parents("li").attr("cartid")
        console.log(cartid)
        // alert("xxx")
        $.getJSON("/axf/changeSelectStatus", {"cartid": cartid}, function (data) {
            if (data["code"] == "200") {
                flag = "True"
                if (data["isSelect"]) { //选中  加上 勾
                    currentChooice.find("span").html("√")
                    flag = "True"
                } else { //不选中  去掉勾
                    currentChooice.find("span").html("")
                    //只要有一个没有被选中,则全选 必须去掉选中
                    flag = "False"
                }

                if (data["is_allselect"]) {//选中
                    $("#all_select").find("span").html("√")
                } else {
                    $("#all_select").find("span").html("")
                }

                currentChooice.attr("is_select", flag)

            }
        })

    })


    //购物车中 将商品的数量进行添加操作
    $(".addCartNum").click(function () {
        //    获得该cartid
        //获得cartid
        addCartNum = $(this)
        cartid = addCartNum.parents("li").attr("cartid")
        $.getJSON("/axf/addCartNum", {"cartid": cartid}, function (data) {
            if (data["code"] == "200") {
                //    改数量
                addCartNum.prev().html(data["num"])
            }
        })

    })

    $(".subCartNum").click(function () {
        subCartNum = $(this)
        cartid = subCartNum.parents("li").attr("cartid")
        $.getJSON("/axf/subCartNum", {"cartid": cartid}, function (data) {
            if (data["code"] == "200") {
                subCartNum.next().html(data["num"])
            } else if (data["code"] == "901") {
                //    将整个该条记录删除,即 删除 li
                subCartNum.parents("li").remove()
            }
        })
    })


//   全选按钮
    $("#all_select").click(function () {
        // 1.只要有一个是未选中状态, 则需要将所有的都置为选中, 且全选变为选中
        // 2.当所有的都是选中状态时, 则需要将所有的都位置位未选中,且全选变为 未选中
        //  解决方式:  客户端,     服务器
        allSelectEle = $(this)
        selectList = []
        noselectList = []
        //    遍历所有的商品,获取选中状态
        $(".is_chooice").each(function () {
            //    获得当前的选中状态
            currentCh = $(this)
            isSelect = currentCh.attr("is_select")
            console.log(isSelect)

            if (isSelect == "True") { //选中的
                cartid = $(this).parents("li").attr("cartid")
                selectList.push(cartid)
            } else { //没有选中的
                cartid = $(this).parents("li").attr("cartid")
                noselectList.push(cartid)
            }

        })

        //    打印下选中 的 未选中的
        console.log(selectList)
        console.log(noselectList)
        if (noselectList.length == 0) { //当前是全部选中
            //---置为全部不选中, 且全选不 选中
            $.getJSON("/axf/chanageCartSelect", {
                "selectlist": selectList.join("#"),
                "action": "noselection"
            }, function (data) {
                if (data["code"] == 200) { //修改成功
                    $(".is_chooice").each(function () {
                        $(this).find("span").html("")
                        $(this).attr("is_select", "False")
                    })
                    allSelectEle.find("span").html("")
                }
            })


        } else { //当前至少有一个未选中的
            //----置为全部选中   且全选 选中
            $.getJSON("/axf/chanageCartSelect", {
                "selectlist": noselectList.join("#"),
                "action": "selection"
            }, function (data) {
                if (data["code"] == 200) {
                    $(".is_chooice").each(function () {
                        $(this).find("span").html("√")
                        $(this).attr("is_select", "True")
                    })
                    allSelectEle.find("span").html("√")
                }
            })
        }
    })

    //点击选好了生成订单
    $("#generate_order").click(function () {
        selectList = []
        //获得选中的 cartid
        $(".is_chooice").each(function () {
            if ($(this).attr("is_select") == "True"){
                selectList.push($(this).parents("li").attr("cartid"))
            }
        })
        console.log(selectList)

        if (selectList.length == 0) {
            alert("没有选中的商品,请选择商品")
        } else {
            // ajax请求生成订单信息
            $.getJSON("/axf/generateOrder", {"selectList": selectList.join("#")}, function (data) {
                if (data["code"] == "200") { //生成订单成功

                // alert(data["orderNumber"])

                //   打开订单详情
                    window.open("/axf/orderInfo/" + data["orderNumber"],target="_self")
                }
            })
        }


    })

})






