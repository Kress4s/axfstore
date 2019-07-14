import hashlib
import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

# 请求主页
from django.urls import reverse

from app.models import HomeWheel, HomeNav, HomeMustBuy, HomeShop, HomeShow, MarketFoodType, MarketGoods, UserModel, \
    CartModel, OrderModel, OrderGoodsModel


def home(request):
    # 查询到轮播图数据
    wheels = HomeWheel.objects.all()
    # 顶部nav导航数据
    navs = HomeNav.objects.all()
    # 必买数据
    mustbuys = HomeMustBuy.objects.all()
    # shop数据
    shops = HomeShop.objects.all()
    # 将Shop数据拆分
    shops1= shops[0:1]
    shops2_3 = shops[1:3]
    shops4_7 = shops[3:7]
    shops8_11 = shops[7:]

    # 获得show数据
    shows = HomeShow.objects.all()

    data = {
        "title":"主页",
        "wheels":wheels,
        "navs":navs,
        "mustbuys":mustbuys,
        "shops1":shops1,
        "shops2_3":shops2_3,
        "shops4_7":shops4_7,
        "shops8_11":shops8_11,
        "shows":shows

    }

    return render(request, "home/home.html",context=data)

# 请求 闪购 超市
def market(request):
   #  默认是 热销邦
   return redirect(reverse("axf:marketWP",args=("104749","0","1")))

# 请求超市/  携带参数
def market_with_param(request,typeid,childcid,sorttype):
    print(typeid)
    # 商品类型数据
    foodTypes = MarketFoodType.objects.all()
    # 商品所有数据
    # goodses = MarketGoods.objects.all()


    # 获取到childtypenames, 并拆分开来
    foodType = MarketFoodType.objects.filter(typeid=typeid).first()

    # 空判断

    # foodType = MarketFoodType()
    childtypes = foodType.childtypenames.split("#")
    # print(childtypes)

    allchildType = []

    for childtype in childtypes:
        type = childtype.split(":") #  ["全部分类","0"]
        allchildType.append(type)

    # 如果选择了子级筛选,则是继续在大分类上继续筛选
    if childcid == "0":
        # 根据商品类型来查询
        goodses = MarketGoods.objects.filter(categoryid=typeid)
    else:
        goodses = MarketGoods.objects.filter(categoryid=typeid).filter(childcid=childcid)

    # 排序
    # 综合排序---竞价排名

    if sorttype == "1":
        pass
    elif sorttype=="2":# 销量排序
        goodses = goodses.order_by("productnum")
    elif sorttype == "3": #价格最低
        goodses = goodses.order_by("price")
    elif sorttype == "4": #价格最高
        goodses = goodses.order_by("-price")
    else:
        pass


    data = {
        "title": "闪购",
        "foodTypes": foodTypes,
        "goodses": goodses,
        "typeid": typeid,
        "allchildType": allchildType,
        "childcid":childcid
    }

    return render(request, "market/market.html", context=data)


# 请求 购物车
def cart(request):
    # 先判断用户用户是否已经登录 ,作业:抽取是否登录判断
    userid = request.session.get("user_id")
    # 获得用户
    res = UserModel.objects.filter(pk=userid)

    if not res.exists():  # 不存在
        return redirect(reverse("axf:logoUser"))
    user = res.first()

    # 根据用户 查询购物车数据
    carts = CartModel.objects.filter(c_user=user)

    # 只要有一个没有被选中,则全选不能被选中
    is_allselect = True
    for cart in carts:
       if cart.c_isselect == False:
           is_allselect = False
           break



    data = {
        "title": "购物车",
        "carts":carts,
        "is_allselect":is_allselect,
    }
    return render(request, "cart/cart.html",context=data)


# 请求 我的
def mine(request):
    # 根据session 获取 user_id
    user_id = request.session.get("user_id")
    # 判断

    # 根据user_id获取到对应的user
    res = UserModel.objects.filter(pk=user_id)
    user = None
    is_login = False
    imgPath = "#"
    # 判断
    if res.exists():
        # user = UserModel()
        user = res.first()
        is_login = True
    #   图片地值
        imgPath = "/static/media/" + user.icon.url
        # print(imgPath)

    # 获得待付款,待收货, 待评价,售后/退款 的定单数量
    # 获得该用户下的所有订单

    # user = UserModel()
    orders = user.ordermodel_set.all()

    nopay = 0  # 待付款数量
    payed = 0  # 待收货数量
    noevaluate = 0 #待评价数量
    refund = 0 #退款数量

    # 遍历订单
    for order in orders:
        # order = OrderModel()
        status = order.o_status
        if status == 1:
            nopay +=1
        elif status == 2:
            payed +=1
        elif status == 3:
            noevaluate +=1
        elif status ==  4:
            refund +=1



    data = {
        "title": "我的",
        "user":user,
        "is_login":is_login,
        "imgPath":imgPath,
        "nopay":nopay,
        "payed":payed,
    }
    return render(request, "mine/mine.html",context=data)



# 注册请求
def register(request):
    method = request.method
    if method == "GET": #请求注册页面
        return  render(request,"user/user_register.html")
    elif method == "POST":#执行注册
#         现获取到上传的数据
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        icon = request.FILES["icon"]

        # print(username)
        # print(password)
        # print(email)
        # print(icon)

        # 保存到数据库
        userModel = UserModel()
        userModel.username = username
        userModel.password = createPwd(password)
        userModel.email = email
        userModel.icon = icon

        # 保存
        userModel.save()

        # 设置session,存储userid
        request.session["user_id"] = userModel.id

        return  redirect(reverse("axf:mine"))


#密码处理
def createPwd(password):
    mysha512 = hashlib.sha512()
    mysha512.update(password.encode("utf-8"))
    return  mysha512.hexdigest()

# 退出
def logout(request):
#    清除session
    request.session.flush()
    return redirect(reverse("axf:mine"))


# 验证用户名是否存在
def checkUser(request):
    username = request.GET.get("username")
#   根据用户名去数据库查数据
    res = UserModel.objects.filter(username=username)
    data = {}
    if res.exists():#存在
        data["status"] = "user is exist"
        data["msg"] = "用户名已经存在,请重新设置"
        data["code"] = "901"
    else:#不存在
        data["status"] = "ok"
        data["msg"] = "用户名可用"
        data["code"] = "200"

    return JsonResponse(data)

# 处理登录页面
def logoinUser(request):
    method = request.method
    if method == "GET":#请求登录页面
        return  render(request,"user/user_login.html")
    elif method == "POST": #处理登录请求
       username = request.POST.get("username")
       password = request.POST.get("password")

#      验证账号和密码
       res = UserModel.objects.filter(username=username)
       if res.exists(): #存在,继续验证密码
           user =  res.first()
           # user = UserModel()
           if user.password == createPwd(password):#密码也匹配
       #         设置一个session
                request.session["user_id"] = user.id

       #          重定向到 mine 页面
                return redirect(reverse("axf:mine"))

       return redirect(reverse("axf:logoUser"))

# 将商品添加到购物车
def addToCart(request):
    userid = request.session.get("user_id")
    # 获得用户
    res = UserModel.objects.filter(pk=userid)
    data = {
        "msg":"请求成功",
        "code":200,
        "status":"ok"
    }


    if not res.exists():#不存在
        # print("-----------1")
        # 重定向  到登录页
        # 问题: ajax请求不能执行重定向
        # return redirect(reverse("axf:logoUser"))
        data["code"] = 901 #未登录,重定向
        data["msg"] = "未登录,请重新登录"
        data["status"] = "ok"
        return JsonResponse(data)

    user = res.first()
    # 获得商品信息
    goodsid = int(request.GET.get("goodsid"))
    # 根据id查询出商品
    goods = MarketGoods.objects.filter(pk=goodsid).first()
#     保存到购物车
#    根据 用户 和 商品查询出购物车记录
    cartRes = CartModel.objects.filter(c_user=user,c_goods=goods)
    if cartRes.exists(): #存在该记录,表示修改
       cart = cartRes.first()
       # cart = CartModel()
       cart.c_num += 1
       cart.save()
       data["num"] = cart.c_num
    else:  #不存在,则需要添加一条记录
        cart = CartModel()
        cart.c_goods = goods
        cart.c_user = user
        cart.c_num = 1
        cart.save()
        data["num"] = 1
    return JsonResponse(data)


# 在超市页面做减少购物车商品操作
def subToCart(request):
    userid = request.session.get("user_id")
    # 获得用户
    res = UserModel.objects.filter(pk=userid)
    data = {
        "msg": "请求成功",
        "code": "200",
    }

    if not res.exists():  # 不存在
        # print("-----------1")
        # 重定向  到登录页
        # 问题: ajax请求不能执行重定向
        # return redirect(reverse("axf:logoUser"))
        data["code"] = "901"  # 未登录,重定向
        data["msg"] = "未登录,请重新登录"
        return JsonResponse(data)
    user = res.first()

    # 获得商品信息
    goodsid = int(request.GET.get("goodsid"))
    # 根据id查询出商品
    goods = MarketGoods.objects.filter(pk=goodsid).first()
    #     保存到购物车
    #    根据 用户 和 商品查询出购物车记录
    cartRes = CartModel.objects.filter(c_user=user, c_goods=goods)
    if cartRes.exists():
        cartModel = cartRes.first()
        # cartModel = CartModel()
        if cartModel.c_num == 1: #如果原数量为1.则直接删除该购物车记录
            cartModel.delete()
            data["num"] = 0
            data["code"] = "200"
        else:
            cartModel.c_num -= 1
            cartModel.save()
            data["num"] = cartModel.c_num
            data["code"] = "200"
    else: #没有该购物车记录,
        data["code"] = "902"
        data["msg"] = "没有该购物车记录,不能进行删除"

    return JsonResponse(data)

def changeSelectStatus(request):
    data = {}
    # 获取到cartid
    cartid = int(request.GET.get("cartid"))
    # 根据该cartid查询出对应的记录
    cart = CartModel.objects.filter(pk=cartid).first()
    # 修改状态
    # cart = CartModel()
    cart.c_isselect = not cart.c_isselect
    cart.save()
    data["code"] = "200"

    data["isSelect"] = cart.c_isselect

    # 设置 全选 是否选中
    # 先判断用户用户是否已经登录 ,作业:抽取是否登录判断
    userid = request.session.get("user_id")
    # 获得用户
    user = UserModel.objects.filter(pk=userid).first()
    # 根据用户查询该用户的所有的 购物车记录
    carts = CartModel.objects.filter(c_user=user)
    is_allselect = True
    for cart in carts:
        if not  cart.c_isselect:
            is_allselect = False
            break

    data["is_allselect"] = is_allselect


    return  JsonResponse(data)



# 改变购物车中商品的购买数量  加 操作
def addCartNum(request):
    data = {}
    cartid = int(request.GET.get("cartid"))
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    cart.c_num += 1
    cart.save()
    data["code"] = "200"
    data["num"] = cart.c_num

    return  JsonResponse(data)

# 改变购物车中商品的购买数量  减少操作
def subCartNum(request):
    data = {}
    cartid = int(request.GET.get("cartid"))
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    if cart.c_num == 1:#删除
        cart.delete()
        data["code"] = "901"

    else:
        cart.c_num -= 1
        cart.save()
        data["code"] = "200"
        data["num"] = cart.c_num


    return JsonResponse(data)



def chanageCartSelect(request):
    data = {}
    # 获得选中的字符串形式的列表, 是cartid
    selectList = request.GET.get("selectlist").split("#")
    # print(selectList)

    action = request.GET.get("action")
    if action == "noselection":
        # 拿出每一个 cart将其置为未选中
        for cartid in selectList:
            cartid = int(cartid)
            cart = CartModel.objects.filter(pk=cartid).first()
            # cart = CartModel()
            cart.c_isselect = False
            cart.save()
        data["code"] = "200"
        data["msg"] = "取消全选成功"
    else: #全部选中
        for cartid in selectList:
            cartid = int(cartid)
            cart = CartModel.objects.filter(pk=cartid).first()
            # cart = CartModel()
            cart.c_isselect = True
            cart.save()
        data["code"] = "200"
        data["msg"] = "全部选中成功"

    return JsonResponse(data)



# 点击选好了,生成一个订单
def generateOrder(request):
    data = {}
    # 获得选中的list,存放的是cartid
    selectList = request.GET.get("selectList").split("#")

    userid = int(request.session.get("user_id"))
    user = UserModel.objects.filter(pk=userid).first()


    # 生成一个订单
    order = OrderModel()
    #订单号,唯一的:    规则:时间 + 随机数 +  ...
    order.o_num = str(uuid.uuid4())
    order.o_user = user
    order.o_status = 1
    order.save()

    # 订单商品表
    for cartid  in selectList:
       cartid = int(cartid)
       #  先查出该条购物车记录
       cart = CartModel.objects.filter(pk=cartid).first()
       # cart = CartModel()

       goods = cart.c_goods
       goodsNum = cart.c_num

       #  创建一个订单商品
       orderGoods =  OrderGoodsModel()
       orderGoods.og_order =  order
       orderGoods.og_goods = goods
       orderGoods.og_num = goodsNum
       orderGoods.save()
    #  删除购物车中的该记录
       cart.delete()
    data["code"] = "200"
    #返回当前的订单号
    data["orderNumber"] = order.o_num

    return JsonResponse(data)


def orderInfo(request,orderNumber):
    # 获得订单号
    print(orderNumber + "8888888888888")

    # 根据订单号,  查出订单商品


    order = OrderModel.objects.filter(o_num=orderNumber).first()
    # order = OrderModel()

    print(order.o_num + "--------------")
    # order = OrderModel()
    ordergoods = order.ordergoodsmodel_set.all()
    # ordergood = OrderGoodsModel()
    # ordergood.og_goods.productlongname

    data = {
        "ordergoods":ordergoods,
        "orderNumber":orderNumber
    }

    return render(request,"order/order_info.html",context=data)


def chageOrderStatus(request):
    data = {}
    orderNumber = request.GET.get("orderNumber")
    status = request.GET.get("status")
    # 根据订单号查询对应的订单
    order = OrderModel.objects.filter(o_num=orderNumber).first()
    # order = OrderModel()
    # 修改状态
    order.o_status = int(status)
    order.save()
    data["code"] = "200"
    return JsonResponse(data)


# 查询没有付款的订单
def nopayOrder(request):
    data = {}
    userid = request.session.get("user_id")
    user = UserModel.objects.filter(pk=userid).first()
    # user = UserModel()
    #根据用户查询出所有 未付款的订单
    orders = user.ordermodel_set.filter(o_status=1)
    data = {
        "orders":orders,
    }

    # order = OrderModel()
    # order.o_num

    return  render(request,"order/order_nopay.html",context=data)












