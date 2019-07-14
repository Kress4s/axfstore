from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    url(r'^home/', views.home,name="home"),
    url(r'^market/$', views.market,name="market"),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.market_with_param,name="marketWP"),
    url(r'^cart/', views.cart,name="cart"),
    url(r'^mine/', views.mine,name="mine"),
    url(r'^register/', views.register,name="register"),
    url(r'^logout/', views.logout,name="logout"),
    url(r'^checkUser/', views.checkUser,name="checkUser"),
    url(r'^logoUser/', views.logoinUser,name="logoUser"),
    url(r'^addToCart/', views.addToCart,name="addToCart"),
    url(r'^subToCart/', views.subToCart,name="subToCart"),
    url(r'^changeSelectStatus/', views.changeSelectStatus,name="changeSelectStatus"),
    url(r'^addCartNum/', views.addCartNum,name="addCartNum"),
    url(r'^subCartNum/', views.subCartNum,name="subCartNum"),
    url(r'^chanageCartSelect/', views.chanageCartSelect,name="chanageCartSelect"),
    url(r'^generateOrder/', views.generateOrder,name="generateOrder"),
    url(r'^orderInfo/(.+)', views.orderInfo,name="orderInfo"),
    url(r'^chageOrderStatus', views.chageOrderStatus,name="chageOrderStatus"),
    url(r'^nopayOrder', views.nopayOrder,name="nopayOrder"),
]
