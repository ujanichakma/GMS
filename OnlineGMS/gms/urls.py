from django.urls import path
from .views import *

urlpatterns =[
    path('logout/',log_out,name='logout'),
    path('',login_view,name=''),
    path('authenticated/',dashboard,name='authenticated'),
    path('teacher/',teacher_dashboard,name='teacher'),
    path('teacher/<course>/<batch>/', make_result ,name='make_result'),
]