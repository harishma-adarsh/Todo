
# from datetime import datetime
# from django.utils import timezone   
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Task

# def task_list(request):
#     tasks = Task.objects.all()
#     pending_count = Task.objects.filter(completed=False).count()
#     today = timezone.now().date()
#     return render(request, 'todo/task_list.html', {
#         "tasks": tasks,
#         "pending_count": pending_count,
#         "today": today
#     })

# def add_task(request):
#     if request.method == "POST":
#         title = request.POST.get('title')
#         due_date = request.POST.get('due_date')  # New line to get due_date
#         if title:
#             Task.objects.create(title=title, due_date=due_date)  # Save due_date
#         return redirect('task_list')
#     return render(request, 'todo/add_task.html')

# def update_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)

#     if request.method == "POST":
#         task.title = request.POST.get('title')

#         due_date_str = request.POST.get('due_date')
#         if due_date_str:
#             try:
#                 task.due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
#             except ValueError:
#                 task.due_date = None
#         else:
#             task.due_date = None

#         task.completed = 'completed' in request.POST
#         task.save()
#         return redirect('task_list')
#     return render(request, 'todo/update_task.html', {'task': task})

# def delete_task(request, task_id):
#     task = get_object_or_404(Task, id=task_id)
#     if request.method == "POST":
#         task.delete()
#         return redirect('task_list')
#     return render(request, 'todo/delete_task.html', {'task': task})
# #

from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Task

def task_list(request):
    # Order tasks: completed first, then pending, both ordered by position
    tasks = Task.objects.all().order_by('completed', 'position')
    pending_count = Task.objects.filter(completed=False).count()
    today = timezone.now().date()
    
    return render(request, 'todo/task_list.html', {
        "tasks": tasks,
        "pending_count": pending_count,
        "today": today
    })


def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        due_date_str = request.POST.get('due_date', '').strip()

        # Validate title - prevent null/empty values
        if not title:
            messages.error(request, "Task title is required and cannot be empty.")
            return redirect('add_task')
        
        if len(title) < 3:
            messages.error(request, "Task title must be at least 3 characters long.")
            return redirect('add_task')

        # Validate due date - prevent null/empty values
        if not due_date_str:
            messages.error(request, "Due date is required and cannot be empty.")
            return redirect('add_task')
        
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            # ✅ Validation: disallow past dates
            if due_date < timezone.now().date():
                messages.error(request, "Due date cannot be before today.")
                return redirect('add_task')
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('add_task')

        try:
            Task.objects.create(title=title, due_date=due_date)
            messages.success(request, f"Task '{title}' has been created successfully!")
        except Exception as e:
            messages.error(request, f"Error creating task: {str(e)}")
            return redirect('add_task')
        
        return redirect('task_list')

    today = timezone.now().date()
    return render(request, 'todo/add_task.html', {"today": today})

def save_order(request):
    if request.method == "POST":
        order = request.POST.get("order")  # e.g. "3,1,2"
        if order:
            order_list = order.split(",")
            for pos, task_id in enumerate(order_list):
                task = get_object_or_404(Task, id=int(task_id))
                task.position = pos
                task.save()
    return redirect("task_list")

def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        
        # Validate title - prevent null/empty values
        if not title:
            messages.error(request, "Task title is required and cannot be empty.")
            return redirect('update_task', task_id=task.id)
        
        if len(title) < 3:
            messages.error(request, "Task title must be at least 3 characters long.")
            return redirect('update_task', task_id=task.id)
        
        task.title = title

        due_date_str = request.POST.get('due_date', '').strip()
        
        # Validate due date - prevent null/empty values
        if not due_date_str:
            messages.error(request, "Due date is required and cannot be empty.")
            return redirect('update_task', task_id=task.id)
        
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
            # ✅ Validation: disallow past dates
            if due_date < timezone.now().date():
                messages.error(request, "Due date cannot be before today.")
                return redirect('update_task', task_id=task.id)
            task.due_date = due_date
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('update_task', task_id=task.id)

        task.completed = 'completed' in request.POST
        
        try:
            task.save()
            messages.success(request, f"Task '{title}' has been updated successfully!")
        except Exception as e:
            messages.error(request, f"Error updating task: {str(e)}")
            return redirect('update_task', task_id=task.id)
        
        return redirect('task_list')

    today = timezone.now().date()
    return render(request, 'todo/update_task.html', {'task': task, "today": today})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/delete_task.html', {'task': task})
