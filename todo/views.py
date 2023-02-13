from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.http import HttpResponse

from .constants import USER_PERMISSION
from .forms import ChangeForm, ToDoForm
from .models import Change, Log, SharePermission, ToDo, User


def index(request):
    return render(request, 'index.html')

# To Do
class ToDoCreate(CreateView):
    form_class = ToDoForm
    success_url = reverse_lazy('todo:todo_list')
    template_name = 'todo/todo_create.html'

    def form_valid(self, form):
        user = self.request.user
        form.instance.owner = user
        return super().form_valid(form)

class ToDoUpdate(UpdateView):
    form_class = ToDoForm
    # success_url = reverse_lazy('todo:todo_detail' self.)
    template_name = 'todo/todo_update.html'
    queryset = ToDo.objects.all()

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('todo:todo_detail', kwargs={'pk': pk})

class ToDoDelete(DeleteView):
    model = ToDo
    success_url = reverse_lazy('todo:todo_list')
    template_name = 'todo/todo_delete.html'

class ToDoList(ListView):
    template_name = 'todo/todo_list.html'

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(owner=user)

class ToDoDetail(DetailView):
    model = ToDo
    template_name = 'todo/todo_detail.html'

class ToDoDetailReadOnly(DetailView):
    model = ToDo
    template_name = 'todo/todo_detail_readonly.html'

# Sharing
def share_todo(request):
    # print(f'request_method: {request.method}')
    if request.method == 'POST':
        todo = request.POST.get('todo', None)
        user = request.POST.get('user', None)
        permission = request.POST.get('permission', 'read_only')

        # print(f'type: type(todo)')
        # getting objects from ids
        todo = get_object_or_404(ToDo, pk=todo)
        user = get_object_or_404(User, pk=user)

        sp = SharePermission.objects.create(
            todo = todo,
            user = user,
            permission = permission
        )
        return redirect(reverse_lazy('todo:todo_detail', kwargs={'pk': todo.pk})) 
    else:
        # form = SharePermissionForm()
        user_todos = ToDo.objects.filter(owner=request.user)
        users_to_share = User.objects.all().exclude(username=request.user.username)

        context = {
            'user_todos': user_todos,
            'users_to_share': users_to_share,
            'permission': USER_PERMISSION
        }
        return render(request, 'todo/share_permission.html', context=context)

# make changes
def make_changes(request, todo_id):
    todo = get_object_or_404(ToDo, pk=todo_id)

    # Check if changes exist for todo by same user
    change_obj = Change.objects.filter(
            original_ref=todo_id, 
            change_by=request.user
        ).first()
    
    if request.method == 'POST':    
        change_form = ChangeForm(request.POST, instance=change_obj or None)

        if change_form.is_valid():
            change_obj = change_form.save(commit=False)
            change_obj.change_by = request.user
            change_obj.original_ref = todo
            change_obj.save()

            # also adding it in log
            Log.objects.create(
                todo_id=todo_id,
                updated_by=request.user.username,
            )
            return redirect(reverse_lazy('todo:shared_todo_list'))
        else:
            return HttpResponse(change_form.errors)
    else:
        # checking if user has permission to update or readonly
        sp = SharePermission.objects.filter(todo=todo, user=request.user).first()

        if sp:
            if sp.permission.lower() == 'read/write':
                if not change_obj:
                    change_obj = Change.objects.create(
                        title=todo.title, 
                        description=todo.description, 
                        category=todo.category, 
                        due_date=todo.due_date, 
                        status=todo.status, 
                        original_ref=todo, 
                        change_status='created',
                        change_by=request.user,
                    )

                change_form = ChangeForm(instance=change_obj)
                context = {
                    'change_form': change_form
                }
                return render(request, 'todo/make_changes.html', context=context)
            else:
                # readonly access
                return redirect(reverse_lazy('todo:todo_detail_readonly',kwargs={'pk': todo.pk}))
        else:
            return HttpResponse("You don't have permission to write or read this to do")

# compare changes approve / reject
def compare_changes(request, change_id):
    change_obj = get_object_or_404(Change, pk=change_id)
    todo = change_obj.original_ref
    if request.method == 'POST':
        action = request.POST['action']
        if action == 'approved':
            # changes to todo
            todo.title = change_obj.title
            todo.description = change_obj.description
            todo.category = change_obj.category
            todo.status = change_obj.status
            todo.due_date = change_obj.due_date

            change_obj.change_status = 'approved'
            todo.save()
            change_obj.save()
        else:
            change_obj.change_status = 'rejected'
            change_obj.save()
        return redirect(reverse_lazy('todo:todo_list'))
    else:
        context = {
            'change_obj': change_obj,
            'todo': todo
        }
        return render(request, 'todo/compare_changes.html', context=context)

# see logs
class LogList(ListView):

    def get_queryset(self):
        user = self.request.user
        user_todos = ToDo.objects.filter(owner=user)
        return Log.objects.filter(todo_id__in=user_todos)

class LogDetail(DetailView):
    model = Log
    template_name = 'todo/log_detail.html'

# change list
class ChangeList(ListView):
    template_name = 'todo/change_list.html'

    def get_queryset(self):
        # todo created by user but changes made by others to review
        user = self.request.user
        return Change.objects.filter(original_ref__owner=user)

class ChangeDetail(DetailView):
    template_name = 'todo/change_detail.html'
    model = Change

# shared todo with me list
class SharedToDoList(ListView):
    template_name = 'todo/shared_todo_list.html'

    def get_queryset(self):
        user = self.request.user
        shared_todo_id_with_me = SharePermission.objects.filter(user=user).values_list('todo__id', flat=True)
        todos = ToDo.objects.filter(pk__in=shared_todo_id_with_me)
        return todos
