from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.urls import reverse

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.db.models import Prefetch
from django.db.models import OuterRef, Subquery
from django.db.models import Count

from .models import Category
from .models import Event
from .models import EventUser
from .models import Chat

from .forms import CategoryForm
from .forms import EventForm
from .forms import ChatForm


# Create your views here.
class IndexView(ListView):
    model = Event
    template_name = 'event/index.html'
    paginate_by = 3
    
    def get_queryset(self):
        object_list = Event.objects.select_related('category').order_by('id')
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'イベント一覧'
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'event/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '宴会くん'
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'event/category/list.html'
    paginate_by = 3
    
    def get_queryset(self):
        object_list = Category.objects.all().order_by('id')
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'カテゴリ一覧'
        return context


class CategoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('event:category_list')
    template_name = 'event/category/create.html'
    success_message = 'カテゴリ新規登録が完了しました'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'カテゴリ新規登録'
        return context


class CategoryUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('event:category_list')
    template_name = 'event/category/update.html'
    success_message = 'カテゴリ更新が完了しました'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'カテゴリ更新'
        return context


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event/list.html'
    paginate_by = 3
    
    def get_queryset(self):
        object_list = Event.objects.select_related('user','category').order_by('id')
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'イベント一覧'
        return context


class EventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event:event_list')
    template_name = 'event/event/create.html'
    success_message = 'イベント新規登録が完了しました'
    
    def get_form(self):
        form = super().get_form()
        user_id = self.request.user.id
        form.fields['user'].initial = user_id
        return form
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'イベント新規登録'
        return context


class OnlyMyEventMixin(UserPassesTestMixin):
    def test_func(self):
        user_id = self.request.user.id
        event_id = self.kwargs.get('pk')
        return Event.objects.filter(id=event_id, user=user_id).exists()


class EventUpdateView(OnlyMyEventMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    success_url = reverse_lazy('event:event_mylist')
    template_name = 'event/event/update.html'
    success_message = 'イベント更新が完了しました'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'イベント更新'
        return context
    
    def handle_no_permission(self):
        messages.error(self.request, 'マイイベントのみを更新できます')
        return redirect(resolve_url('event:event_mylist'))


class MyEventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event/event/mylist.html'
    paginate_by = 3
    
    def get_queryset(self):
        user_id = self.request.user.id
        object_list = Event.objects \
            .filter(user=user_id) \
            .select_related('category', 'user') \
            .order_by('id')
        return object_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'マイイベント一覧'
        return context


class EventDetailView(LoginRequiredMixin, DetailView):
    model = Event
    template_name = 'event/event/detail.html'
    
    def get_object(self):
        event_id = self.kwargs.get('pk')
        event = Event.objects \
            .filter(id=event_id) \
            .select_related('category', 'user') \
            .prefetch_related(
                Prefetch(
                    'eventuser_set',
                    queryset = EventUser.objects.select_related('user'),
                    to_attr = 'eventusers'
            )) \
            .first()
        return event
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'イベント詳細'
        
        # ログインユーザがイベントに参加しているかのデータ
        user_id = self.request.user.id
        event_id = self.kwargs.get('pk')
        is_attended = EventUser.objects.filter(user=user_id, event=event_id).exists()
        context['is_attended'] = is_attended
        return context


class EventUserCreateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    def get_success_url(self):
        # イベントID
        event_id = self.kwargs.get('event_id')
        # イベント詳細に移動
        return reverse('event:event_detail', kwargs={'pk' : event_id})
    
    def get(self, *args, **kwargs):
        # ログインユーザID
        user_id = self.request.user.id
        # イベントID
        event_id = self.kwargs.get('event_id')
        
        # イベントの定員判定
        event = Event.objects.filter(id=event_id).first()
        event_user_count = EventUser.objects.filter(event=event_id).count()
        if event_user_count >= event.number :
            # 定員なのでイベント詳細に戻る
            messages.error(self.request, '定員です')
            return redirect(self.get_success_url())
        
        # 参加しているかどうかの判定
        is_attended = EventUser.objects.filter(event=event_id, user=user_id).exists()
        if is_attended :
            # 参加しているのでイベント詳細に戻る
            messages.error(self.request, 'イベントに参加済みです')
            return redirect(self.get_success_url())
        
        # イベントユーザの新規登録
        eventuser = EventUser()
        eventuser.event_id = event_id
        eventuser.user_id = user_id
        eventuser.save()
        messages.success(self.request, 'イベントに参加しました')
        return redirect(self.get_success_url())


class EventUserDeleteView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    def get_success_url(self):
        # イベントID
        event_id = self.kwargs.get('event_id')
        # イベント詳細に移動
        return reverse('event:event_detail', kwargs={'pk' : event_id})
    
    def get(self, *args, **kwargs):
        # ログインユーザID
        user_id = self.request.user.id
        # イベントID
        event_id = self.kwargs.get('event_id')
        
        # イベントの参加判定
        eventuser = EventUser.objects.filter(event=event_id, user=user_id).first()
        if not eventuser :
            # イベント未参加なのでイベント詳細に戻る
            messages.error(self.request, 'イベントに参加していません')
            return redirect(self.get_success_url())
        
        # イベントユーザの削除
        eventuser.delete()
        messages.success(self.request, 'イベントから辞退しました')
        return redirect(self.get_success_url())


class OnlyEventAttendedMixin(UserPassesTestMixin):
    def test_func(self):
        # ログインユーザID
        user_id = self.request.user.id
        # イベントID
        event_id = self.kwargs.get('event_id')
        # ログインユーザがイベントに参加しているかの判定
        return EventUser.objects.filter(event=event_id, user=user_id).exists()


class ChatTalkView(OnlyEventAttendedMixin, SuccessMessageMixin, CreateView):
    model = Chat
    form_class = ChatForm
    template_name = 'event/chat/talk.html'
    
    def get_success_url(self):
        # イベントID
        event_id = self.kwargs.get('event_id')
        # イベント詳細に移動
        return reverse('event:chat_talk', kwargs={'event_id' : event_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'チャット'
        
        # イベントのチャット一覧を取得
        event_id = self.kwargs.get('event_id')
        object_list = Chat.objects \
            .filter(event=event_id) \
            .select_related('user') \
            .order_by('created_at')
        context['object_list'] = object_list
        
        # イベントID
        event_id = self.kwargs.get('event_id')
        # イベント取得
        object = Event.objects.filter(id=event_id).first()
        context['object'] = object
        return context
    
    def form_valid(self, form):
        # ログインユーザID
        user_id = self.request.user.id
        # イベントID
        event_id = self.kwargs.get('event_id')
        # チャットモデル取得
        chat = form.save(commit=False)
        # チャットにユーザIDを代入
        chat.user_id = user_id
        # チャットにイベントIDを代入
        chat.event_id = event_id
        # チャットを新規登録
        chat.save()
        # フラッシュメッセージを設定
        messages.success(self.request, 'チャットを投稿しました')
        # チャット画面にリダイレクト
        return redirect(self.get_success_url())
    
    def handle_no_permission(self):
        # イベントID
        event_id = self.kwargs.get('event_id')
        # フラッシュメッセージを設定
        messages.error(self.request, 'イベントに参加していません')
        # イベント詳細にリダイレクト
        return redirect(reverse('event:event_detail', kwargs={'pk' : event_id}))
