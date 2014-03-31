from django.conf.urls import patterns, url, include
from rest_framework import routers
from server import views

router = routers.DefaultRouter()
router.register(r'users', views.StudentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/?', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^verify_credentials/?', 'rest_framework.authtoken.views.obtain_auth_token'),
    url(r'^courses/add/?', views.AddCourseView.as_view()), 
    url(r'^courses/remove/?', views.RemoveCourseView.as_view()),     
    url(r'^register/?', views.RegisterUserView.as_view()),     
    url(r'^courses/university/(?P<universityID>.+)/?$', views.CourseList.as_view()),    
    url(r'^universities/list/?', views.UniversityView.as_view()),
    url(r'^locations/university/(?P<universityID>.+)/?$', views.UniversityLocationsView.as_view()),     
    url(r'^users/profile/?', views.StudentProfileView.as_view()),
    url(r'^sessions/courses/(id=\d+&)*(id=\d+)/?$', views.SessionPerCourseView.as_view()),    
    url(r'^sessions/university/(?P<universityID>.+)/?$', views.SessionByUniversityView.as_view()),    
)