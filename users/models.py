from django.db import models
#signal信号
from  django.db.models.signals import post_delete,post_save
from notifications.signals import notify
# Create your models here.
from  django.contrib.auth.models import AbstractUser
import  random
from django.core  import validators

from notifications.models import Notification
from  imagekit.models  import  ProcessedImageField
from imagekit.processors import ResizeToFill
from  django.core.validators import MaxValueValidator,MinValueValidator

import  time
#def usernameValidators(valuse)
class  User_Info(AbstractUser):
    '''
    2019/1/24用户信息更新,增加朋友关系，多对多
    2019/1/27更新用户数据表，增加多个个人信息相关设置
    '''
    nick_name=models.CharField(max_length=20,verbose_name='昵称',default='username')
    mobile = models.CharField(max_length=11,null=True, blank=True, verbose_name='电话号码', validators=[validators.RegexValidator(r"\d{11}")])
    levels=models.PositiveIntegerField(default=0,verbose_name="活跃积分",blank=True)
    avatar = ProcessedImageField(upload_to='image/%Y/%m', default='image/timg.jpg',
                                 processors=[ResizeToFill(160, 160)], format='JPEG', options={'quality': 100},
                                 verbose_name='用户头像', max_length=300, blank=True, null=True,
                                 height_field='avatarHeight', width_field='avatarWeight')
    avatarWeight=models.PositiveIntegerField(default=150,verbose_name="个人头像宽度")
    avatarHeight=models.PositiveIntegerField(default=150,verbose_name="个人头像高度")
    privilege=models.CharField(max_length=200,default=0,verbose_name=u'权限',blank=True)
    friends=models.ManyToManyField('self',blank=True,null=True)
    gender=models.CharField(verbose_name="性别",max_length=10
                            ,choices=(('male','男'),('female','女')),default='female')
    oneWords=models.CharField(max_length=50,default='他很懒,还没有更新一句话介绍...',verbose_name="一句话介绍自己",blank=True,null=True)
    location=models.CharField(max_length=20,default='暂无',verbose_name="居住地",blank=True,null=True)
    trade=models.CharField(max_length=20,default='生物信息',verbose_name="所在行业",blank=True,null=True)
    jobs=models.CharField(max_length=50,default='暂无',verbose_name="工作经历",blank=True,null=True)
    school=models.CharField(max_length=50,default='暂无',verbose_name="教育经历",blank=True,null=True)
    introduction=models.TextField(verbose_name="个人简介",default='暂无',blank=True,null=True)
    agreeNumber=models.PositiveIntegerField(default=0,verbose_name="总被点赞次数")
    attentionNumber=models.PositiveIntegerField(default=0,verbose_name="总被关注次数")
    allGoodBlogerNum = models.PositiveIntegerField(default=0, verbose_name="总有利数")
    allLookNumber= models.PositiveIntegerField(default=0, verbose_name="个人主页总被浏览数")
    class  Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name

    def  increaseMyIndex(self):
        self.allLookNumber+=1
        self.save(update_fields=['allLookNumber'])
    def  __str__(self):
        return   self.nick_name

    def  checkfriend(self,username):
        """
        1/24日更新，检查某人是否为好友
        :param username: 用户名
        :return: 布尔值
        """
        for  eachUser  in self.friends.all():
            if eachUser.username==username:
                return True
        return False

    def  save(self, *args, **kwargs):
        if self.nick_name=='username':
            self.nick_name=self.username
        return super(User_Info,self).save()



class FriendsApplication(models.Model):			#好友关注
    sender = models.ForeignKey(User_Info,related_name="friendsApplicationSender",on_delete=models.CASCADE,verbose_name="好友申请发起者")							#发送者
    receiver = models.ForeignKey(User_Info,related_name="friendsApplicationReceiver",on_delete=models.CASCADE,verbose_name="好友申请接收者")						#接收者
    status = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)], verbose_name="关注情况（0为sender关注，1为相互关注）")				#好友关注 0:sender已关注  1：相互关注
    isRead = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(1)], verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def description(self):
        return "{}".format(self.sender)
    def senderDescription(self):
        return "{}".format(self.receiver)


    def  update_status(self):
        oldSender=User_Info.objects.get(username=self.receiver.username)
        oldReceiver=User_Info.objects.get(username=self.sender.username)
        isStatus=FriendsApplication.objects.filter(sender=oldSender,receiver=oldReceiver)
        if isStatus.exists():
            isStatus.update(status=1)
        else:
            isStatus.update(status=0)

    def save(self,*args,**kwargs):
        self.update_status()
        return super(FriendsApplication,self).save(*args,**kwargs)

    class Meta:
        verbose_name="账户关注"
        verbose_name_plural = verbose_name



    def __str__(self):
            return "【{}】关注了【{}】".format(self.sender,self.receiver)




def friendsApplication_Save(sender, instance,**kwargs):
    if instance.receiver.id!=instance.sender.id:
        receiver=User_Info.objects.get(id=instance.receiver.id)
        receiver.attentionNumber+=1
        receiver.allGoodBlogerNum+=1
        receiver.save()
    else:
        pass

# 消息响应函数注册
post_save.connect(friendsApplication_Save,sender=FriendsApplication)


