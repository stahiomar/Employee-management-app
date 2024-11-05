from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum, Avg, Count
from datetime import date
from django.contrib.auth import update_session_auth_hash
from decimal import Decimal

def evaluateEmployees(request):
    today = date.today()
    message = "Evaluation should be done only on 30/06/YYYY."
    
    if today.day == 30 and today.month == 6:
        message = "Evaluation done."
        
        if request.method == 'POST':
            employees = Employee.objects.annotate(not_justified_absence_count=Count('absence', filter=Absence.objects.filter(state="not justified"))).filter(not_justified_absence_count__lt=3)
            
            for employee in employees:
                employee.salary *= Decimal('1.1')
                employee.save()

    employees = Employee.objects.all()
    
    return render(request, 'project/allEmp.html', {'msg': message, 'employees': employees})

def home(request):
    countEmp = Employee.objects.count()
    countRes = Responsable.objects.count()
    sumSalariesEmp = Employee.objects.aggregate(sum=Sum('salary')).get('sum') or 0  # Set to 0 if sum is None
    sumSalariesRes = Responsable.objects.aggregate(sum=Sum('salary')).get('sum') or 0  # Set to 0 if sum is None
    sumTotal = sumSalariesEmp + sumSalariesRes
    avgSalaries = round(sumTotal / (countEmp + countRes), 2) if countEmp + countRes > 0 else 0  # Calculate average if count is greater than 0, otherwise set to 0
    return render(request, "project/home.html", {
        "countEmp": countEmp,
        "countRes": countRes,
        "sumSalaries": round(sumTotal, 2),  # Round to 2 decimal places
        "avgSalaries": avgSalaries,
    })


def empPage(request):    
    return render(request, 'project/empInfos.html')

def about(request):    
    return render(request, "project/about.html")

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
    return render(request, 'project/contact.html')

def hello(request):    
    return render(request, "project/hello.html")

def table(request):
    employees = Employee.objects.all()
    return render(request, 'project/allEmp.html', {'employees': employees})

def adminLogout(request):
    logout(request)
    return redirect('hello')

def addEmployee(request):
    profession = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    age = models.DecimalField(max_digits=6, decimal_places=0, null=True)
    
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        e_mail = request.POST['email']
        ad = request.POST['adresse']
        pr = request.POST['profession']
        gen = request.POST['gender']
        a = request.POST['age']
        sal = request.POST['salary']
        co = request.POST['code']
        # Create a new User object
        user = User.objects.create_user(username=e_mail, password=co)

        # Create the Employee object and associate it with the User object
        new_employee = Employee.objects.create(user=user, firstname=fn, lastname=ln, email=e_mail, adresse=ad, salary=sal, code=co, profession=pr, 
         gender=gen, age=a)

        return render(request, "project/addEmployee.html")

    return render(request, "project/addEmployee.html")

def showEmpInfos(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    absences = Absence.objects.filter(emp=employee)

    if request.method == "POST":
        # Retrieve the updated information from the form
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        desc = request.POST.get('description')

        # Update the employee object with the new information
        employee.firstname = firstname
        employee.lastname = lastname
        employee.email = email
        employee.adresse = adresse
        employee.description = desc
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            employee.picture = profile_image

        # Save the updated employee object
        employee.save()

        # Update the user's credentials
        user = employee.user
        user.username = email
        user.save()

        # Re-authenticate the user to update the session
        updated_user = authenticate(request, username=email, password=user.password)
        auth_login(request, updated_user)
        update_session_auth_hash(request, updated_user)

        return redirect('showEmpInfos', employee_id=employee_id)

    return render(request, "project/empInfos.html", {'employee': employee, 'absences': absences})

def empLogout(request):
    logout(request)
    return redirect('hello')

@login_required
def editEmpInfos(request):
    employee = request.user.employee
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        
        employee.firstname = firstname
        employee.lastname = lastname
        employee.email = email
        
        employee.save()

        user = employee.user
        user.username = email

        return redirect('showEmpInfos')
        user.save()
    return render(request, 'project/editEmpInfos.html', {'employee': employee})

def removeEmployee(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')
        try:
            user = User.objects.get(username=email)
            employee = Employee.objects.get(user=user, code=code)
            employee.user.delete()  # Remove the associated user
            employee.delete()
            message = 'Employee removed successfully.'            
            return render(request, 'project/removeEmployee.html', {'message': message})

        except (User.DoesNotExist, Employee.DoesNotExist, Responsable.DoesNotExist):
            message = 'User not found.'
        try:
            user = User.objects.get(username=email)
            responsable = Responsable.objects.get(user=user, code=code)
            responsable.user.delete()  # Remove the associated user
            responsable.delete()
            message = 'Responsible removed successfully.'
            
            return render(request, 'project/removeEmployee.html', {'message': message})

        except (User.DoesNotExist, Employee.DoesNotExist, Responsable.DoesNotExist):
            message = 'User not found.'

            return render(request, 'project/removeEmployee.html', {'message': message})
    return render(request, 'project/removeEmployee.html')

def responsablePage(request):
    countFor = Formation.objects.count()
    countEmp = Employee.objects.count()
    count = Employee.objects.filter(formation__isnull=False).count()
    avgSalaries = Employee.objects.aggregate(avg=Avg('salary')).get('avg')
    return render(request, "project/responsablePage.html",
           {'formation_emp':count,'count_formation':countFor,'count_emp':countEmp,'avg':round(avgSalaries,2)})

def addResponsable(request):
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        e_mail = request.POST['email']
        sal = request.POST['salary']
        co = request.POST['code']

        user = User.objects.create_user(username=e_mail, password=co)

        new_responsable = Responsable.objects.create(user=user, firstname=fn, lastname=ln, email=e_mail, salary=sal,  code=co)

        return render(request, "project/addResponsable.html")

    return render(request, "project/addResponsable.html")

def addFormation(request):
    if request.method == "POST":
        n = request.POST['name']
        dur = request.POST['duration']
        
        new_formation = Formation.objects.create(name=n, duration=dur)
        
        
    return render(request, "project/addFormation.html")

def editEmp(request, employee_id):
    employee = Employee.objects.get(id=employee_id)

    if request.method == "POST":
        salary = request.POST.get('salary')
        code = request.POST.get('code')
        formation_id = request.POST.get('formation')
        absence_state = request.POST.get('state')
        absence_date = request.POST.get('date')
        employee.salary = salary
        employee.code = code
        employee.formation_id = formation_id
        employee.save()

        if absence_state and absence_date:
            absence = Absence.objects.create(state=absence_state, date=absence_date, emp=employee)
            employee.absence = absence
            employee.save()

    return render(request, "project/editEmp.html", {
        "employee": employee,
        "formations": Formation.objects.all(),
        "absences": Absence.objects.all(),
    })


    formations = Formation.objects.all()
    return render(request, 'project/editEmp.html', {'employee': employee, 'formations': formations})

def responsableLogout(request):
    logout(request)
    return redirect('hello')

def searchEmp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('code')

        try:
            user = User.objects.get(username=email)
            employee = Employee.objects.get(user=user, code=code)
            # Employee exists, perform any necessary actions or redirection here
            return redirect('editEmp', employee_id=employee.id)
        except (User.DoesNotExist, Employee.DoesNotExist):
            error_message = 'Employee not found.'
            return render(request, 'project/searchEmp.html', {'error_message': error_message})

    return render(request, 'project/searchEmp.html')

from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the values in the form are 'admin' and 'admin'
        if username == 'admin@gmail.com' and password == 'admin':
            # Redirect to the admin page
            return redirect('home')

        # Check if the values exist in the Employee table
        try:
            # Try to authenticate the user using email as the username
            user = User.objects.get(username=username)
            employee = Employee.objects.get(user=user)
            if user.check_password(password):
                # If authentication is successful, log in the employee
                auth_login(request, user)
                return redirect('showEmpInfos', employee_id=employee.id)
        except (User.DoesNotExist, Employee.DoesNotExist):
            pass

        # Check if the values exist in the Responsable table
        try:
            # Try to authenticate the user using email as the username
            user = User.objects.get(username=username)
            responsable = Responsable.objects.get(user=user)
            if user.check_password(password):
                # If authentication is successful, log in the responsable
                auth_login(request, user)
                return redirect('responsablePage')
        except (User.DoesNotExist, Responsable.DoesNotExist):
            pass

        # If none of the above conditions match, show an error message
        error_message = "Invalid username or password."
        return render(request, 'project/login.html', {'error_message': error_message})

    return render(request, 'project/login.html')
