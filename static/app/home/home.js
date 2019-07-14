$(function () {
    //启动顶部菜单轮播
    initSwiper()
//    启动必买轮播
    initMustBuySwiper()

})

function initSwiper() {
   var mySwiper = new Swiper ('#topSwiper', {
    autoplay: 5000,//可选选项，自动滑动
    loop: true,
    // 如果需要分页器
    pagination: '.swiper-pagination',

  })
}


function initMustBuySwiper() {
   var mySwiper = new Swiper ('#swiperMenu', {
    slidesPerView: 3,  //一页显示的数量
    spaceBetween: 5,  //每页之间的间隔
  })
}



