from django.shortcuts import render,redirect,get_object_or_404
from  django.http  import  JsonResponse,HttpResponseForbidden,HttpResponse
from  django.views.generic import View
# Create your views here.
from  .models import User_Info,FriendsApplication
from  topic.models import AgreeModel,Create_Topic_Model
import random
import datetime
class notificationView(View):
    def get(self,request):

        return  render(request,'users/notification.html')


def  editProfile(request):
    if request.user.is_authenticated:
        user=User_Info.objects.get(username=request.user.username)
        name=user.nick_name
        gender=user.gender
        oneWord=user.oneWords
        locations=user.location
        trade=user.trade
        jobs=user.jobs
        school=user.school
        introduction=user.introduction
        return  render(request,'users/editProfile.html',locals())
    else:
        redirect(to='account_login')


def editProfileApi(request):
    if request.user.is_authenticated:
        if request.is_ajax() and request.method=="GET":
            if request.GET.get("profileName"):
                name=request.GET.get("profileName")
                user=User_Info.objects.get(username=request.user.username)
                user.nick_name=name
                user.save()
                result={"name":user.nick_name,"gender":user.gender,"oneWord":user.oneWords,"location1":user.location, "trade":user.trade,"jobs":user.jobs,"school":user.school,"introduction":user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileGender"):
                name = request.GET.get("profileGender")
                user = User_Info.objects.get(username=request.user.username)
                user.gender = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade":user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileOneWord"):
                name = request.GET.get("profileOneWord")
                user = User_Info.objects.get(username=request.user.username)
                user.oneWords = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade":user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileLocation"):
                name = request.GET.get("profileLocation")
                user = User_Info.objects.get(username=request.user.username)
                user.location = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade":user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileTrade"):
                name = request.GET.get("profileTrade")
                user = User_Info.objects.get(username=request.user.username)
                user.trade = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade":user.trade,"jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileJob"):
                name = request.GET.get("profileJob")
                user = User_Info.objects.get(username=request.user.username)
                user.jobs = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade": user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileStudy"):
                name = request.GET.get("profileStudy")
                user = User_Info.objects.get(username=request.user.username)
                user.school = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade": user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            elif request.GET.get("profileIntroduction"):
                name = request.GET.get("profileIntroduction")
                user = User_Info.objects.get(username=request.user.username)
                user.introduction = name
                user.save()
                result = {"name": user.nick_name, "gender": user.gender, "oneWord": user.oneWords,
                          "location1": user.location, "trade": user.trade, "jobs": user.jobs, "school": user.school,
                          "introduction": user.introduction}
                return JsonResponse(result)
            else:
                return JsonResponse({"result":"未能成功返回所需要的数据"})
        else:
            return  redirect(to='account_login')
    else:
        return redirect(to='account_login')


def uploadPicture(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            picture = request.FILES.get("file", '')
            print(picture)
            """
            制造随机数名字,更改上传图片的名称
            """
            picture_extension=picture.name.split('.')[-1]
            new_file_name = random.randint(0, 4897151534531)
            picture_full_name='%s_%s.%s'%(new_file_name,'{0:%Y%m%d%H%M%S%f}'.format(datetime.datetime.now()),picture_extension)
            picture.name=picture_full_name
            user = User_Info.objects.get(username=request.user.username)
            user.avatar = picture
            user.save()
            return JsonResponse({"result":"上传成功"})
        else:
            return redirect(to='account_login')
    else:
        return redirect(to='account_login')

def  agreeView(request):
    postId=request.POST.get("postId","")
    if request.user.is_authenticated:
        if request.method == 'POST' and request.is_ajax():
            """
            判断点赞是否存在
            """
            myPost=Create_Topic_Model.objects.get(id=postId)
            if AgreeModel.objects.filter(user=request.user,post=myPost).exists():
                postAgree=AgreeModel.objects.filter(user=request.user, post=myPost)[0]
                postAgree.delete()
                myPost.agree=int(myPost.agree)-1
                myPost.save()
                agreeNumber=myPost.agree
                realUser = User_Info.objects.get(username=myPost.user.username)
                realUser.agreeNumber -= 1
                realUser.allGoodBlogerNum -= 1
                realUser.save()

                return JsonResponse({"result":agreeNumber,"status":1})
            else:
                agreeInstance=AgreeModel()
                agreeInstance.user=request.user
                agreeInstance.post=myPost
                agreeInstance.save()
                myPost.increase_agree()
                agreeNumber = myPost.agree
                realUser = User_Info.objects.get(username=myPost.user.username)
                realUser.agreeNumber += 1
                realUser.allGoodBlogerNum += 1
                realUser.save()
                return JsonResponse({"result":agreeNumber,'status':0})
        else:
            return JsonResponse({"result":-2})
    else:
        return JsonResponse({"result": -1})


def  lookUserProfile(request,id):
    if request.method == 'GET':
        if id==request.user.id and request.user.is_authenticated:
            return redirect(to='topic:new_profile')
        else:
            try:
                lookUser = User_Info.objects.get(id=id)
                if  request.user.is_authenticated:
                    if FriendsApplication.objects.filter(sender=request.user,receiver=lookUser).exists() and FriendsApplication.objects.filter(sender=lookUser, receiver=request.user).exists():
                        attentionStatus = '相互关注'
                        lookUser.increaseMyIndex()
                        allPost=Create_Topic_Model.objects.filter(draft_pk__isnull=True,user=lookUser)
                        agreeSender=FriendsApplication.objects.filter(sender=lookUser)
                        agreeRecevier=FriendsApplication.objects.filter(receiver=lookUser)
                        agreePost=AgreeModel.objects.filter(user=lookUser)
                        return render(request,'users/lookProfile.html',locals())
                    elif FriendsApplication.objects.filter(sender=request.user,receiver=lookUser).exists():
                        attentionStatus = '已关注'
                        lookUser.increaseMyIndex()
                        allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True,user=lookUser)
                        agreeSender = FriendsApplication.objects.filter(sender=lookUser)
                        agreeRecevier = FriendsApplication.objects.filter(receiver=lookUser)
                        agreePost = AgreeModel.objects.filter(user=lookUser)
                        return render(request, 'users/lookProfile.html', locals())
                    else:
                        attentionStatus = '关注'
                        lookUser.increaseMyIndex()
                        allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True,user=lookUser)
                        agreeSender = FriendsApplication.objects.filter(sender=lookUser)
                        agreeRecevier = FriendsApplication.objects.filter(receiver=lookUser)
                        agreePost = AgreeModel.objects.filter(user=lookUser)
                        return render(request, 'users/lookProfile.html', locals())
                else:
                    attentionStatus='关注'
                    lookUser.increaseMyIndex()
                    allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True,user=lookUser)
                    agreeSender = FriendsApplication.objects.filter(sender=lookUser)
                    agreeRecevier = FriendsApplication.objects.filter(receiver=lookUser)
                    agreePost = AgreeModel.objects.filter(user=lookUser)
                    return render(request, 'users/lookProfile.html', locals())
            except:
                return render(request, 'error/404.html')
    else:
        redirect(to='topic:index')


# 关注视图

def  follow(request):
    if request.method=='POST' and request.is_ajax():
        if request.user.is_authenticated:
            requestUser = request.POST.get('requestUser')
            acceptUser = request.POST.get('acceptUser')
            status=request.POST.get('status')
            postId=request.POST.get('postId')
            getPost = Create_Topic_Model.objects.get(id=postId)
            if  status=='关注':
                try:
                    friend = FriendsApplication()
                    friend.receiver = User_Info.objects.get(username=acceptUser)
                    friend.sender = User_Info.objects.get(username=requestUser)
                    friend.save()
                    if FriendsApplication.objects.filter(sender=request.user,receiver=getPost.user).exists() and FriendsApplication.objects.filter(sender=getPost.user, receiver=request.user).exists():
                        return  JsonResponse({'newStatus': '相互关注'})
                    elif FriendsApplication.objects.filter(sender=request.user,receiver=getPost.user).exists():
                        return  JsonResponse({'newStatus': '已关注'})
                    else:
                        render(request, 'error/404.html')

                except:
                    return render(request, 'error/404.html')
            elif status=='已关注':
                try:
                    friend1 = FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=acceptUser),sender=User_Info.objects.get(username=requestUser))
                    friend1.delete()
                    return JsonResponse({'newStatus': '关注'})
                except:
                    return render(request, 'error/404.html')
            elif  status=='相互关注':
                try:
                    friend1 = FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=acceptUser),sender=User_Info.objects.get(username=requestUser))
                    friend1.delete()
                    friend2=FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=requestUser),sender=User_Info.objects.get(username=acceptUser))
                    friend2.update(status=0)
                    return JsonResponse({'newStatus': '关注'})
                except:
                    return render(request, 'error/404.html')
            else:
                return render(request, 'error/404.html')
        else:
            return render(request, 'error/404.html')
    else:
        return render(request, 'error/404.html')

#个人主页的点赞按钮,异步api

def profileFollow(request):
    if request.method=='POST'  and  request.is_ajax():
        if request.user.is_authenticated:
            try:
                status=request.POST.get('status','')
                requestUser=request.POST.get('requestUser','')
                lookUser=request.POST.get('lookUser','')
                if status == '关注':
                    try:
                        friend = FriendsApplication()
                        friend.receiver = User_Info.objects.get(username=lookUser)
                        friend.sender = User_Info.objects.get(username=requestUser)
                        friend.save()
                        if FriendsApplication.objects.filter(sender=request.user,receiver=User_Info.objects.get(username=lookUser)).exists() and FriendsApplication.objects.filter(sender=User_Info.objects.get(username=lookUser), receiver=request.user).exists():
                            return JsonResponse({'newStatus': '相互关注'})
                        elif FriendsApplication.objects.filter(sender=request.user, receiver=User_Info.objects.get(username=lookUser)).exists():
                            return JsonResponse({'newStatus': '已关注'})
                        else:
                            return  render(request, 'error/404.html')

                    except:
                        return render(request, 'error/404.html')
                elif status == '已关注':
                    try:
                        friend1 = FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=lookUser),sender=User_Info.objects.get(username=requestUser))
                        friend1.delete()
                        return JsonResponse({'newStatus': '关注'})
                    except:
                        return render(request, 'error/404.html')
                elif status == '相互关注':
                    try:
                        friend1 = FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=lookUser),
                                                                    sender=User_Info.objects.get(username=requestUser))
                        friend1.delete()
                        friend2 = FriendsApplication.objects.filter(receiver=User_Info.objects.get(username=requestUser),
                                                                    sender=User_Info.objects.get(username=lookUser))
                        friend2.update(status=0)
                        return JsonResponse({'newStatus': '关注'})
                    except:
                        return render(request, 'error/404.html')
                else:
                    return render(request, 'error/404.html')
            except:
                return render(request, 'error/404.html')
        else:
            return render(request, 'error/404.html')
    else:
        return render(request, 'error/404.html')