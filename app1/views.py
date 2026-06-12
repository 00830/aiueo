from django.shortcuts import render, redirect
from django.views.generic import View
from app1.models import User
from .form import RegisterUserForm


class Search(View):
    def get(self, request):
        return render(request, "app1/main.html")


class Login(View):
    def get(self, request):
        return render(request, "app1/login.html")


class Register(View):
    def get(self, request):
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "app1/registerUser.html", context)   # 大文字Uに


class RegisterConfirm(View):
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, "app1/registerUser.html", context)
        request.session["register_data"] = form.cleaned_data
        context = {"form": form}
        return render(request, "app1/registerUserConfirm.html", context)  # 指定名に

    def get(self, request):
        return redirect("app1:registerUser")


class RegisterComplete(View):
    def post(self, request):
        data = request.session.get("register_data")
        if not data:
            return redirect("app1:registerUser")
        user = User()
        user.user_id = data["user_id"]
        user.password = data["password"]
        user.name = data["name"]
        user.address = data["address"]
        user.save()
        name = data["name"]
        del request.session["register_data"]
        context = {"name": name}
        return render(request, "app1/registerUserCommit.html", context)   # complete → Commit

    def get(self, request):
        return redirect("app1:registerUser")