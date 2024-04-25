from django.shortcuts import render,redirect    
from .forms import ExpenseForm
from .models import Expense
from django.db.models import Sum
import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'expense/home.html')

@login_required
def index(request):
    if request.method == "POST":
        expense = ExpenseForm(request.POST)
        if expense.is_valid():
            expense.save()
            return redirect('expense:index')
    
    
    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))
    
    expense_form = ExpenseForm()
    return render(request,'expense/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses})

@login_required
def list_expenses(request):

    expenses = Expense.objects.all()
    total_expenses = expenses.aggregate(Sum('amount'))

    #logic to calculate 365 days expenses
    last_year = datetime.date.today() - datetime.timedelta(days=365)
    data = Expense.objects.filter(date__gt=last_year)
    yearly_sum = data.aggregate(Sum('amount'))

    #logic to calculate 30 days expenses
    last_month = datetime.date.today() - datetime.timedelta(days=30)
    data = Expense.objects.filter(date__gt=last_month)
    monthly_sum = data.aggregate(Sum('amount'))

    #logic to calculate 7 days expenses
    last_week = datetime.date.today() - datetime.timedelta(days=7)
    data = Expense.objects.filter(date__gt=last_week)
    weekly_sum = data.aggregate(Sum('amount'))

    return render(request,'expense/list_expenses.html',{'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum})

@login_required
def charts(request):
    expenses = Expense.objects.all()
    daily_sums = Expense.objects.filter().values('date').order_by('date').annotate(sum=Sum('amount'))
    categorical_sums = Expense.objects.filter().values('category').order_by('category').annotate(sum=Sum('amount'))
    return render(request,'expense/charts.html',{'expenses':expenses,'daily_sums':daily_sums,'categorical_sums':categorical_sums})

@login_required
def edit(request,id):
    expense = Expense.objects.get(id=id)
    expense_form = ExpenseForm(instance=expense)
    if request.method == "POST":
        
        expense = Expense.objects.get(id=id)
        form = ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            expense.save()
            return redirect('expense:index')
    return render(request,'expense/edit.html',{'expense_form':expense_form})

@login_required
def delete(request,id):
    if request.method == "POST" and 'delete' in request.POST:
        expense = Expense.objects.get(id=id)
        expense.delete()
    return redirect('expense:list_expenses')