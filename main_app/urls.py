from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Car listing URLs
    path('', views.home_view, name='home'),
    path('cars/page/<int:page>/', views.car_list_view, name='car_list'),
    path('cars/<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('cars/<int:car_id>/rent/', views.rent_car, name='rent_car'),
    path('return/<int:rental_id>/', views.return_car, name='return_car'),


    
    # User account URLs
    path('profile/', views.profile_view, name='profile'),
    path('rental-history/', views.rental_history_view, name='rental_history'),
    path('contact/', views.contact_us, name='contact_us'),

    # Admin URLs
    path('dashboard/admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/customer-report/', views.admin_customer_report, name='admin_customer_report'),
    path('dashboard/admin/reserved-cars/', views.admin_reserved_cars_report, name='admin_reserved_cars_report'),
     # PDF report URLs
    path('dashboard/admin/customer-report/pdf/', views.pdf_customer_report, name='pdf_customer_report'),
    path('dashboard/admin/reserved-cars/pdf/', views.pdf_reserved_cars_report, name='pdf_reserved_cars_report'),

    path('dashboard/admin/add-car/', views.admin_add_car, name='admin_add_car'),
    path('dashboard/admin/remove-cars/', views.admin_car_list, name='admin_car_list'),

   
]