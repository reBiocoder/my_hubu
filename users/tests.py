from django.test import TestCase

# Create your tests here.

from  slugify  import   slugify

txt="Python构建RESTful网络服务[Django篇：基于函数视图的API]"
print(txt[0:10])
r=slugify(txt)
print(r)