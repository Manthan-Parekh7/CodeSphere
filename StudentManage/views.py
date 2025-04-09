import os
import json
import subprocess
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from urllib.parse import quote
from HomePageAuth.models import Profile
from StaffManage.models import Assignment
from .models import CodeFile


@login_required
def home(request):
    # Fetch the logged-in user's profile
    profile = Profile.objects.get(user=request.user)
    assignments = Assignment.objects.all()

    return render(request, "StudentManage/home.html", {"profile": profile, 'files': CodeFile.objects.all(), 'student': request.user, 'assignments': assignments})
    # return render(request, 'StudentManage/home.html', {'files': CodeFile.objects.all(), 'student': request.user})


def upload_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        subject = request.POST.get('subject')
        file = request.FILES.get('file')
        CodeFile.objects.create(
            file_name=file_name, subject=subject, file=file, student=request.user)
    return redirect('home')


def delete_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id)
    file.delete()
    return redirect('home')


def download_file(request, file_id):
    file = get_object_or_404(CodeFile, id=file_id)
    file_path = file.file.path
    file_name = file.file_name
    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(
                f.read(), content_type="application/force-download")
            response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
            return response
    except FileNotFoundError:
        raise Http404("File not found")


def view_file(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    file_path = file_obj.file.path
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
            return render(request, 'StudentManage/view_file.html', {'file': file_obj, 'content': file_content})
    except FileNotFoundError:
        raise Http404("File not found")


def editor(request, file_id):
    file_obj = get_object_or_404(CodeFile, id=file_id)
    file_path = file_obj.file.path
    try:
        with open(file_path, 'r') as f:
            file_content = f.read()
            return render(request, 'StudentManage/editor.html', {'file': file_obj, 'content': file_content})
    except FileNotFoundError:
        raise Http404("File not found")


@csrf_exempt
def save_code(request, file_id):
    if request.method == "POST":
        file_obj = get_object_or_404(CodeFile, id=file_id)
        try:
            data = json.loads(request.body)
            new_code = data.get("code", "")
            file_path = file_obj.file.path
            with open(file_path, "w", encoding="utf-8") as f:  # ✅ Explicit encoding added
                f.write(new_code)
            return JsonResponse({"success": True, "message": "Code saved successfully!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})


@csrf_exempt
def run_code(request, file_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            language = data.get("language")
            code = data.get("code")
            custom_input = data.get("input", "")

            file_extension = {
                "python": "py",
                "c": "c",
                "cpp": "cpp",
                "javascript": "js"
            }.get(language, None)

            if not file_extension:
                return JsonResponse({"output": "Unsupported language"})

            file_name = f"temp.{file_extension}"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(code)

            command = []
            if language == "python":
                command = ["python", file_name]
            elif language == "c":
                output_file = "temp.out"
                compile_command = ["gcc", file_name, "-o", output_file]
                compile_result = subprocess.run(
                    compile_command, capture_output=True, text=True)
                if compile_result.stderr:
                    return JsonResponse({"output": compile_result.stderr})
                command = ["./" + output_file]
            elif language == "cpp":
                output_file = "temp.out"
                compile_command = ["g++", file_name, "-o", output_file]
                compile_result = subprocess.run(
                    compile_command, capture_output=True, text=True)
                if compile_result.stderr:
                    return JsonResponse({"output": compile_result.stderr})
                command = ["./" + output_file]
            elif language == "javascript":
                command = ["node", file_name]

            result = subprocess.run(
                command, input=custom_input, text=True, capture_output=True)

            output = result.stdout if result.stdout else result.stderr

            # Cleanup
            os.remove(file_name)
            if language in ["c", "cpp"] and os.path.exists("temp.out"):
                os.remove("temp.out")

            return JsonResponse({"output": output})

        except Exception as e:
            return JsonResponse({"output": str(e)})

    return JsonResponse({"output": "Invalid request method"})
