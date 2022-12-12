from django.urls import path

from .views import (ChangeDetail, ChangeList, LogDetail, LogList,
                    SharedToDoList, ToDoCreate, ToDoDelete, ToDoDetail,
                    ToDoDetailReadOnly, ToDoList, ToDoUpdate, compare_changes,
                    make_changes, share_todo)

app_name = 'todo'

urlpatterns = [
    # todo views
    path('<int:pk>', ToDoDetail.as_view(), name='todo_detail'),
    path('<int:pk>/readonly', ToDoDetailReadOnly.as_view(), name='todo_detail_readonly'),
    path('', ToDoList.as_view(), name='todo_list'),
    path('create', ToDoCreate.as_view(), name='todo_create'),
    path('<int:pk>/update', ToDoUpdate.as_view(), name='todo_update'),
    path('<int:pk>/delete', ToDoDelete.as_view(), name='todo_delete'),

    # share and make changes
    path('share_todo', share_todo, name='share_todo'),
    path('make_changes/<int:todo_id>', make_changes, name='make_changes'),
    path('compare_changes/<int:change_id>', compare_changes, name='compare_changes'),
    path('change', ChangeList.as_view(), name='change_list'),
    path('change/<int:pk>', ChangeDetail.as_view(), name='change_detail'),
    path('shared_todo_list', SharedToDoList.as_view(), name='shared_todo_list'),

    # logs
    path('todo/log', LogList.as_view(), name='log_list'),
    path('todo/log/<int:pk>', LogDetail.as_view(), name='log_detail'),
]
