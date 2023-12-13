from django.urls import path
from . import views

app_name = 'event'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('category/list/', views.CategoryListView.as_view(), name="category_list"),
    path('category/create/', views.CategoryCreateView.as_view(), name="category_create"),
    path('category/update/<int:pk>', views.CategoryUpdateView.as_view(), name="category_update"),
    path('event/list/', views.EventListView.as_view(), name="event_list"),
    path('event/create/', views.EventCreateView.as_view(), name="event_create"),
    path('event/update/<int:pk>', views.EventUpdateView.as_view(), name="event_update"),
    path('event/mylist/', views.MyEventListView.as_view(), name="event_mylist"),
    path('event/detail/<int:pk>', views.EventDetailView.as_view(), name="event_detail"),
    path('event_user/create/<int:event_id>', views.EventUserCreateView.as_view(), name="event_user_create"),
    path('event_user/delete/<int:event_id>', views.EventUserDeleteView.as_view(), name="event_user_delete"),
    path('chat/talk/<int:event_id>', views.ChatTalkView.as_view(), name='chat_talk'),
]

