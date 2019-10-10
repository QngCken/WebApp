$(function(){
    var width=300;
    var speed=100;
    var delay=3000;
    var currentSlide=1;
    //轮播图切换
    var interval;
    var $slides=$(".slides");
    var $slide=$slides.find('.slide');
    // 可以通过Js代码copy第一个轮播图到最后的slide位置实现循环
    function startSlide(){
        interval=setInterval(function(){
            $slides.animate({"margin-left": '-='+width}, speed, function(){
                currentSlide++;
                if (currentSlide == $slide.length){
                    currentSlide=1;
                    $slides.css('margin-left', 0);
                }
            });
        }, delay);
    }
    function stopSlide(){
        clearInterval(interval);
    }
    $slide.on({'mouseover': stopSlide, 'mouseout': startSlide})
    startSlide();

    //页头header滚动悬浮
    var isFixed = false;
    $(window).on('scroll', function(){
        var btm = $('.btm');
        if($(this).scrollTop() > 96){
            btm.addClass('fixed');
            if(!isFixed){
                btm.css('top', '-80px');
                btm.animate({'top': 0}, 500);
                isFixed = true;
            }
        }
        if($(this).scrollTop() < 16){
            isFixed = false;
            btm.removeClass('fixed');
        }
    });
	
	
	
	
	
	
	
	

	
});