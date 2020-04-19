from  django  import   forms
from .  import  models

class Create_Topic_Form(forms.ModelForm):
    """
    2019/1/20,重写创建文章表单
    """
    class Meta:
        model =models.Create_Topic_Model
        fields = ('title','content',)
        error_messages={
            'title':{'required':'您未输入标题'},
            'content':{'requires':'请输入内容'}
                        }#数据格式为json格式
        widgets = {'title': forms.TextInput(attrs={"class": "form-control input-lg","style":"width: 900px;","placeholder":"输入文章标题..."}),}
