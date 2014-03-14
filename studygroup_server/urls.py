from django.conf.urls import patterns, url, include
from rest_framework import routers
from server import views

router = routers.DefaultRouter()
router.register(r'users', views.StudentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^courses/add', views.AddCourseView.as_view()), 
    url('^courses/university/(?P<universityID>.+)/$', views.CourseList.as_view()),    
)