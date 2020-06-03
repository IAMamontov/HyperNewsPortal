from django.shortcuts import redirect
from django.views import View


class TodoView(View):
    all_todos = []

    def post(self, request, *args, **kwargs):
        todo_new = request.POST.get('todo')
        important_new = request.POST.get('important')
        if todo_new not in self.all_todos:
            if important_new == "true":
                self.all_todos.insert(0, todo_new)
            else:
                self.all_todos.append(todo_new)
        return redirect('/')