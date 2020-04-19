from django.db import models
from  django.core.validators import MaxValueValidator,MinValueValidator
#####
from  mdeditor.fields import MDTextField
#####
from  PIL  import Image
from  users.models import User_Info

from  bs4  import BeautifulSoup

from slugify  import slugify
# Create your models here.
from notifications.models import Notification
#signal信号
from  django.db.models.signals import post_delete,post_save
from notifications.signals import notify
from  imagekit.models  import  ProcessedImageField
from imagekit.processors import ResizeToFill
import  mistune
from lxml.html.clean import clean_html
import os
import re
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class  Sort_Model(models.Model):
    """
    2019/01/20
    重写分类，与文章一对一关系
    2019/01/24
    对分类进行更新，更新为板块
    """
    name = models.CharField(max_length=30,verbose_name='文章分类/板块（内部）')
    node = models.CharField(max_length=20,verbose_name='文章分类/板块（外部）')
    manager = models.ForeignKey(User_Info,on_delete=models.CASCADE,verbose_name="板块管理人")
    parent = models.ForeignKey('self', on_delete=models.CASCADE,blank=True, null=True, related_name='childcolumn')
    description = models.TextField(verbose_name='板块描述')
    sort_img = ProcessedImageField(upload_to='sort/%Y/%m', default='image/timg.jpg',
                                 processors=[ResizeToFill(40, 40)], format='JPEG', options={'quality': 100},
                                 verbose_name='分类图标', max_length=300, blank=True, null=True,
                                 height_field='sort_imgHeight', width_field='sort_imgWeight')
    sort_imgWeight = models.PositiveIntegerField(default=150, verbose_name="个人头像宽度")
    sort_imgHeight = models.PositiveIntegerField(default=150, verbose_name="个人头像高度")

    post_number = models.IntegerField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="分类序号(用时间区分)")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新板块时间")
    class  Meta:
        verbose_name='板块'
        verbose_name_plural=verbose_name
        ordering=["pub_time",]

    def  __str__(self):
        return  self.node





class  Create_Topic_Model(models.Model):
    """
    2019/01/20,重新设计文章模型
    2019/01/24,重写外键
    """
    user=models.ForeignKey(User_Info,on_delete=models.CASCADE,verbose_name="作者")

    node = models.ForeignKey(Sort_Model, on_delete=models.CASCADE,verbose_name="文章分类")

    title = models.CharField(max_length=200, verbose_name='标题')
    
    zhihu_id = models.CharField(verbose_name="是否为知乎文章", max_length=500, null=True, blank=True)

    draft_pk = models.CharField(verbose_name="草稿id", max_length=500,null=True,blank=True)

    content = MDTextField(verbose_name='文章内容(html版)')

    pub_time = models.DateTimeField(auto_now_add=True,verbose_name="发布时间")

    read_nums = models.IntegerField(default=0, verbose_name=u"阅读次数")
    pictureUrl=models.CharField(max_length=200,verbose_name="文章样图",blank=True,null=True)

    update_time = models.DateTimeField(auto_now=True,verbose_name="修改时间",)
    top = models.IntegerField(validators=[MaxValueValidator(1),MinValueValidator(0)], default='0', blank=True, verbose_name="是否置顶(1表示置顶)",null=True)
    slug=models.SlugField(max_length=200,verbose_name="短标签",null=True,blank=True)
    agree=models.PositiveIntegerField(default=0,verbose_name="点赞次数")
    class  Meta:
        verbose_name='发表文章'
        verbose_name_plural=verbose_name
        ordering=('-pub_time',)

    def  __str__(self):
        return  str(self.title)

    # 使用方法统计阅读次数
    def increase_views(self):
        self.read_nums += 1
        self.save(update_fields=['read_nums'])
    #     获取文章中的图片地址
    def  getPostPictureUrl(self):
        value = clean_html(mistune.markdown(self.content))
        soup=BeautifulSoup(value,'html.parser')
        try:
            img = soup.find_all('img')
            src = img[0].get('src')
            src1 = str(src).replace('editor/', 'post/')
            self.pictureUrl=src1
            self.save()
            src = str(src).split('/')[3]
            pictureUrl1 = os.path.join(BASE_DIR, 'uploads', 'editor', src)
            im = Image.open(pictureUrl1)
            newIm = im.copy()
            newIm.thumbnail((200, 110),Image.ANTIALIAS)
            b = os.path.join(BASE_DIR, 'uploads', 'post', src)
            newIm.save(b)
        except:
            self.pictureUrl="无"
            self.save()
    def updatePictureUrl(self):
        content=self.content
        newText = re.findall(r'!\[\]\((.*)\)', content)
        for eachText in newText:
            content = content.replace(str(eachText), str('http://www.biocoder.cn' + eachText))
        self.content=content

    def  save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Create_Topic_Model,self).save(*args,**kwargs)
    def increase_agree(self):
        self.agree += 1
        self.save(update_fields=['agree'])



class  Carousel_Model(models.Model):
    title = models.CharField(max_length=50, verbose_name='轮播标题')
    post=models.ForeignKey(Create_Topic_Model,on_delete=models.CASCADE,verbose_name="关联文章")
    slug= models.CharField(max_length=500, verbose_name='轮播内容')
    update_at=models.DateTimeField(auto_now=True,verbose_name="生成时间")
    avatar = ProcessedImageField(upload_to='carousel/%Y/%m', default='image/timg.jpg',
                                 processors=[ResizeToFill(800, 250)], format='JPEG', options={'quality': 100},
                                 verbose_name='轮播图片', max_length=300, blank=True, null=True,
                                 height_field='avatarHeight', width_field='avatarWeight')
    avatarWeight = models.PositiveIntegerField(default=800, verbose_name="个人头像宽度")
    avatarHeight = models.PositiveIntegerField(default=250, verbose_name="个人头像高度")
    class  Meta:
        verbose_name='轮播内容'
        verbose_name_plural=verbose_name
        ordering=["-update_at",]

    def  __str__(self):
        return  self.title



# class  DraftsModel(models.Model):
#     """
#     1/20,还未考虑用户外键
#     1/24更新，加入用户外键
#     """
#     user = models.ForeignKey(User_Info, on_delete=models.CASCADE, verbose_name="作者")
#     draft_pk=models.CharField(verbose_name="草稿id",max_length=500)
#
#     title = models.CharField(max_length=200, default='无标题',verbose_name='草稿标题')
#     content = models.TextField(verbose_name='草稿内容')
#     update_time = models.DateTimeField(auto_now=True, verbose_name="草稿修改时间")
#
#     class  Meta:
#         verbose_name='草稿箱'
#         verbose_name_plural=verbose_name
#         ordering=('-update_time',)
#
#     def  __str__(self):
#         return  str(self.id)
# class Message(models.Model):
#     # 好友消息
#     sender = models.ForeignKey(User_Info, related_name='message_sender')  # 发送者
#     receiver = models.ForeignKey(User_Info, related_name='message_receiver')  # 接收者
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def description(self):
#         return "{}给你发送了消息{}".format(self.sender, self.content)
#
#     class Meta:
#         db_table = 'message'
#         verbose_name_plural = u'消息'

class  AgreeModel(models.Model):
    """
    点赞model 2019/1/31
    """
    user=models.ForeignKey(User_Info,on_delete=models.CASCADE,verbose_name="点赞用户")
    post=models.ForeignKey(Create_Topic_Model,on_delete=models.CASCADE,verbose_name="被点赞的文章")
    agreeTime=models.DateTimeField(auto_now_add=True,verbose_name="点赞时间")
    status=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(1)],verbose_name="是否已读")
    class  Meta:
        verbose_name='点赞模块'
        verbose_name_plural=verbose_name

    def  __str__(self):
        return  self.status

    def statisticsAgree(self,*args,**kwargs):
        realUser=User_Info.objects.get(username=self.post.user.username)
        realUser.agreeNumber+=1
        realUser.allGoodBlogerNum+=1
        realUser.save()

def Agree_Save(sender, instance,**kwargs):
    receiver = instance.post.user
    # if instance.post.user.username!=instance.user.username:
    #     instance.statisticsAgree()
    notify.send(sender=instance.user,recipient=receiver,verb="文章点赞",description=instance.post.title)



post_save.connect(Agree_Save,sender=AgreeModel)

