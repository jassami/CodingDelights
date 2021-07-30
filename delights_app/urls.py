from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('cupcakes', views.cupcakes),
    path('tarts', views.tarts),
    path('cookies', views.cookies),
    path('all', views.all),
    path('<int:user_id>', views.user_account),
    path('cupcakes/<int:cupcake_id>', views.cupcake),
    path('tarts/<int:tart_id>', views.tart),
    path('cookies/<int:cookie_id>', views.cookie),
    path('add_delight/<int:delight_id>', views.add_delight),
    path('check_out', views.check_out),
    path('update', views.update),
    path('logout', views.logout),
    path('order', views.order),
    path('place_order/<int:order_id>', views.place_order),
    path('review/<int:delight_id>', views.review),
    path('rate/<int:delight_id>', views.rate),
    path('edit/<int:delight_id>', views.edit),
    path('remove/<int:delight_id>', views.remove),
] 
