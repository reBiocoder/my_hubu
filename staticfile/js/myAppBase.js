//轮播项目
$(function () {


        var text = $('.carousel-inner .active img').attr('alt');
        $('#carousel-title').html(text);
        $('#myNiceCarousel').on('slide.zui.carousel', function () {
            var text = $('.carousel-inner .active img').attr('alt');
            $('#carousel-title').html(text);
            var text = $('.carousel-inner .active img').attr('alt');
            $('#carousel-title').html(text);

        })
    });

//首页的一些情况
$(
    function () {
        $('#recommend').click(function () {
            $('#newNew a').removeClass('color-index');
            $('#top a').removeClass('color-index');
            $('#recommend').addClass('color-index');
            $.ajax({
                url:'/',
                type:'get',
                dataType:'text',
                data:{'type':'recommend'},
                success:function (res) {
                  $('#list-Content').html(res);
                },
                error:function () {

                },
            });
        });
        $('#top').click(function () {
            $('#top a').addClass('color-index');
            $('#recommend').removeClass('color-index');
            $('#newNew a').removeClass('color-index');
            $.ajax({
                url:'/',
                type:'get',
                dataType:'text',
                data:{'type':'top'},
                success:function (res) {
                  $('#list-Content').html(res);
                },
                error:function () {
                    alert("失败");
                },
            });
        });
        $('#newNew').on('click',function(){
            $('#newNew a').addClass('color-index');
            $('#recommend').removeClass('color-index');
            $('#top a').removeClass('color-index');
            $.ajax({
                url:'/',
                type:'get',
                dataType:'text',
                data:{'page_id':'1','type':'newNew'},
                success:function (res) {
                  $('#list-Content').html(res);
                },
                error:function () {
                    alert("失败");
                },
            });

        });
        $(document).on('click',".load-more",'',function () {
            var num=$('#loading-number').text();
            var num1=parseInt(num);
            num1=num1+1;
            $('#loading-number').text(num1);
            $.ajax({
                url:'/',
                type:'get',
                dataType:'text',
                data:{'page_id':num,'type':'newNew'},
                success:function (res) {
                  $('#list-Content').html(res);
                },
                error:function () {
                    alert("失败");
                },
            });
        });
    }
);
$(function() {
    $(document).on('click', '#notification', function () {

            $.ajax({
                url: "/api/notifications/",
                type: "get",
                dataType: "json",
                success: function (res) {

                    // $("#notification .popover-content").empty();
                    var content = [];
                    //*************
                    var agree = res.result.agreeList;
                    $.each(agree, function (i, val) {
                        content.push('<li class=\'popover-notifications  button-mysettings\'  style=\'    font-size: 15px!important;\'>' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>' + val[0] + '</a>' + '赞了文章' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>' + val[1] + '</a>' + '<span style=\'margin-left: 10px;\'>' + val[2] + '</span>' + '天前' + '</li>');
                    });

                    if (content.length > 10) {
                        for (let i = content.length; i >= 9; i--) {
                            content.splice(i, 1);
                        }
                    }

                    //*************
                    var receive = res.result.allReceiveNotifications;
                    $.each(receive, function (i, val) {
                        content.push('<li class=\'popover-notifications  button-mysettings\'  style=\'    font-size: 15px!important;\'>' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>' + val[0] + '</a>' + '关注了您的主页' + '<span style=\'margin-left: 10px;\'>' + val[1] + '</span>' + '天前' + '</li>');


                    });
                    //################################################
                    var send = res.result.allSendNotifications;
                    $.each(send, function (i, val) {
                        content.push('<li class=\'popover-notifications  button-mysettings\' style=\'    font-size: 15px!important;\'>您关注了' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>' + val[0] + '</a>' + '的主页' + '<span style=\'margin-left: 10px;\'>' + val[1] + '</span>' + '天前</li>')
                    });
                    //********************}


                    //****************************************************

                    if (content.length == 0) {

                        content.push("<li class='popover-notifications  button-mysettings'>没有任何通知</li>")
                    }

                    for (let i = content.length; i > 15; i--) {
                        content.splice(i, 1);
                    }
                    content.push("<li class='popover-notifications  button-mysettings'><a href='/accounts/profile/' style='font-size: 15px!important;'>查看完整通知</a></li>")

                    $('#notification[data-toggle="popover"]').popover(
                        {
                            // tipClass:"popover-primary",
                            tipClass: "popover-area",
                            placement: 'bottom',
                            html: true,
                            content: content,
                        }
                    );
                    //***************************************************

                    $("#label-notification").hide();
                },


            });
    })
});
// $(
//     function () {
//         $("#notification").click(function(){
//             $.ajax({
//                 url:"/api/notifications/",
//                 type:"get",
//                 dataType:"json",
//                 beforeSend:function(res){
//                     alert("正在加载");
//                 },
//                 success:function(res){
//
//                      // $("#notification .popover-content").empty();
//                     var  content=[];
//                                         //*************
//                     var agree=res.result.agreeList;
//                     $.each(agree,function(i,val){
//                          content.push('<li class=\'popover-notifications  button-mysettings\'  style=\'    font-size: 15px!important;\'>' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>'+val[0]+'</a>' + '赞了文章' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>'+val[1]+'</a>'+'<span style=\'margin-left: 10px;\'>'+val[2]+'</span>' + '天前' + '</li>');
//                     });
//
//                     if(content.length>10) {
//                         for (let i = content.length; i >= 9; i--) {
//                             content.splice(i, 1);
//                         }
//                     }
//
//                     //*************
//                     var receive=res.result.allReceiveNotifications;
//                     $.each(receive,function(i,val) {
//                         content.push('<li class=\'popover-notifications  button-mysettings\'  style=\'    font-size: 15px!important;\'>' + '<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>'+val[0]+'</a>' + '关注了您的主页' + '<span style=\'margin-left: 10px;\'>'+val[1]+'</span>' + '天前' + '</li>');
//
//
//                     });
//                     //################################################
//                     var send=res.result.allSendNotifications;
//                     $.each(send,function(i,val){
//                         content.push('<li class=\'popover-notifications  button-mysettings\' style=\'    font-size: 15px!important;\'>您关注了'+'<a style=\'color: #0a67fb!important;font-size: 15px!important;\'>'+val[0]+'</a>'+'的主页'+'<span style=\'margin-left: 10px;\'>'+val[1]+'</span>' +'天前</li>')
//                     });
//                     //********************}
//
//
//                      //****************************************************
//
//                     if (content.length==0){
//
//                         content.push("<li class='popover-notifications  button-mysettings'>没有任何通知</li>")
//                     }
//
//                     for (let i=content.length;i>15;i--){
//                             content.splice(i,1);
//                     }
//                     content.push("<li class='popover-notifications  button-mysettings'><a href='/accounts/profile/' style='font-size: 15px!important;'>查看完整通知</a></li>")
//
//
//                      //***************************************************
//                      $('#notification[data-toggle="popover"]').popover(
//                         {
//                              // tipClass:"popover-primary",
//                             tipClass:"popover-area",
//                             placement:'bottom',
//                             html:true,
//                             content:content,
//                         }
//                         );
//                     $("#label-notification").hide();
//                 },
//
//
//
//             });
//         });
//
//
//     }
//
// );


// $(function(){
//     // 或者在初始化时指定弹出方向
// $('#notification[data-toggle="popover"]').popover(
//     {
//          // tipClass:"popover-primary",
//         tipClass:"popover-area",
//         placement:'bottom',
//         html:true,
//         content:"<li class='popover-notifications  button-mysettings'>您关注了<a style='color: #0a67fb!important;'>点击修改昵称</a>的主页<span style='margin-left: 10px;'>0天前</span></li>" +
//             "<br><li>您关注了点击修改昵称的主页0天前</li>" +
//             "<br><li>您关注了点击修改昵称的主页0天前</li>",
//
//     }
// );
// });





$(function(){
    var postId=$('input[name=postId]').attr('value');
    var postAuthor=$('input[name=postAuthor]').attr('value');
    var requestUser=$('input[name=requestUser]').attr('value');
    var editUrl='/writePost/edit/?postId='+postId;
    // 或者在初始化时指定弹出方向
//    判断是否登录
    if(postAuthor==requestUser) {

        $('#setting-button[data-toggle="popover"]').popover(
            {
                // tipClass:"popover-primary",
                tipClass: "popover-area",
                placement: 'top',
                html: true,
                content: "<button  class='btn btn-primary button-mysettings'><a href='" + editUrl + "'>修改文章</a></button>" +
                    "<br><button id='deletePost' class='btn btn-primary button-mysettings'>删除文章</button>",

            }
        );
    }
    else if(postAuthor==''){
        $('#setting-button').hide();
    }
    else
    {
        $('#setting-button[data-toggle="popover"]').popover(
            {
                // tipClass:"popover-primary",
                tipClass: "popover-area",
                placement: 'top',
                html: true,
                content: "<button  class='btn btn-primary button-mysettings  follow1'>关注作者</button>"
            }
        );

    }
});
//****************删除文章js代码***********************************
var myModalTrigger = new $.zui.ModalTrigger({
        title: "您确定要删除这篇文章吗？",
        custom: "<div id=\"isDefineDeletePost\" class=\"row\" style=\"display: block;\">\n" +
            "            <div class=\"col-md-3\">\n" +
            "            </div>\n" +
            "            <div class=\"col-md-5\">\n" +
            "            </div>\n" +
            "              <div class=\"col-md-2\">\n" +
            "              <button type=\"button\" data-dismiss=\"modal\"  style=\"font-size: 16px;\" class=\"btn btn-block\">取消</button></div>\n" +
            "            <div class=\"col-md-2\">\n" +
            "                <button type=\"button\" id=\"deleteDeletePost\" style=\"font-size: 16px;\" class=\"btn btn-block btn-primary\">确定</button>\n" +
            "          </div>\n" +
            "        </div>",
    });
var myMessager = new $.zui.Messager('删除成功!', {type: 'success',time:'8000'});
var myMessager1 = new $.zui.Messager('删除失败!', {type: 'danger',time:'8000'});

$(document).on('click','#deletePost',function () {
    myModalTrigger.show();
});
$(document).on('click','#deleteDeletePost',function () {
    var postId=$('input[name=postId]').attr('value');
    var requestUser=$('input[name=requestUser]').attr('value');
    $.ajax({
        url:'/writePost/delete/',
        type:'post',
        dataType:'json',
        data:{
            'postId':postId,
            'requestUser':requestUser,
        },
        success:function (res) {
            myModalTrigger.close();
            myMessager.show();
            setTimeout(function (){
                window.location.href = "/";
            },2000);

        },
        error:function(res){
            myMessager1.show();
        }
    });
});

//*****************************************************************
//点赞异步
$(
    function(){
    $("#agree-button").click(function(){
        var postId=$("input[name='postId']").val();
        $.ajax({
            type:"post",
            url:"/user/api/agreebutton/",
            dataType: "json",
            data:{'postId':postId},
            success:function (res) {
                var number=res.status;
                var agreeNumber=res.result;
                if (agreeNumber==-1)
                {
                 // new $.zui.Messager('登录后才能点赞', {
                 // icon: 'bell', // 定义消息图标
                 // placement: 'top',
                 // }).show();
                    window.location.href="/accounts/login/";

                }
                else if(agreeNumber==-2)
                {
                    new $.zui.Messager('非正常提交', {
                 icon: 'bell', // 定义消息图标
                 placement: 'top',
                 }).show();

                }
                else
                {
                    if (number==1)
                {
                    $("#agreeTwo").html('<br>\n' +
                        '        <button type="button"  class="btn  btn-lg notAgreeTwoButton">\n' +
                        '            <i style="font-size: 18px;" class="icon icon-heart-empty"></i>\n' +
                        '            <span class="notAgreeTwoFont" >赞同</span>\n' +
                        '            <span  class="agreetwo" style="margin-left: 10px;" >'+agreeNumber+'</span>\n' +
                        '        </button>');

                    $("#agree-button").html('<i class="icon icon-thumbs-o-up"></i>'+"赞同"+agreeNumber);
                    $("#top-agree").text(agreeNumber+' 人赞了该文章')
                    $("#agree-button").removeClass('agree').addClass('notAgree');

                }
                else
                {
                   $("#agree-button").html('<i class="icon icon-thumbs-up"></i>'+"赞同"+agreeNumber);
                   $("#top-agree").text(agreeNumber+' 人赞了该文章');
                    $("#agree-button").removeClass('notAgree').addClass('agree');
                   $("#agreeTwo").html('<br><button type="button" class="btn  btn-lg  agreeTwoButton"> <i style="font-size: 18px;color: white;" class="icon icon-heart"></i> <span class="agreeTwoFont">赞同</span> <span class="agreetwo" style="margin-left: 10px;color: white;text-shadow: 0 0px 0 #fff;" >'+agreeNumber+'</span> </button>');

                }

                }
            },
        });
    });

});
//点赞异步二

$(
    function(){
      $("#agreeTwo").click(
          function(){
              var postId=$("input[name='postId']").val();
        $.ajax({
            type:"post",
            url:"/user/api/agreebutton/",
            dataType: "json",
            data:{'postId':postId},
            success:function (res) {
                var number=res.status;
                var agreeNumber=res.result;
                if (agreeNumber==-1)
                {
                 // new $.zui.Messager('登录后才能点赞', {
                 // icon: 'bell', // 定义消息图标
                 // placement: 'top',
                 // }).show();
                    window.location.href="/accounts/login/";

                }
                else if(agreeNumber==-2)
                {
                 //    new $.zui.Messager('非正常提交', {
                 // icon: 'bell', // 定义消息图标
                 // placement: 'top',
                 // }).show();
                    window.location.href="/accounts/login/";

                }
                else
                {
                    if (number==1)
                {
                    $("#agreeTwo").html('<br>\n' +
                        '        <button type="button"  class="btn  btn-lg notAgreeTwoButton">\n' +
                        '            <i style="font-size: 18px;" class="icon icon-heart-empty"></i>\n' +
                        '            <span class="notAgreeTwoFont" >赞同</span>\n' +
                        '            <span  class="agreetwo" style="margin-left: 10px;" >'+agreeNumber+'</span>\n' +
                        '        </button>');
                    $("#agree-button").html('<i class="icon icon-thumbs-o-up"></i>'+"赞同"+agreeNumber);
                    $("#top-agree").text(agreeNumber+' 人赞了该文章')
                    $("#agree-button").removeClass('agree').addClass('notAgree');


                }
                else
                {
                   $("#agreeTwo").html('<br><button type="button" class="btn  btn-lg  agreeTwoButton"> <i style="font-size: 18px;color: white;" class="icon icon-heart"></i> <span class="agreeTwoFont">赞同</span> <span class="agreetwo" style="margin-left: 10px;color: white;text-shadow: 0 0px 0 #fff;" >'+agreeNumber+'</span> </button>');


                   $("#agree-button").html('<i class="icon icon-thumbs-up"></i>'+"赞同"+agreeNumber);
                   $("#top-agree").text(agreeNumber+' 人赞了该文章');
                   $("#agree-button").removeClass('notAgree').addClass('agree');

                }

                }
            },
        });

          }
      );

});

//滑动事件
$(
    function(){
        $(window).scroll(function(){
            var windowHeight=$(window).height();
            var documentHeight=$(document).height();
            var scrollHeight=$(document).scrollTop();
           if(documentHeight-windowHeight-scrollHeight<=100)
           {

           }
        });
    }
);

$(document).ready(function(){
    $("#sendRow").hide();
  $("#id_comment").focus(function(){
    $("#sendRow").show();
  });
  $("#commentCancel").click(function(){
      $("#defaultComment").append($("#comment-info"));
      $("#form-comment  input[name='parent']").val('');
    $("#defaultComment").append($("#form-comment"));
    $("#sendRow").hide();
  });

  $("#commentSend").click(function(){
      var coment=$("textarea[name='comment']").val();
      var  honeypot=$("input[name='honeypot']").val();
      var  content_type=$("input[name='content_type']").val();
      var object_pk=$("input[name='object_pk']").val();
      var  timestamp=$("input[name='timestamp']").val();
      var  security_hash=$("input[name='security_hash']").val();
      var parent=$("input[name='parent']").val();
      var csrfmiddlewaretoken=$("#entryCommentFrom input[name='csrfmiddlewaretoken']").val();
      if(coment==''){
          $("#comment-info").html('<div class="alert alert-warning">\n' +
              '    <div class="content"><strong>注意!</strong>评论内容不能为空。</div>\n' +
              '</div>');
          setTimeout(function () {
                          $("#comment-info").html('');
                      }, 3000);
      }
      else {
          $.ajax({
              url: "/articles/comments/post/",
              type: "post",
              dataType: "text",
              data: {
                  "comment": coment,
                  "honeypot": honeypot,
                  "content_type": content_type,
                  "object_pk": object_pk,
                  "timestamp": timestamp,
                  "security_hash": security_hash,
                  "parent": parent,
                  "csrfmiddlewaretoken": csrfmiddlewaretoken,
              },
              success: function (html, res, statusInfo) {
                  if (res == 'success')
                  {
                      $("#comment-info").html('    <div class="alert alert-success">\n' +
                          ' <strong>恭喜!</strong>\n' +
                          '    您的评论提交成功。\n' +
                          '</div>');
                      setTimeout(function () {
                          $("#comment-info").html('');
                          $("#defaultComment").prepend($("#comment-info"));
                      }, 3000);
                          $("#form-comment textarea").val('');
                          $("#form-comment  input[name='parent']").val('');
                          $("#defaultComment").append($("#form-comment"));
                          $("#sendRow").hide();
                          var postId=$("input[name='postId']").val();
                          $.ajax({
                              url:"/api/allCommentList/",
                              dataType:'text',
                              type:'post',
                              data:{
                                  'postId':postId,
                              },
                              success:function(res){
                                  $("#getAllComment").html(res);
                                  $(".comment_reply_link").click(function () {
           $(this).closest('.actions').append($("#comment-info"));
           $(this).closest('.actions').append($("#form-comment"));
           var b=$(this).closest('.actions').find('a').attr('data-comment-id');
           $("input[name='parent']").val(b);

        });
                              //    ************

                              //    ***********
                              },
                              error:function (res) {
                                  alert(res);
                              },
                          });

                  }
              },
              error: function (res) {
                  if (res.status == 200) {
                      $("#comment-info").html('<div class="alert alert-warning">\n' +
                          ' <strong>注意!</strong>\n' +
                          '    您的评论未能成功提交，可能是网络原因，请刷新后再试。\n' +
                          '</div>');
                      setTimeout(function () {
                          $("#comment-info").html('');
                      }, 4000);
                  }

              }
          });
      }

  });
});
//*************************************回复js********************************************************
$(
    function(){
        $(".comment_reply_link").click(function () {
           $(this).closest('.actions').append($("#comment-info"));
           $(this).closest('.actions').append($("#form-comment"));
           var b=$(this).closest('.actions').find('a[class="comment_reply_link"]').attr('data-comment-id');
           $("input[name='parent']").val(b);
        });

  $(document).on('click','.comment_delete_link',function(){
            var b=$(this).closest('.actions').find('a[class="comment_delete_link"]').attr('data-comment-id');
            window.commentId=b;
            $.zui.modalTrigger.show({
        title: "您确定要删除这条评论吗？",
        custom: "<div id=\"defineDelete\" class=\"row\" style=\"display: block;\">\n" +
            "            <div class=\"col-md-3\">\n" +
            "            </div>\n" +
            "            <div class=\"col-md-5\">\n" +
            "            </div>\n" +
            "              <div class=\"col-md-2\">\n" +
            "              <button type=\"button\" data-dismiss=\"modal\"  style=\"font-size: 16px;\" class=\"btn btn-block\">取消</button></div>\n" +
            "            <div class=\"col-md-2\">\n" +
            "                <button type=\"button\" id=\"deleteSend\" style=\"font-size: 16px;\" class=\"btn btn-block btn-primary\">确定</button>\n" +
            "          </div>\n" +
            "        </div>",
    })});

        $(document).on('click','#deleteSend',function(){
             // alert(window.commentId);
            $.ajax({
                url:'/articles/comments/delete/'+window.commentId+'/',
                data:{},
                dataType:'json',
                type:'post',
                success:function(res){
                    new $.zui.Messager('删除成功！', {
                        icon: 'bell',
                    type: 'success', // 定义颜色主题
                    }).show();
                    $.zui.modalTrigger.close();
                // 重新加载评论列表
                          var postId=$("input[name='postId']").val();
                          $.ajax({
                              url:"/api/allCommentList/",
                              dataType:'text',
                              type:'post',
                              data:{
                                  'postId':postId,
                              },
                              success:function(res){
                                  $("#getAllComment").html(res);
                                  $(".comment_reply_link").click(function () {
           $(this).closest('.actions').append($("#comment-info"));
           $(this).closest('.actions').append($("#form-comment"));
           var b=$(this).closest('.actions').find('a').attr('data-comment-id');
           $("input[name='parent']").val(b);

        });
                              //    ************

                              //    ***********
                              },
                              error:function (res) {
                                  new $.zui.Messager('评论列表更新失败，可能是网络原因，刷新再试。', {
                        icon: 'bell',
                    type: 'warning', // 定义颜色主题
                    }).show();
                              },
                          });

                //    ********************

                },
                error:function(res){
                    new $.zui.Messager('删除失败！可能是网络原因', {
                        icon: 'bell',
                    type: 'warning', // 定义颜色主题
                    }).show();
                },
            });
        })
});

//关注js
//*******************************************************************


$(document).on('click','.follow',function () {
    var postId=$('input[name=postId]').attr('value');
    var postAuthor=$('input[name=postAuthor]').attr('value');
    var requestUser=$('input[name=requestUser]').attr('value');
    var status=$.trim($('.follow').text());
    if(postAuthor=='')
    {
        new $.zui.Messager('请先登录！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else if(postAuthor==requestUser)
    {
        new $.zui.Messager('自己无法关注自己！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else
    {
        $.ajax({
            url:'/user/api/follow/',
            dataType:'json',
            type:'post',
            data:{
                'requestUser':postAuthor,
                'acceptUser':requestUser,
                'status':status,
                'postId':postId,
            },
            success:function(res){
                if (res.newStatus=='关注')
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon icon-plus-sign"></i>关注');

                }
                else if(res.newStatus=='已关注')
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon icon-check"></i>已关注');

                }
                else
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon  icon-exchange"></i>相互关注');


                }
            },
            error:function () {
                alert("失败");
            }

        });

    }
});




$(document).on('click','.follow1',function () {
    var postId=$('input[name=postId]').attr('value');
    var postAuthor=$('input[name=postAuthor]').attr('value');
    var requestUser=$('input[name=requestUser]').attr('value');
    var status=$.trim($('.follow').text());
    if(postAuthor=='')
    {
        new $.zui.Messager('请先登录！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else if(postAuthor==requestUser)
    {
        new $.zui.Messager('自己无法关注自己！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else
    {
        $.ajax({
            url:'/user/api/follow/',
            dataType:'json',
            type:'post',
            data:{
                'requestUser':postAuthor,
                'acceptUser':requestUser,
                'status':status,
                'postId':postId,
            },
            success:function(res){
                if (res.newStatus=='关注')
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon icon-plus-sign"></i>关注');
                    $('.follow1').html('关注作者');

                }
                else if(res.newStatus=='已关注')
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon icon-check"></i>已关注');
                    $('.follow1').html('已关注');
                }
                else
                {
                    $('.follow').html('<i style="font-size: 14px!important;" class="icon  icon-exchange"></i>相互关注');
                    $('.follow1').html('相互关注');

                }
            },
            error:function () {
                alert("失败");
            }

        });

    }
});

//******************************************************************

//个人主页关注js

$(document).on('click','#profileAttention',function () {
    var status=$.trim($('#profileAttention').text());
    var requestUser=$('input[name=requestUser]').attr('value');
    var lookUser=$('input[name=lookUser]').attr('value');
    if(requestUser=='')
    {
        new $.zui.Messager('请先登录！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else if(lookUser==requestUser)
    {
        new $.zui.Messager('自己无法关注自己！', {
        icon: 'bell' // 定义消息图标
    }).show();
    }
    else {
        $.ajax({
            url: '/user/api/profileFollow/',
            dataType: 'json',
            type: 'post',
            data: {
                'status': status,
                'requestUser': requestUser,
                'lookUser': lookUser,
            },
            success: function (res) {
                if (res.newStatus == '关注') {
                    $('#profileAttention').html('<i style="font-size: 14px!important;color: #fff!important;" class="icon icon-plus-sign"></i>关注');
                } else if (res.newStatus == '已关注') {
                    $('#profileAttention').html('<i style="font-size: 14px!important;color: #fff!important;" class="icon icon-check"></i>已关注');

                } else {
                    $('#profileAttention').html('<i style="font-size: 14px!important;color: #fff!important;" class="icon icon-exchange"></i>相互关注');
                }
            },
            error: function (res) {
                alert("失败");
            },
        });
    }
});

//异步所有的草稿

$(document).on('click','.draft-delete',function () {
    var draft_id=$(this).closest('.item-footer').attr('value');
    $.ajax({
        url:'/drafts/delete/?draft_id='+draft_id,
        dataType:'text',
        type:'get',
        success:function (res) {
            $('#draft-content').html(res);
        },
        error:function (res) {
            alert(res);

        }
    });
});

//排序js
$(document).on('click','#sortTime',function () {
    $('#sortHot').removeClass('sortClick');
    $('#sortTime').addClass('sortClick');
    var node_id=$('input[name=nodeTwo_id]').attr('value');
    $.ajax({
        url:'/sort/',
        dataType:'text',
        type:'get',
        data:{
            'node_id':node_id,
            'type':'时间',
        },
        success:function (res) {
            $('#sortContent').html(res);
        },
        error:function (res) {
          alert('网络有误');
        }
    });
});
$(document).on('click','#sortHot',function () {
        $('#sortHot').addClass('sortClick');
    $('#sortTime').removeClass('sortClick');

        var node_id=$('input[name=nodeTwo_id]').attr('value');
    $.ajax({
        url:'/sort/',
        dataType:'text',
        type:'get',
        data:{
            'node_id':node_id,
            'type':'热门',
        },
        success:function (res) {
            $('#sortContent').html(res);
        },
        error:function (res) {
          alert('网络有误');
        }
    });
});

