from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
import datetime
import io
from xhtml2pdf import pisa
from django.urls import reverse
from .models import CustomUser, Car, Rental, Transaction, ContactMessage
from .forms import CustomUserCreationForm, CustomUserLoginForm, RentalForm, AddBalanceForm, AdminCarForm
from datetime import date, timedelta
from django.shortcuts import get_object_or_404, redirect
# from .utils import render_to_pdf


def is_admin(user):
    """Check if the user is an admin"""
    return user.is_superuser

# Authentication Views
def signup_view(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main_app/signup.html', {'form': form})

def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = CustomUserLoginForm()
    return render(request, 'main_app/login.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out',extra_tags="auth")
    return redirect('login')

# Car Listing Views
def home_view(request):
    """Home page with first page of car listings"""
    # Check for rentals that should be returned today
    Rental.check_returns()
    
    cars = Car.objects.all()
    # Paginator--A Django helper class for splitting data into pages.
    paginator = Paginator(cars, 9)  # 9 cars per page
    page_obj = paginator.get_page(1)
    
    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages,
        'current_page': 1
    }
    return render(request, 'main_app/home.html', context)

def car_list_view(request, page=1):
    """View for paginated car listings"""
    cars = Car.objects.all()
    paginator = Paginator(cars, 9)  # 9 cars per page (except last page might have 8)
    page_obj = paginator.get_page(page)
    
    context = {
        'page_obj': page_obj,
        'total_pages': paginator.num_pages,
        'current_page': page
    }
    return render(request, 'main_app/home.html', context)


@login_required
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if Rental.objects.filter(user=request.user, is_active=True).exists():
                messages.error(request, 'You already have an active rental',extra_tags="rental-already-active")
                return redirect('car_detail', car_id=car.id)
    # even we have marked the unavailable cars as disbale to rent in the home view
    # but since backend must always validate the state, therefore we check again
    if not car.available:
        messages.error(request, "This car is not available for rent.",extra_tags="rental-not-available")
        return redirect('car_detail', car_id=car.id)

    if request.method == 'POST':
        try:
            days = int(request.POST.get('days'))
            if days < 1:
                messages.error(request, "Rental duration must be at least 1 day.",extra_tags="rental-duration-error")
                return redirect('car_detail', car_id=car.id)
        except (TypeError, ValueError):
            messages.error(request, "Invalid number of days.",extra_tags="invalid-days-error")
            return redirect('car_detail', car_id=car.id)
        
        user = request.user
        start_date = date.today()
        end_date = start_date + timedelta(days=days - 1)
        total_cost = car.rent_per_day * days

        if not user.has_sufficient_balance(total_cost):
            messages.error(request, "Insufficient balance to rent this car.",extra_tags="rental-insufficient-balance")
            return redirect('car_detail', car_id=car.id)

        # Deduct and create rental
        user.balance -= total_cost
        user.save()

        car.mark_unavailable()

        Rental.objects.create(
            user=user,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
            is_active=True
        )

        Transaction.objects.create(
            user=request.user,
            amount=total_cost,
            transaction_type='PAYMENT',
            description=f'Rented {car.name} for {days} day(s)'
        )

        messages.success(request, f'You have successfully rented {car.name} for {days} day(s).',extra_tags="rental-success")
        return redirect('rental_history')

        
    # below-- here is a safe fallback for non-POST requests like if the user directly visits the URL
    # or is the user refreshing the page without submitting the form
    return redirect('car_detail', car_id=car.id)

@login_required
def car_detail_view(request, car_id):
    """Detail view for a specific car"""
    car = get_object_or_404(Car, id=car_id)
    
    # Handle rental form submission
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # pin_code = form.cleaned_data['pin_code']
            
            # # Validate PIN code
            # if pin_code != request.user.pin_code:
            #     messages.error(request, 'Invalid PIN code')
            #     return redirect('car_detail', car_id=car.id)
            
            # Check if user already has an active rental
            if Rental.objects.filter(user=request.user, is_active=True).exists():
                messages.error(request, 'You already have an active rental')
                return redirect('car_detail', car_id=car.id)
            
            # Check if car is available
            if not car.available:
                messages.error(request, 'This car is no longer available')
                return redirect('car_detail', car_id=car.id)
            
            # Calculate rental costz
            days = (end_date - start_date).days + 1
            total_cost = car.rent_per_day * days
            
            # Check if user has sufficient balance
            if request.user.balance < total_cost:
                messages.error(request, f'Insufficient balance. You need ${total_cost}')
                return redirect('car_detail', car_id=car.id)
            
            # Process rental
            try:
                # Create rental record
                rental = Rental.objects.create(
                    user=request.user,
                    car=car,
                    start_date=start_date,
                    end_date=end_date,
                    total_cost=total_cost,
                    is_active=True
                )
                
                # Update user balance
                request.user.balance -= total_cost
                request.user.save()
                
                # Record transaction
                Transaction.objects.create(
                    user=request.user,
                    amount=total_cost,
                    transaction_type='PAYMENT',
                    description=f'Rental of {car.name} from {start_date} to {end_date}'
                )
                
                # Mark car as unavailable
                car.mark_unavailable()
                
                messages.success(request, 'Car rented successfully!')
                return redirect('rental_history')
            except Exception as e:
                messages.error(request, f'Error processing rental: {str(e)}')
                return redirect('car_detail', car_id=car.id)
    else:
        # Set default rental dates (today and tomorrow)
        today = timezone.now().date()
        tomorrow = today + datetime.timedelta(days=1)
        form = RentalForm(initial={'start_date': today, 'end_date': tomorrow})
    
    context = {
        'car': car,
        'form': form
    }
    return render(request, 'main_app/car_detail.html', context)

# view to return a rented car if the rental period is not over
# when the rental period is over, the car will be automatically returned
@login_required
def return_car(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id, user=request.user)

    if not rental.is_active:
        messages.warning(request, "This car rental is already completed.")
        return redirect('profile',extra_tags="already-completed-rental")

    rental.is_active = False
    rental.save()

    rental.car.mark_available()

    messages.success(request, f"You have successfully returned {rental.car.name}.",extra_tags="returned-by-user")
    return redirect('profile')

# User Account Views
@login_required
def profile_view(request):
    """User profile page"""
    user = request.user
    # since a button is already provided in the profile.html to view the rental history
    # therefore, no need to pass active_rentals here
    
    # Handle add balance form
    if request.method == 'POST':
        form = AddBalanceForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
                user.add_balance(amount)
                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    transaction_type='ADD',
                    description='Added to wallet'
                )
                messages.success(request, f'${amount} added to your balance',extra_tags="amount-added-to-wallet")
                return redirect('profile')
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = AddBalanceForm()
    
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'main_app/profile.html', context)

@login_required
def rental_history_view(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-created_at')
    today = timezone.now().date()
    return render(request, 'main_app/rental_history.html', {
        'rentals': rentals,
        'today': today
    })

@login_required
def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at') # this minus sign before "created_at" will sort the transactions in descending order
    return render(request, 'main_app/transaction_history.html', {'transactions': transactions})








# Now the admin views start here



@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_cars = Car.objects.count()
    total_users = CustomUser.objects.filter(is_superuser=False).count()
    active_rentals = Rental.objects.filter(is_active=True).count()
    
    context = {
        'total_cars': total_cars,
        'total_users': total_users,
        'active_rentals': active_rentals,
    }
    return render(request, 'main_app/admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def admin_customer_report(request):
    users = CustomUser.objects.filter(is_superuser=False)
    customers_data = []

    for user in users:
        total_rentals = Rental.objects.filter(user=user).count()
        completed_rentals = Rental.objects.filter(user=user, is_active=False)
        current_rental = Rental.objects.filter(user=user, is_active=True).first()
        total_spent = sum(rental.total_cost for rental in completed_rentals)

        customers_data.append({
            'username': user.username,
            'full_name': f"{user.first_name} {user.last_name}",
            'total_rentals': total_rentals,
            'completed_rentals': completed_rentals.count(),
            'total_spent': total_spent,
            'current_car': current_rental.car.name if current_rental else "No current rental"
        })

    return render(request, 'main_app/admin/customer_report.html', {
        'customers_data': customers_data
    })

@login_required
@user_passes_test(is_admin)
def pdf_customer_report(request):
    """Generate PDF customer report"""
    users = CustomUser.objects.filter(is_superuser=False)
    user_data = []
    
    for user in users:
        active_rentals = Rental.objects.filter(user=user, is_active=True)
        past_rentals = Rental.objects.filter(user=user, is_active=False)
        
        user_data.append({
            'user': user,
            'active_rentals': active_rentals,
            'past_rentals': past_rentals,
            'total_spent': sum(rental.total_cost for rental in past_rentals)
        })
    
    context = {
        'user_data': user_data,
        'timestamp': timezone.now()
    }
    
    return render_to_pdf('main_app/admin/pdf_customer_report.html', context)

def render_to_pdf(template_src, context_dict):
    """Helper function to generate PDF from HTML template"""
    template = render_to_string(template_src, context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(template.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error generating PDF', status=400)

@login_required
@user_passes_test(is_admin)
def admin_reserved_cars_report(request):
    """Admin view for reserved cars report"""
    rentals = Rental.objects.filter(is_active=True).order_by('end_date')
    return render(request, 'main_app/admin/reserved_cars_report.html', {'rentals': rentals})

@login_required
@user_passes_test(is_admin)
def pdf_reserved_cars_report(request):
    """Generate PDF of currently reserved (active) cars"""
    reserved_cars = Car.objects.filter(available=False)
    active_reservations = []

    for car in reserved_cars:
        rental = Rental.objects.filter(car=car, is_active=True).select_related('user').first()
        if rental:
            active_reservations.append(rental)

    context = {
        'active_reservations': active_reservations,
        'total_active_reservations': len(active_reservations),
        'now': timezone.now()
    }

    return render_to_pdf('main_app/admin/pdf_reserved_cars_report.html', context)

@login_required
@user_passes_test(is_admin)
def admin_add_car(request):
    """Admin view to add a new car using Django Form (with image upload)"""
    if request.method == 'POST':
        form = AdminCarForm(request.POST, request.FILES)  # handle text + file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Car added successfully!',extra_tags="car-added-successfully")
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminCarForm()

    return render(request, 'main_app/admin/add_car.html', {'form': form})

# admin_car_list--for removing car_list_view
# this view recives both GET and POST requests
# GET--to show the list of cars 
# POST--to delete selected cars
@login_required
@user_passes_test(is_admin)
def admin_car_list(request):
    if request.method == 'POST':
        car_ids = request.POST.getlist('car_ids')
        deleted_count = 0

        for car_id in car_ids:
            car = get_object_or_404(Car, id=car_id)
            if car.available or not Rental.objects.filter(car=car, is_active=True).exists():
                car.delete()
                deleted_count += 1
            else:
                messages.warning(request, f'Car "{car.name}" is currently rented and was not removed.',extra_tags='car-can-not-be-removed')
                  
        if deleted_count:
            messages.success(request, f'{deleted_count} car(s) removed successfully.',extra_tags='car-removed-successfully')
        return redirect('admin_car_list')

    cars = Car.objects.all()
    return render(request, 'main_app/admin/admin_car_list.html', {'cars': cars})

# Contact Us View
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            return render(request, 'main_app/contact_us.html', {
                'error': "All fields are required."
            })

        # Save message
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Simple redirect with query param
        
        return redirect(reverse('contact_us') + '?success=true')
    return render(request, 'main_app/contact_us.html')

