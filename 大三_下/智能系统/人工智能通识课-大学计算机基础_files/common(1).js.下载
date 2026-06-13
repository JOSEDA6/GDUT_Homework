// JavaScript Document
//左侧导航选中js
$(function () {
    $(".nav-content ul li").click(function () {
        var dataname = $(this).attr("dataname");
        //打开新页面的地方不需要文件点击过去
        var openType =  $(this).attr("openType");
        if (dataname != "tk" && dataname != "bjexpand2" && dataname != "bjexpand1" && dataname != "bjexpand3" && openType != 1) {
            $(".nav-content ul li").removeClass("curNav");
            $(this).addClass("curNav");

            var pageHeader = $(this).attr("pageheader");
            if (typeof pageHeader === 'undefined') {
                return;
            }
            if ($("#toolMenu").length) {
                if (pageHeader == 21) {
                    $("#toolMenu").hide();
                } else {
                    $("#toolMenu").show();
                }
            }
        }
    })
    // $(".name").hover(function () {
    //     $(".loginCon").show();
    //     $(".loginCon").animate({"height": "98px", "opacity": "1"}, 400);
    // }, function () {
    //     $(".loginCon").animate({"height": "0", "opacity": "0"}, 400);
    //     $(".loginCon").hide();
    // })
})

	  $(function(){
		 	 var het =$(window).height();
		 	 var lefthet = het-52;
			 $(".sideCon").css("height",lefthet+"px");
		  })
	  window.onresize = function(){
 		 	var het =$(window).height();
		 	var lefthet = het-52;
			$(".sideCon").css("height",lefthet+"px");
        }

  $(document).ready(function() {
    $("#boxscrollleft").niceScroll({cursorborder:"",cursorwidth:"8px", cursorcolor:"#E6ECF5",boxzoom:false}); // First scrollable DIV
    $("#boxscrollRight").niceScroll({cursorborder:"",cursorwidth:"8px", cursorcolor:"#CfD8E6",boxzoom:false}); // First scrollable DIV
  });


//计算右测高度
var het = $(window).innerHeight();
var conhet = het -112;
var mainhet = $(".main").css("min-height",conhet)


