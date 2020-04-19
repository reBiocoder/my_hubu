from  django  import  template
register=template.Library()

from  users.models import FriendsApplication
from  notifications.models import Notification
from  topic.models import Create_Topic_Model
from  bs4  import  BeautifulSoup
import  mistune
from lxml.html.clean import clean_html
@register.simple_tag
def notifications(request):
    allList=[]
    allReceiveNotifications = FriendsApplication.objects.filter(receiver=request.user)
    allSendNotifications = FriendsApplication.objects.filter(sender=request.user)
    for eachReceiceNotifications in allReceiveNotifications:
        if eachReceiceNotifications.isRead==0:
            allList.append(eachReceiceNotifications)
        else:
            continue
    for eachSendNotifications in allSendNotifications:
        if eachSendNotifications.isRead==0:
            allList.append(eachSendNotifications)
        else:
            continue
    allAgree = Notification.objects.filter(verb="文章点赞")
    for eachAgree in allAgree:
        if eachAgree.recipient == request.user:
            if eachAgree.level=='info':
                allList.append(eachAgree)
            else:
                continue
    number=len(allList)

    return  number

# 切割字符
@register.simple_tag
def CutContent(value):
    """
    2018/10/30更新
    使用beautifulsoup进行文章摘要显示
    :param value:
    :return:
    2019/2/7/引用旧版
    """
    # value=mistune.markdown(value)
    try:
        value=clean_html(mistune.markdown(value))
        soup=BeautifulSoup(value,'html.parser')
        soupText=soup.get_text()
        strNum=len(str(soupText))
        multiple=int(strNum*0.01)
        strResult=soupText[0:multiple]+str("......")
        return  strResult
    except:
        return ""


# 得到草稿的数量

@register.simple_tag
def getDratfsNumber(request):
    allDraftsNum=Create_Topic_Model.objects.filter(draft_pk__isnull=False,user=request.user).count()
    return allDraftsNum

# 得到makedown版本
@register.simple_tag
def getHtml(value):
    return mistune.markdown(value)






