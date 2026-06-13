(function() {
    // 定位 CSDN 页面上的主要内容
    var mainContent = $("article, .blog-content-box, #content_views, .markdown_views").first();

    if (mainContent.length) {
    // 隐藏所有非主要内容的元素
    $("body").children().not(mainContent).hide();
    mainContent.css({
    'width': '100%',
    'margin': '0 auto',
    'padding': '0',
    'font-size': '12pt',
    'line-height': '1.5',
    'color': '#000'
    });

    $("body").css({
    'margin': '0',
    'padding': '0',
    'background': '#fff'
    });

    // 强制触发打印
    window.print();

    // 打印后恢复页面样式
    setTimeout(function() {
    location.reload();
    }, 1000);
    } else {
    alert("未找到文章内容，请检查页面结构。");
    }
    })();