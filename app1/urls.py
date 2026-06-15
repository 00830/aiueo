from django.urls import path
from . import views

app_name = "app1"

urlpatterns = [
    path('search/', views.Search.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('login/register/', views.Register.as_view(), name='registerUser'),
    path('login/register/confirm/', views.RegisterConfirm.as_view(), name='registerUserConfirm'),
    path('login/register/commit/', views.RegisterComplete.as_view(), name='registerUserCommit'),
    path('userinfo/', views.UserInfo.as_view(), name='userInfo'),
    path('searchResult/', views.SearchResult.as_view(), name='searchResult'),
    path('item/<int:item_id>/', views.ItemDetail.as_view(), name='itemDetail'),
    path('item/<int:item_id>/addcart/', views.AddToCart.as_view(), name='addToCart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('updateuser/', views.UpdateUser.as_view(), name='updateUser'),
    path('updateuser/confirm/', views.UpdateUserConfirm.as_view(), name='updateUserConfirm'),
    path('updateuser/commit/', views.UpdateUserCommit.as_view(), name='updateUserCommit'),
    path('withdraw/confirm/', views.WithdrawConfirm.as_view(), name='withdrawConfirm'),
    path('withdraw/commit/', views.WithdrawCommit.as_view(), name='withdrawCommit'),
]