from django.shortcuts import render,redirect,get_object_or_404
from  django.views.generic import View
from  django.http  import  JsonResponse,HttpResponse,Http404,HttpResponseForbidden,FileResponse
from  .forms import    Create_Topic_Form
from  .models import Create_Topic_Model,Sort_Model,AgreeModel
from  notifications.models import Notification
from users.models import User_Info,FriendsApplication
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from  django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# Create your views here.
from  django.db.models import Q
import  random
import  datetime
import  time
import string
from .models import Carousel_Model,Create_Topic_Model,AgreeModel
from  users.models import FriendsApplication
from  threadedcomments.models import ThreadedComment
import requests
import re

import  os
root_path = os.getcwd()
def ads(request):
    ads_path = "/var/www/my_hubu/topic/ads.txt"
    print(ads_path)
    return FileResponse(open(ads_path, 'rb'))

def getCarousel(request):
    getCarsourel=Carousel_Model.objects.all()
    allCarourselList=[]
    for  tmp  in  getCarsourel:
        tmpDict={}
        tmpDict["post_id"]=tmp.post.id
        tmpDict["picture"]=str("https://www.biocoder.cn"+tmp.avatar.url)
        allCarourselList.append(tmpDict)
    return JsonResponse({"data":allCarourselList})

def apiGetSortContent(request):
    if request.method == "POST":
        node_id = request.POST.get('node_id', 1)
        node = Sort_Model.objects.get(id=int(node_id))
        allPost = Create_Topic_Model.objects.filter(node=node, draft_pk__isnull=True).order_by('-update_time')
        allPostList = []
        for eachLi in allPost:
            tmpDict = {}
            tmpDict["nick_name"] = eachLi.user.nick_name
            tmpDict["update_time"] = eachLi.update_time.strftime('%Y-%m-%d')
            tmpDict["sort"] = eachLi.node.node
            tmpDict["title"] = eachLi.title
            tmpDict["id"] = eachLi.id
            tmpDict["picture"] = eachLi.pictureUrl
            allPostList.append(tmpDict)
            #allPostList.append({"code": 0})
        return JsonResponse({"data": allPostList})   

def apiGetSort(request):
    allSort = Sort_Model.objects.all()
    eachSortList = []
    for eachSort in allSort:
        tmpDict={}
        tmpDict["name"]=eachSort.node
        tmpDict["picture"]="https://www.biocoder.cn"+eachSort.sort_img.url
        tmpDict["id"]=eachSort.id
        tmpDict["des"]=eachSort.name
        eachSortList.append(tmpDict)
    return JsonResponse({"data":eachSortList})



def apiGetPost(request):
    if request.method == "POST":
        postId=request.POST.get('postId',1)
        getPost = Create_Topic_Model.objects.get(id=int(postId), draft_pk__isnull=True)
        return JsonResponse({'data':{'title':getPost.title,'content':getPost.content,'author':getPost.user.nick_name,'update_time':getPost.update_time.strftime("%Y-%m-%d"),'sort':getPost.node.node}})


def apiAllPostRecommend(request):
    if request.method == "POST":
        allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True)[0:20]
        num = len(allPost)
        li = list(range(num))
        random.shuffle(li)
        allPostList = []
        for eachLi in li:
            tmpDict = {}
            tmpDict["nick_name"] = allPost[eachLi].user.nick_name
            tmpDict["update_time"] = allPost[eachLi].update_time.strftime('%Y-%m-%d')
            tmpDict["sort"] = allPost[eachLi].node.node
            tmpDict["title"] = allPost[eachLi].title
            tmpDict["id"] = allPost[eachLi].id
            tmpDict["picture"] = allPost[eachLi].pictureUrl
            allPostList.append(tmpDict)
        return JsonResponse({"data": allPostList,"code":0})
    else:
        return JsonResponse( {"code":1})


def apiAllPost(request):
    if request.method == "POST":
        try:
            offset = request.POST.get('offset', '0')
            num=10+int(offset)*10
            allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True)[0:num]
            allPostList = []
            for eachLi in allPost:
                tmpDict = {}
                tmpDict["nick_name"] = eachLi.user.nick_name
                tmpDict["update_time"] = eachLi.update_time.strftime('%Y-%m-%d')
                tmpDict["sort"] = eachLi.node.node
                tmpDict["title"] = eachLi.title
                tmpDict["id"] = eachLi.id
                tmpDict["picture"] = eachLi.pictureUrl
                allPostList.append(tmpDict)
            return JsonResponse({"data": allPostList,"code":0})
        except:
            return JsonResponse({"code":2})
    else:
        return JsonResponse( {"code":1})
class indexView(View):
    def get(self,request):
        if request.is_ajax():
            type=request.GET.get('type')
            if type=='newNew':
                page_id=request.GET.get('page_id','1')
                allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True).order_by('-update_time')
                page_id_int=int(page_id)
                pageNum=int(len(allPost)/8)+1
                tem=8*int(page_id)
                newAllPost=allPost[0:tem]
                return  render(request,'topic/newNew.html',locals())
            elif type=='recommend':
                allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True)
                num = len(allPost)
                li = list(range(num))
                random.shuffle(li)
                allPostList = []
                for eachLi in li:
                    allPostList.append(allPost[eachLi])
                return render(request, 'topic/recommend.html', locals())
            elif type == 'top':
                allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True,top=1).order_by('-update_time')
                return render(request,'topic/allTop.html',locals())
            else:
                return HttpResponse("有误")
        else:
            allPost = Create_Topic_Model.objects.filter(draft_pk__isnull=True)
            num=len(allPost)
            li=list(range(num))
            random.shuffle(li)
            allPostList=[]
            for eachLi  in li:
                allPostList.append(allPost[eachLi])
            allCarousel=Carousel_Model.objects.all()[0:3]
            allGoodBloger=User_Info.objects.all().order_by('-allGoodBlogerNum')[0:5]
            allGoodPost=Create_Topic_Model.objects.filter(draft_pk__isnull=True).order_by('-read_nums')[0:10]

            # """
            #         制作分页器
            #         """
            # p = Paginator(allPost, 15)
            # try:
            #     contacts = p.page(page_id)
            # except  PageNotAnInteger:
            #     contacts = p.page(1)
            # except  EmptyPage:
            #     contacts = p.page(p.num_pages)
            # cus_list=contacts
            return render(request, 'topic/index.html', locals())



class PostContentView(View):
    def  get(self,request,postId,slug):
        try:
            getPost = Create_Topic_Model.objects.get(id=postId,draft_pk__isnull=True)
            aboutPost=Create_Topic_Model.objects.exclude(id=getPost.id).filter(Q(title__icontains=getPost.title)|Q(content__in=getPost.title)|Q(user__nick_name__icontains=getPost.user.nick_name),draft_pk__isnull=True)[0:5]            
            if request.user.is_authenticated:
                if AgreeModel.objects.filter(user=request.user,post=getPost).exists():
                   if FriendsApplication.objects.filter(sender=request.user,receiver=getPost.user).exists() and FriendsApplication.objects.filter(sender=getPost.user, receiver=request.user).exists():
                        friendStatus = '相互关注'
                        getPost.increase_views()
                        status=1
                        return render(request, 'topic/postContent.html', locals())

                   elif FriendsApplication.objects.filter(sender=request.user,receiver=getPost.user).exists():
                       friendStatus = '已关注'
                       getPost.increase_views()
                       status = 1
                       return render(request, 'topic/postContent.html', locals())
                   else:
                       friendStatus = '关注'
                       getPost.increase_views()
                       status = 1
                       return render(request, 'topic/postContent.html', locals())
                else:
                    if FriendsApplication.objects.filter(sender=request.user,receiver=getPost.user).exists() and FriendsApplication.objects.filter(sender=getPost.user, receiver=request.user).exists():
                        friendStatus = '相互关注'
                        getPost.increase_views()
                        status = 0
                        return render(request, 'topic/postContent.html', locals())

                    elif FriendsApplication.objects.filter(sender=request.user, receiver=getPost.user).exists():
                        friendStatus = '已关注'
                        getPost.increase_views()
                        status = 0
                        return render(request, 'topic/postContent.html', locals())
                    else:
                        friendStatus = '关注'
                        getPost.increase_views()
                        status = 0
                        return render(request, 'topic/postContent.html', locals())
            else:
                friendStatus = '关注'
                status = 0
                getPost.increase_views()
                return render(request, 'topic/postContent.html', locals())
        
        except:
            return render(request,'error/404.html')


class writePostView(View):
    def get(self,request,type):
        """
        2019/1/20,
        得到写文章的内容,此时还未考虑请求者的身份验证.
        :param request:
        :return:
        """
        if type=='create':
            # 增加
            if  request.user.is_authenticated:
                forms=Create_Topic_Form()
                return  render(request,'topic/writePost.html',locals())
            else:
                return redirect(to="account_login")
        elif type=='edit':
            # 改
            post_id = request.GET.get('postId')
            post = Create_Topic_Model.objects.get(id=post_id)
            if  request.user==post.user:
                try:
                    forms=Create_Topic_Form(instance=post)
                    return  render(request,'topic/writePost.html',locals())
                except:
                    return render(request,'error/404.html')
            else:
                return render(request, 'error/404.html')
        else:
            return render(request, 'error/404.html')
    def post(self,request,type):
        if type=='create':
            # 增加
            if request.user.is_authenticated:
                forms=Create_Topic_Form(request.POST)
                sortnode=request.POST.get("sortnode","无")
                if forms.is_valid():
                    postInstance=Create_Topic_Model()
                    postInstance.title=forms.cleaned_data["title"]
                    postInstance.content=forms.cleaned_data["content"]
                    # mistune.markdown(forms.cleaned_data["content"])clean_html(mistune.markdown
                    postInstance.node = Sort_Model.objects.filter(node=str(sortnode))[0]
                    Sort_Model.objects.filter(node=str(sortnode))[0].updated_time=datetime.datetime.now()
                    Sort_Model.objects.filter(node=str(sortnode))[0].save()
                    postInstance.user=request.user
                    postInstance.getPostPictureUrl()
                    postInstance.updatePictureUrl()
                    postInstance.save()
                    myuser=User_Info.objects.get(id=request.user.id)
                    myuser.levels+=1
                    myuser.save()
                    return redirect(to='topic:postSuccess',username=postInstance.id)
                return render(request, 'error/404.html')
            else:
                return redirect(to="account_login")
        elif type=='edit':
            post_id = request.GET.get('postId')
            post = Create_Topic_Model.objects.get(id=post_id)
            if  request.user==post.user:
                try:
                    forms = Create_Topic_Form(request.POST)
                    sortnode = request.POST.get("sortnode", "无")
                    if forms.is_valid():
                        post.title=forms.cleaned_data["title"]
                        post.content=forms.cleaned_data["content"]
                        post.node=Sort_Model.objects.filter(node=str(sortnode))[0]
                        Sort_Model.objects.filter(node=str(sortnode))[0].updated_time=datetime.datetime.now()
                        Sort_Model.objects.filter(node=str(sortnode))[0].save()
                        post.getPostPictureUrl()
                        post.updatePictureUrl()
                        post.save()
                        #####################################
                        # 建议修改文章发表成功后的状态
                        #####################################
                        ##################################################
                        myuser = User_Info.objects.get(id=request.user.id)
                        myuser.levels += 1
                        myuser.save()
                        ###################################################
                        return redirect(to='topic:postSuccess', username=post.id)
                    return render(request, 'error/404.html')
                except:
                    return render(request,'error/404.html')
            else:
                return render(request, 'error/404.html')
        elif  type=='delete':
            try:
                postId=request.POST.get('postId','')
                requestUser=request.POST.get('requestUser','')
                deletePsot=Create_Topic_Model.objects.get(id=postId)
                if request.user==deletePsot.user  and request.is_ajax():
                    deletePsot.delete()
                    return JsonResponse({'result':'ok'})
                else:
                    return render(request, 'error/404.html')
            except:
                return render(request, 'error/404.html')
        else:
            return render(request, 'error/404.html')



def  selectPostAjaxView(request):
    """
    :param request:2019/1/20
    :return:
    异步加载文章分类项
    """
    allSort=Sort_Model.objects.all()
    eachSortList=[]
    for eachSort in allSort:
        eachSortList.append(eachSort.node)
    result={"result":eachSortList}
    return JsonResponse(data=result)


class  ajaxDraftsView(View):
    def  post(self,request):
        """
        第一次提交时，post提交
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            if request.is_ajax() and request.method=="POST":
                timestamp=int(time.time())
                #ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
                ran_str=int(random.randint(1,5200))
                draftStr=str(timestamp)+str(ran_str)
                draftInstance=Create_Topic_Model()
                title=request.POST.get("title","")
                if title=='':
                    draftInstance.title="无标题"
                else:
                    draftInstance.title=title
                draftInstance.content=request.POST.get("content","")
                draftInstance.user=request.user
                draftInstance.draft_pk=draftStr
                draftInstance.node=Sort_Model.objects.all()[0]
                draftInstance.save()
                result={"id":draftStr,"update-time":Create_Topic_Model.objects.get(draft_pk=draftStr).update_time,}
                return  JsonResponse({"result":result})
            return JsonResponse({"result":"未登录，无法获取数据"})
class ajaxDraftsContentView(View):
    def  post(self,request,draftsId):
        """
        更新草稿操作
        :param request:
        :return:
        """
        if request.user.is_authenticated:
            if request.is_ajax() and request.method=="POST":
                updateDrafts=Create_Topic_Model.objects.get(draft_pk=draftsId)
                title=request.POST.get("title",updateDrafts.title)
                if title=='':
                    updateDrafts.title="无标题"
                else:
                    updateDrafts.title=title
                updateDrafts.content=request.POST.get("content",updateDrafts.content)
                updateDrafts.user=request.user
                updateDrafts.save()
                return JsonResponse({"result":"草稿保存成功"})
        else:
            return JsonResponse({"result":"用户未登录"})

# 草稿箱的功能
class  DraftsView(View):
    def get(self,request,type):
        if request.user.is_authenticated and type=='watch':
            allDrafts=Create_Topic_Model.objects.filter(draft_pk__isnull=False,user=request.user).order_by('-update_time')
            return render(request,'topic/drafts.html',locals())
        elif request.user.is_authenticated and type=='delete' and request.is_ajax():
            draft_id=request.GET.get('draft_id')
            if request.user==Create_Topic_Model.objects.get(id=draft_id).user:
                realDraft=Create_Topic_Model.objects.get(id=draft_id)
                realDraft.delete()
                allDrafts = Create_Topic_Model.objects.filter(draft_pk__isnull=False,user=request.user).order_by('-update_time')
                return render(request,'topic/allDrafts.html',locals())
            else:
                return render(request, 'error/404.html')
        elif request.user.is_authenticated and type=='edit':
            draft_id = request.GET.get('draft_id')
            if request.user == Create_Topic_Model.objects.get(id=draft_id).user:
                realDraft = Create_Topic_Model.objects.get(id=draft_id)
                try:
                    forms = Create_Topic_Form(instance=realDraft)
                    return render(request, 'topic/writePost.html', locals())
                except:
                    return render(request, 'error/404.html')
            else:
                return render(request, 'error/404.html')
        else:
            return redirect(to="account_login")
    def  post(self,request,type):
        try:
            draft_id = request.GET.get('draft_id')
            forms = Create_Topic_Form(request.POST)
            sortnode = request.POST.get("sortnode", "无")
            postInstance=Create_Topic_Model.objects.get(id=int(draft_id))
            if request.user.is_authenticated and type == 'edit' and request.user == Create_Topic_Model.objects.get(id=draft_id).user:
                if forms.is_valid():
                    postInstance.title = forms.cleaned_data["title"]
                    postInstance.content = forms.cleaned_data["content"]
                    # mistune.markdown(forms.cleaned_data["content"])clean_html(mistune.markdown
                    postInstance.node = Sort_Model.objects.filter(node=str(sortnode))[0]
                    Sort_Model.objects.filter(node=str(sortnode))[0].updated_time=datetime.datetime.now()
                    Sort_Model.objects.filter(node=str(sortnode))[0].save()
                    postInstance.draft_pk=None
                    postInstance.user = request.user
                    postInstance.getPostPictureUrl()
                    postInstance.updatePictureUrl()
                    postInstance.save()
                    ##################################################
                    postInstance.user = request.user
                    myuser = User_Info.objects.get(id=request.user.id)
                    myuser.levels += 1
                    myuser.save()
                    ###################################################
                    return redirect(to='topic:postSuccess', username=postInstance.id)
                else:

                    return render(request, 'error/404.html')
            else:

                return render(request, 'error/404.html')

        except:

            return render(request, 'error/404.html')



class  EmailSettingsView(View):
    def get(self,request):
        if request.user.is_authenticated:
            return render(request, 'topic/emailSettings.html')
        else:
            return redirect(to="account_login")



# #########################查看个人信息板块##############################################
class  NewProfileView(View):
    def get(self,request):
        if request.user.is_authenticated:
            allPost=Create_Topic_Model.objects.filter(draft_pk__isnull=True,user=request.user)
            interestSender=FriendsApplication.objects.filter(sender=request.user)
            interestReceiver=FriendsApplication.objects.filter(receiver=request.user)
            agreePost=AgreeModel.objects.filter(user=request.user)
            # 'topic/new_profile.html'
            return render(request, 'topic/new_profile.html',locals())
        else:
            return redirect(to="account_login")
###########################异步提交通知########################################
def  notificationView(request):
    if request.user.is_authenticated:
        if request.is_ajax() and request.method=="GET":
            allReceiveNotifications=FriendsApplication.objects.filter(receiver=request.user).order_by('-created_at')
            allSendNotifications=FriendsApplication.objects.filter(sender=request.user).order_by('-created_at')
            receicerList=[]
            nowTime=datetime.datetime.now()
            for  eachReceiceNotifications  in  allReceiveNotifications:
                eachReceiceNotifications.isRead=1
                eachReceiceNotifications.save()
                delTime=nowTime-eachReceiceNotifications.created_at
                receicerList.append([eachReceiceNotifications.description(),delTime.days])

            senderList=[]
            for  eachSendNotifications  in allSendNotifications:
                eachSendNotifications.isRead=1
                eachSendNotifications.save()
                delTime = nowTime - eachSendNotifications.created_at
                senderList.append([eachSendNotifications.senderDescription(),delTime.days])
            """
            点赞通知
            """
            agreeList=[]
            allAgree=Notification.objects.filter(verb="文章点赞").order_by('-timestamp')
            for  eachAgree  in allAgree:
                if eachAgree.recipient==request.user:
                    eachAgree.level='warning'
                    eachAgree.save()
                    delTime = nowTime - eachAgree.timestamp
                    agreeList.append([eachAgree.actor.nick_name,eachAgree.description,delTime.days])
                else:
                    continue
            result={"allReceiveNotifications":receicerList,"allSendNotifications":senderList,'agreeList':agreeList}
            return  JsonResponse({"result":result})
        else:
            return redirect(to='topic:index')
    else:
        return redirect(to='topic:index')
#############################################################################

def allCommentList(request):
    """
    得到所有的评论与回复
    :param request:
    :return:
    """
    if request.is_ajax() and request.method=="POST":
        postId = request.POST.get('postId','')
        try:
            getPost = Create_Topic_Model.objects.get(id=postId)
            return render(request,'topic/allCommentList.html',locals())
        except:
            return HttpResponse("请求不合法！")
    else:
        return HttpResponse("请求不合法！")

# 个人分类视图

class  Sort_View(View):
    def get(self,request,node_id=Sort_Model.objects.all()[0].id):
        if request.is_ajax():
            typeId=request.GET.get('type','热门')
            node_id=request.GET.get('node_id',Sort_Model.objects.all()[0].id)
            if typeId=='热门':
                node = Sort_Model.objects.get(id=node_id)
                allPost = Create_Topic_Model.objects.filter(node=node, draft_pk__isnull=True).order_by('-agree','-read_nums')
                allNode = Sort_Model.objects.all()
                return render(request, 'topic/allSortContent.html', locals())
            elif typeId=='时间':
                node = Sort_Model.objects.get(id=node_id)
                allPost = Create_Topic_Model.objects.filter(node=node, draft_pk__isnull=True).order_by('-update_time')
                allNode = Sort_Model.objects.all()
                return render(request, 'topic/allSortContent.html', locals())

            else:
                return render(request, 'error/404.html')
        else:
            node=Sort_Model.objects.get(id=node_id)
            allPost=Create_Topic_Model.objects.filter(node=node,draft_pk__isnull=True).order_by('-agree','-read_nums')
            allNode=Sort_Model.objects.all()
            return render(request,'topic/sortNode.html',locals())

#
# class  SearchPost(View):
#     def  get(self):



def searchPostView(request):
    """
    查找文章
    :param request:
    :return:
    """
    if request.method=='GET':
        try:
            q=request.GET.get('q','')
            allPost=Create_Topic_Model.objects.filter(Q(title__icontains=q)|Q(content__in=q),draft_pk__isnull=True)
            aboutPost=Create_Topic_Model.objects.filter(Q(user__nick_name__icontains=q)|Q(user__username__icontains=q),draft_pk__isnull=True)
            allUser=User_Info.objects.all()
            num = len(allUser)
            li = list(range(num))
            random.shuffle(li)
            allUserList = []
            for eachLi in li:
                allUserList.append(allUser[eachLi])
            allUserList=allUserList[0:5]
            return  render(request,'topic/searchContent.html',locals())
        except:
            return render(request, 'error/404.html')
    else:
        return render(request, 'error/404.html')



def postSuccess(request,username):
    try:
        postInstance=Create_Topic_Model.objects.get(id=username)
        if postInstance.user==request.user:
            return render(request,'topic/postSuccess.html',locals())
        else:
            return render(request,'error/404.html')
        ##################################################
        # postInstance.user = request.user
        # myuser = User_Info.objects.get(id=request.user.id)
        # myuser.levels += 1
        # myuser.save()
        ###################################################
    except:
        return render(request,'error/404.html')







