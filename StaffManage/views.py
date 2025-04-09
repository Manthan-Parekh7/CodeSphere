from django.shortcuts import render
from .models import Assignment
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
# Create your views here.


def dashboard(request):
    # add catched assignments
    assignments = Assignment.objects.all()
    return render(request, 'StaffManage/dashboard.html', {'assignments': assignments})


def add_assignment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        Assignment.objects.create(
            title=title, description=description, due_date=due_date)
    return redirect('dashboard')


def delete_assignment(request, assig_id):
    assignment = get_object_or_404(Assignment, assig_id=assig_id)
    assignment.delete()
    return redirect('dashboard')
