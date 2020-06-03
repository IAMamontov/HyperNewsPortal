from django.shortcuts import redirect, Http404
from django.views import View


class TodoView(View):
    all_todos = []

    def delete(self, request, todo_del, *args, **kwargs):
        if todo_del in self.all_todos:
            self.all_todos.remove(todo_del)
            return redirect('/')
        raise Http404
