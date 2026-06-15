from django.shortcuts import render, redirect
from django.views.generic import View
from app1.models import User, Product
from .form import RegisterUserForm
from app1.models import User, Product, Cart


class Search(View):
    def get(self, request):
        user_id = request.session.get("login_user_id")
        user = None
        if user_id:
            user = User.objects.filter(user_id=user_id).first()
        context = {"user": user}                       # ← これが無いと {% if user %} が常に偽
        return render(request, "app1/main.html", context)


class Login(View):
    def get(self, request):
        return render(request, "app1/login.html")

    def post(self, request):
        user_id = request.POST.get("user_id")
        password = request.POST.get("password")
        user = User.objects.filter(user_id=user_id, password=password).first()
        if user is None:
            context = {"error": "会員IDまたはパスワードが違います。"}
            return render(request, "app1/login.html", context)
        request.session["login_user_id"] = user.user_id   
        return redirect("app1:main")


class Logout(View):
    def get(self, request):
        request.session.pop("login_user_id", None)
        return redirect("app1:main")


class Register(View):
    def get(self, request):
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, "app1/registerUser.html", context)


class RegisterConfirm(View):
    def post(self, request):
        form = RegisterUserForm(request.POST)
        if not form.is_valid():
            context = {"form": form}
            return render(request, "app1/registerUser.html", context)
        request.session["register_data"] = form.cleaned_data
        context = {"form": form}
        return render(request, "app1/registerUserConfirm.html", context)

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
        return render(request, "app1/registerUserCommit.html", context)

    def get(self, request):
        return redirect("app1:registerUser")


class UserInfo(View):
    def get(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")
        user = User.objects.get(user_id=user_id)
        context = {"user": user}
        return render(request, "app1/userInfo.html", context)


class SearchResult(View):
    def get(self, request):
        keyword = request.GET.get("keyword", "")
        category = request.GET.get("category", "all")

        products = Product.objects.all()
        if keyword:
            products = products.filter(name__icontains=keyword)
        if category != "all":
            products = products.filter(category_id=category)

        category_names = {"all": "すべて", "1": "鞄", "2": "帽子"}
        category_name = category_names.get(category, "すべて")

        context = {
            "products": products,
            "keyword": keyword,
            "category_name": category_name,
        }
        return render(request, "app1/searchResult.html", context)


class ItemDetail(View):
    def get(self, request, item_id):
        product = Product.objects.get(item_id=item_id)
        context = {"product": product}
        return render(request, "app1/itemDetail.html", context)
    
class ItemDetail(View):
    def get(self, request, item_id):
        product = Product.objects.get(item_id=item_id)
        context = {
            "product": product,
            "quantities": range(1, 11),   
        }
        return render(request, "app1/itemDetail.html", context)

class AddToCart(View):
    def post(self, request, item_id):
        user_id = request.session.get("login_user_id")

        if not user_id:
            return redirect("app1:login")

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            request.session.pop("login_user_id", None)
            return redirect("app1:login")

        product = Product.objects.get(item_id=item_id)
        amount = int(request.POST.get("amount", 1))
        Cart.objects.create(user=user, item=product, amount=amount)

        return redirect("app1:cart")

    def get(self, request, item_id):
        return redirect("app1:itemDetail", item_id=item_id)
    
class CartView(View):
    def get(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")

        user = User.objects.get(user_id=user_id)
        cart_items = Cart.objects.filter(user=user)

        total = 0
        for c in cart_items:
            total += c.item.price * c.amount

        context = {
            "cart_items": cart_items,
            "total": total,
        }
        return render(request, "app1/cart.html", context)
    
class UpdateUser(View):
    def get(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")
        user = User.objects.get(user_id=user_id)
        context = {"user": user}
        return render(request, "app1/updateUser.html", context)
    
class UpdateUserConfirm(View):
    def post(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")

        password = request.POST.get("password")
        checkpassword = request.POST.get("checkpassword")
        name = request.POST.get("name")
        address = request.POST.get("address")

        if password != checkpassword:
            user = User.objects.get(user_id=user_id)
            context = {"user": user, "error": "パスワードが一致しません。"}
            return render(request, "app1/updateUser.html", context)

        request.session["update_data"] = {
            "password": password,
            "name": name,
            "address": address,
        }

        context = {
            "user_id": user_id,
            "password": password,
            "name": name,
            "address": address,
        }
        return render(request, "app1/updateUserConfirm.html", context)

    def get(self, request):
        return redirect("app1:updateUser")
    
class UpdateUserCommit(View):
    def post(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")

        data = request.session.get("update_data")
        if not data:
            return redirect("app1:updateUser")

        user = User.objects.get(user_id=user_id)
        user.password = data["password"]
        user.name = data["name"]
        user.address = data["address"]
        user.save()

        del request.session["update_data"]
        context = {"user": user}                      
        return render(request, "app1/updateUserCommit.html", context)

    def get(self, request):
        return redirect("app1:updateUser")
    
class WithdrawConfirm(View):
    def get(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")

        user = User.objects.filter(user_id=user_id).first()
        if user is None:
            request.session.pop("login_user_id", None)
            return redirect("app1:login")

        context = {"user": user}
        return render(request, "app1/withdrawConfirm.html", context)
    
class WithdrawCommit(View):
    def post(self, request):
        user_id = request.session.get("login_user_id")
        if not user_id:
            return redirect("app1:login")

        user = User.objects.filter(user_id=user_id).first()
        name = ""
        if user is not None:
            name = user.name         
            user.delete()

        request.session.pop("login_user_id", None)
        context = {"name": name}
        return render(request, "app1/withdrawCommit.html", context)

    def get(self, request):
        return redirect("app1:withdrawConfirm")