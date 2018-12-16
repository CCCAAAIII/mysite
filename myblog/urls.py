from django.conf.urls import url
from myblog import views

urlpatterns = [
    url(r'^home/$',views.home,name='home'),
    url(r'index/$', views.index, name='index'),
    url(r'login/$', views.login, name='login'),
    url(r'^loginfault/$', views.loginfault, name='loginfault'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registerfault/$', views.registerfault, name='registerfault'),
    url(r'^registersuccess/$', views.registersuccess, name='registersuccess'),
    url(r'^addarticle/$',views.addarticle,name='addarticle'),
    url(r'^showarticlelist/$',views.showarticlelist,name='showarticlelist'),
    url(r'^addsuccess/$',views.addsuccess,name='addsuccess'),
    url(r'^articledetail/(\d+)/$',views.articledetail,name='articledetail'),
    url(r'^articleedit/(\d+)/$',views.articleedit,name='articleedit'),
    url(r'^articledelete/(\d+)/$',views.articledelete,name='articledelete'),
    url(r'^code/$',views.check_code,name='check_code'),
    url(r'^test/$',views.test,name='test'),
    url(r'^formtest/$',views.formtest,name='formtest'),
    url(r'^showimage/$',views.showimage,name='showimage'),
    url(r'^logout/$',views.logout,name='logout')

]
