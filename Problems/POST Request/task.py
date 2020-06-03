from django.shortcuts import redirect
from django.views import View


class TodoView(View):
    all_todos = []

    def post(self, request, *args, **kwargs):
        todo_new = request.POST.get('todo')
        if todo_new not in self.all_todos:
            self.all_todos.append(todo_new)
        return redirect('/')
