from django.shortcuts import render, redirect
from .models import Resource
from django.http import HttpResponse 
from django.contrib.auth.models import User 
from django.contrib import messages 
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


###################                             Resource                              ####################

@login_required(login_url="/login/")
def resource(request):
    if request.method == "POST":
        resource_image = request.FILES.get('resources_image')
        resource_name = request.POST.get('resources_name')
        resource_description = request.POST.get('resources_description')
        price = request.POST.get('price')  # Retrieve the price field

        Resource.objects.create(
            user=request.user,
            resource_image=resource_image,
            resource_name=resource_name,
            resource_description=resource_description,
            price=price  # Include the price in the Resource creation
        )
        return redirect('/resource/')
    
    queryset = Resource.objects.all()

    if request.GET.get('search'):
        queryset = queryset.filter(resource_name__icontains=request.GET.get('search'))

    context = {'resources': queryset}
    return render(request, 'resource.html', context)

###################                       Update Resource                              ####################

@login_required(login_url="/login/")
def update_resource(request, id):
    resource = get_object_or_404(Resource, id=id)
    if request.user == resource.user:
      if request.method == "POST":
        resources_image = request.FILES.get('resources_image')
        resources_name = request.POST.get('resources_name')
        resource_description = request.POST.get('resources_description')
        price = request.POST.get('price')

        resource.resource_name = resources_name
        resource.resource_description = resource_description
        resource.price = price

        if resources_image:
            resource.resources_image = resources_image

        resource.save()
        return redirect('/resource/') 

      context = {'resource': resource}
      return render(request, 'update_resource.html', context)
    else:
        # Redirect or display an error message indicating access denied
        return redirect('/resource/')
    
    
###################                       Delete Resource                              ####################

@login_required(login_url="/login/")
def delete_resource(request, id):
    resource = get_object_or_404(Resource, id=id)
    if request.user == resource.user:
        resource.delete()
    return redirect('/resource/')
    # else:
    #     return HttpResponse("You don't have permission to delete this resource.")


###################                       login Page                              ####################

def login_page(request):
        
    if request.method == "POST": 
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, 'Inviald Username')
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)
        
        if user is None:
            messages.info(request, 'Inviald Password')
            return redirect('/login/')
        
        else:
            login(request,user)
            return redirect('/resource/')
        
    return render(request, 'login.html')

###################                       logout Page                              ####################

def logout_page(request):
    logout(request)
    return redirect('/login/') 

###################                       Register                              ####################


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Address

from .models import Customer
def register(request):
    if request.method == "POST":
        # Retrieve user data and address data from the form
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        # Retrieve other user data (password)

        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        # Check if the username already exists
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            messages.info(request, 'Username already taken    ')
            return redirect('/register/')

        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            messages.info(request, 'Email already taken')
            return redirect('/register/')
        
        # user_exists = User.objects.filter(phone_number=phone_number).exists()
        # if user_exists:
        #     messages.info(request, 'Username already taken    ')
        #     return redirect('/register/')

        # Create the User object
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            # Assign other user data
        )
        user.set_password(request.POST.get('password'))
        user.save()
        messages.info(request, 'Account created Successfully')
    
        # customer = Customer.objects.create(user=user)
        customer = Customer(user=user)
        customer.generate_unique_id()  # Generate a unique alphanumeric ID
        customer.save()

     
        # Create the Address object linked to the User
        address = Address.objects.create(
            user=user,
            street=street,
            city=city,
            state=state,
            country=country
        )

        # Redirect to a success page or login page
        return redirect('/login/')

    return render(request, 'register.html')


@login_required(login_url="/login/")
def get_resource(request):
    resources = Resource.objects.all()  # Fetch all resources from the database
    return render(request, 'get_resource.html', {'resources': resources})


def index(request):
    resources = Resource.objects.all()  # Fetch all resources from the database
    return render(request, 'index.html', {'resources': resources})

##########################                         get_resource                         ###########################

def get_resource_page(request):
    return render(request, 'get_resource.html')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Resource

def payment_view(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    user = get_object_or_404(User, id=request.user.id)
    
    return render(request, 'payment.html', {'resource': resource, 'user': user})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Resource

@login_required
def add_resource(request):
    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource_description = request.POST.get('resource_description')
        resource_image = request.FILES.get('resource_image')

        new_resource = Resource.objects.create(
            user=request.user,
            resource_name=resource_name,
            resource_description=resource_description,
            resource_image=resource_image
        )
        # Handle any additional logic after resource creation
        return redirect('resource_detail', resource_id=new_resource.id)
    else:
        # Render your resource creation form here
        # ...
        return render(request, 'add_resource.html')  # Replace 'add_resource.html' with your form template


from django.shortcuts import render, get_object_or_404
from .models import Resource

def payment_view(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    added_by_user = resource.user
    address = get_object_or_404(Address, user=added_by_user)
    customer = get_object_or_404(Customer, user=added_by_user)
    return render(request, 'payment.html', {'resource': resource, 'added_by_user': added_by_user, 'address': address, 'customer': customer})



# payment_app/views.py

# import razorpay
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render

# def initiate_payment(request):
#     if request.method == "POST":
#         amount = int(request.POST["amount"]) * 100  # Amount in paise

#         client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#         payment_data = {
#             "amount": amount,
#             "currency": "INR",
#             "receipt": "order_receipt",
#             "notes": {
#                 "email": "user_email@example.com",
#             },
#         }

#         order = client.order.create(data=payment_data)
        
#         # Include key, name, description, and image in the JSON response
#         response_data = {
#             "id": order["id"],
#             "amount": order["amount"],
#             "currency": order["currency"],
#             "key": settings.RAZORPAY_API_KEY,
#             "name": "Your Company Name",
#             "description": "Payment for Your Product",
#             "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
#         }
        
#         return JsonResponse(response_data)
    
#     return render(request, "payment.html")


# def payment_success(request):
#     return render(request, "payment_success.html")

# def payment_failed(request):
#     return render(request, "payment_failed.html")

# views.py
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Collabrative Farming Plateform",
            "description": "Payment for booking.",
            "image": "https://yourwebsite.com/logo.png",  # Replace with your logo URL
        }
        
        return JsonResponse(response_data)
    
    return render(request, "payment.html")


def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")




