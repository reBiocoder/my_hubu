$('[data-toggle="tooltip"]').tooltip();
/*writePost中所需要的js*/
$(document).ready(function(){
        /*var a = $("#username").val();
        var b = $("#password").val();*/
        $("#isSuccessPost").click(function(){
            $("#id_node").empty();
            $.ajax({
            type:"get",
            url:"/api/selectPost/",
            /*data:{"a":a, "b":b},*/
            dataType:"json",
            success:function(res){
              $.each(res.result,function(i,val){
                $('#id_node').append('<option value="'+val+'">'+val+'</option>');
              });
              },
        });
        });
        //**************************************************************************
        $("#ensurePost").click(function(){
            var t = $('form').serializeArray();
            $.each(t,function(i,val){
                if(val.value=='')
                {
                    if(val.name=='title')
                    {
                        confirm("请填写文章标题");
                    }
                    if(val.name=="content")
                    {
                        confirm("请编撰文章内容");
                    }
                    if(val.name=="node")
                    {
                        confirm("请选择文章分类");
                    }
                }

            });
        });
        /***************************************************************************/
//    保存文章草稿功能，设置content初始值
  $("#id_content").attr('placeholder',"markdown编辑器给您最专业的写作体验...");
});

var  lastTime;
var n=0;
$(function(){
    var draftsId="error";
  $("#id_content-wmd-wrapper").keyup(function (e) {
    lastTime = e.timeStamp;
    n+=1;
    if(n==1) {
        setTimeout(function () {
            //    如果键盘有0.5s未输入了，进行异步
            var title = $("input[name=title]").val();
            var content = $("#id_content").val();

            $.ajax({
                    url: "/api/drafts/",
                    type: "post",
                    dataType: "json",
                    data: {
                        "title": title,
                        "content": content,
                        "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),

                    },
                    success: function (res) {
                        draftsId = res.result.id
                    },
                    error: function (res) {
                        $("#writePostTitle").html("<p  style='color: #f1a325'>网络延时，文章未能成功保存至<a href=\"/drafts/watch/\">草稿箱</a></p>");
                    }
                },
            );

        }, 1);
    }
      if(n!=1)
      {
          setTimeout(function(){
          if (lastTime - e.timeStamp == 0) {
              var title = $("input[name=title]").val();
              var content = $("#id_content").val();
              $.ajax(
                  {
                      url: "/api/drafts/" + draftsId + "/",
                      type: "post",
                      dataType: "json",
                      data: {
                          "title": title,
                          "content": content,
                          "csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),

                      },
                      success: function (res) {
                          $("#writePostTitle p").html("文章已成功保存...");
                          setTimeout(function () {
                              $("#writePostTitle p").html("文章自动保存至<a href=\"/drafts/watch/\">草稿箱</a>")
                          }, 5000)

                      },
                      error: function (res) {
                          $("#writePostTitle").html("<p  style='color: #f1a325'>网络延迟，文章未能成功保存至<a href=\"/drafts/watch/\">草稿箱</a></p>");
                      }
                  }
              );
          }
      },2000);

      }
        });
    });
/*********************************************************/

$(
  function(){
      $("#profileHeadEnd").hide();
      $(".profileHeadButton").click(function(){
          $(".profileHeadButton").hide();
          $("#profileHeadEnd").show();

      });
      $(".profileHeadButtonTop").click(function () {
          $("#profileHeadEnd").hide();
           $(".profileHeadButton").show();

      });
      $(".postOrderButton").click(function(){
          var text=$(".postOrderButton").html();
          if (text=="按时间排序")
          {
              $(".postOrderButton").html("按赞数排序");
          }
          else
          {
              $(".postOrderButton").html("按时间排序");
          }
      });
  }
);
/*****************************************************************/
//个人信息板块

$(
    function () {
        $("#profileInfoFullNameForm").hide();
        $("#profileGender").hide();
        $("#profileOneWord").hide();
        $("#profileLocation").hide();
        $("#profileTrade").hide();
        $("#profileJob").hide();
        $("#profileStudy").hide();
        $("#profileIntroduction").hide();
        //***********************************************************************************
        $(".profileInfoFullName").hover(function(){
            $(".profileInfoFullName button").css('opacity','1');
        },
            function () {
                $(".profileInfoFullName button").css('opacity','0');
            }
        );
        $(".profileInfoFullName button").click(function(){
            $(".profileInfoFullName").hide();
            $("#profileInfoFullNameForm").show();
        });

        $("#profileInfoFullNameForm .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name=profileInfoFullName]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileName":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);
                },
                error:function(){
                    alert("失败");
                },
            });




        //    异步结束
            $("#profileInfoFullNameForm").hide();
            $(".profileInfoFullName").show();
        });
        $("#profileInfoFullNameForm .btn-gray").click(function(){
            $("#profileInfoFullNameForm").hide();
            $(".profileInfoFullName").show();
        });
        //********************************************************************************************

        $(".profileGender").hover(function(){
            $(".profileGender button").css('opacity','1');
        },
            function () {
                $(".profileGender button").css('opacity','0');
            }

        );
        $(".profileGender button").click(function(){
            $(".profileGender").hide();
            $("#profileGender").show();
        });

        $("#profileGender .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name='profileGender']:checked").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileGender":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });


        //    异步结束
            $("#profileGender").hide();
            $(".profileGender").show();
        });
        $("#profileGender .btn-gray").click(function(){
            $("#profileGender").hide();
            $(".profileGender").show();
        });

        //**************************************************************************************
                $(".profileOneWord").hover(function(){
            $(".profileOneWord button").css('opacity','1');
        },
            function () {
                $(".profileOneWord button").css('opacity','0');
            }

        );
                $(".profileOneWord button").click(function(){
            $(".profileOneWord").hide();
            $("#profileOneWord").show();
        });

        $("#profileOneWord .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name=profileOneWord]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileOneWord":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });


        //    异步结束
            $("#profileOneWord").hide();
            $(".profileOneWord").show();
        });
        $("#profileOneWord .btn-gray").click(function(){
            $("#profileOneWord").hide();
            $(".profileOneWord").show();
        });
         //***************************************************************************************************
                        $(".profileLocation").hover(function(){
            $(".profileLocation button").css('opacity','1');
        },
            function () {
                $(".profileLocation button").css('opacity','0');
            }

        );
         $(".profileLocation button").click(function(){
            $(".profileLocation").hide();
            $("#profileLocation").show();
        });

        $("#profileLocation .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name=profileLocation]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileLocation":name},
                dataType:"json",

                success:function(res){
                   $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });

        //    异步结束
            $("#profileLocation").hide();
            $(".profileLocation").show();
        });
        $("#profileLocation .btn-gray").click(function(){
            $("#profileLocation").hide();
            $(".profileLocation").show();
        });
        //*****************************************************************************************************
         $(".profileTrade").hover(function(){
            $(".profileTrade button").css('opacity','1');
        },
            function () {
                $(".profileTrade button").css('opacity','0');
            }

        );
        $(".profileTrade button").click(function(){
            $(".profileTrade").hide();
            $("#profileTrade").show();
        });

        $("#profileTrade .btn-primary").click(function(){
        //    异步上传用户名；
                    var name=$("input[name=profileTrade]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileTrade":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });

        //    异步结束
            $("#profileTrade").hide();
            $(".profileTrade").show();
        });
        $("#profileTrade .btn-gray").click(function(){
            $("#profileTrade").hide();
            $(".profileTrade").show();
        });
        //*****************************************************************************************************
                                        $(".profileJob").hover(function(){
            $(".profileJob button").css('opacity','1');
        },
            function () {
                $(".profileJob button").css('opacity','0');
            }

        );
        $(".profileJob button").click(function(){
            $(".profileJob").hide();
            $("#profileJob").show();
        });

        $("#profileJob .btn-primary").click(function(){
        //    异步上传用户名；
                            var name=$("input[name=profileJob]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileJob":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });

        //    异步结束
            $("#profileJob").hide();
            $(".profileJob").show();
        });
        $("#profileJob .btn-gray").click(function(){
            $("#profileJob").hide();
            $(".profileJob").show();
        });

        //****************************************************************************************************
                                                $(".profileIntroduction").hover(function(){
            $(".profileIntroduction button").css('opacity','1');
        },
            function () {
                $(".profileIntroduction button").css('opacity','0');
            }

        );
         $(".profileIntroduction button").click(function(){
            $(".profileIntroduction").hide();
            $("#profileIntroduction").show();
        });

        $("#profileIntroduction .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name=profileIntroduction]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileIntroduction":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });


        //    异步结束
            $("#profileIntroduction").hide();
            $(".profileIntroduction").show();
        });
        $("#profileIntroduction .btn-gray").click(function(){
            $("#profileIntroduction").hide();
            $(".profileIntroduction").show();
        });

        //****************************************************************************************************
                                                        $(".profileStudy").hover(function(){
            $(".profileStudy button").css('opacity','1');
        },
            function () {
                $(".profileStudy button").css('opacity','0');
            }

        );
         $(".profileStudy button").click(function(){
            $(".profileStudy").hide();
            $("#profileStudy").show();
        });

        $("#profileStudy .btn-primary").click(function(){
        //    异步上传用户名；
            var name=$("input[name=profileStudy]").val();
            $.ajax({
                url:"/user/api/editProfile/",
                type:"get",
                data:{"profileStudy":name},
                dataType:"json",

                success:function(res){
                    $("#edit-profile-info .profileInfoFullName strong").html(res.name);
                    $(".profileGender .profileHeadValue ").html(res.gender);
                    $(".profileOneWord .profileHeadValue ").html(res.oneWord);
                    $(".profileLocation .profileHeadValue ").html(res.location1);
                    $(".profileTrade .profileHeadValue ").html(res.trade);
                    $(".profileJob .profileHeadValue ").html(res.jobs);
                    $(".profileStudy .profileHeadValue ").html(res.school);
                    $(".profileIntroduction .profileHeadValue ").html(res.introduction);

                },
                error:function(){
                    alert("失败");
                },
            });



        //    异步结束
            $("#profileStudy").hide();
            $(".profileStudy").show();
        });
        $("#profileStudy .btn-gray").click(function(){
            $("#profileStudy").hide();
            $(".profileStudy").show();
        });
    //******************************************************************************************************
    });

//*******************文件上传******************************
$(
function(){
    $('#uploaderExample').uploader({
    autoUpload: true,            // 当选择文件后立即自动进行上传操作
    url: '/user/api/uploadPicture/',  // 文件上传提交地址
    filters:{
    mime_types: [
        {title: '图片', extensions: 'jpg,gif,png,jpeg,bmp,webp,JPG,GIF,PNG,JPEG,BMP,WEBP'},
        {title: '图标', extensions: 'ico,ICO'}
    ],
    // 不允许上传重复文件
    prevent_duplicates: true,
    max_file_size: '1mb',
},
    limitFilesCount:1,
    rename:false,
    multipart_params:{"csrfmiddlewaretoken": $("[name='csrfmiddlewaretoken']").val(),},
    responseHandler:function(responseObject, file){
        var myMessager =new $.zui.Messager('刷新界面更新头像', {
        icon: 'bell', // 定义消息图标
        type:'success',
        time: 0,
    });
        myMessager.show();
        setTimeout(function(){
            myMessager.hide();
        },6000);

    },
    onError:function () {
        var myMessager = new $.zui.Messager('头像上传发生错误', {
        icon: 'bell', // 定义消息图标
        type:'danger',
        time: 0,
    });
        myMessager.show();
        setTimeout(function(){
            myMessager.hide();
        },6000);
    }

});

});
//***************************头像结束****************************************************
