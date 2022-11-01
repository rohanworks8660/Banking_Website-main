# sys.path defines paths from which imports can be made

from sqlalchemy import null
from profiles.models import Customer_Data, Account_Data, Transactions, ECS_Data, Bills
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
import sys
import random

sys.path.append(os.getcwd()+'/profiles/utils')
import Classes

# Stores customer obj
cur_customer = None


# Create your views here.


def randomGen():
    # return a 6 digit random number
    return int(random.uniform(100000, 999999))


def display_menu(request):
    global cur_customer
    user_log_in = Classes.Login_Details(
        request.user.username, request.user.password)
    # Check if customer is a new or existing customer
    cust_details = Customer_Data.objects.filter(Name=user_log_in.username)
    print("cust_details", cust_details)
    if (cust_details):
        print("Existing Customer")
        customer = Classes.Customer(user_log_in)
        print("customer obj", customer)
    else:
        print("Making New Customer")
        customer = Classes.New_Customer(
            user_log_in, user_log_in.username, '9999999999', 'saa@gmail.com')
    print("Customer name:", customer.customer_data.Name)
    cur_customer = customer
    return render(request, 'profiles/user_account.html', {'customer': customer})


def account_management(request):
    accounts = cur_customer.accounts
    user_accnos = list(accounts.keys())
    print("user_accnos", user_accnos)
    return render(request, 'profiles/account_details.html', {'customer': cur_customer, 'accounts': accounts, 'can_close_accnos': user_accnos})


def withdraw(request):
    accounts = cur_customer.accounts
    accnnnnno = int(list(cur_customer.accounts.keys())[0])
    msg = "<br>Enter a valid account no. and also check for ur balance!</p><br>"
    if request.method == "POST":
        acc_num = int(request.POST.get('acc_no'))
        amount = int(request.POST.get('amount'))
        print('requestPOST=', acc_num, type(acc_num))
        #print('account dict:',accounts.keys())
        if acc_num in accounts:
            #acc_obj= accounts[acc_num]
            acc_q = Account_Data.objects.get(Accno=acc_num)
            balance = acc_q.Balance
            print("balance:", balance)
            if (balance >= amount):
                trans = Classes.Account(acc_q)
                trans.create_transaction(amount, "withdraw")
                balance -= amount
                acc_q.Balance = balance
                print("balance:", acc_q.Balance)
                acc_q.save()
                cur_customer.accounts[acc_num].account_details.Balance -= amount
                msg = "<td>Withdrawn Successfully!</td><br>"
            else:
                msg = "<td>Not sufficient balance!</td><br>"
        else:
            msg = "<p>Invalid account number</p><br>"
    return render(request, 'profiles/withdraw.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'accnnnnno': accnnnnno})


def deposit(request):
    accounts = cur_customer.accounts
    acccno = int(list(cur_customer.accounts.keys())[0])
    msg = "<br>Enter a valid account no. and also check for ur balance!</p><br>"
    if request.method == "POST":
        acc_num = int(request.POST.get('acc_no'))
        amount = int(request.POST.get('amount'))
        print('requestPOST=', acc_num, type(acc_num))
        if acc_num in accounts:
            acc_q = Account_Data.objects.get(Accno=acc_num)
            balance = acc_q.Balance
            print("balance:", balance)
            trans = Classes.Account(acc_q)
            trans.create_transaction(amount, "deposit")
            balance += amount
            acc_q.Balance = balance
            print("balance:", acc_q.Balance)
            acc_q.save()
            cur_customer.accounts[acc_num].account_details.Balance += amount
            msg = "<td>Deposited Successfully!</td><br>"
        else:
            msg = "<p>Invalid account number</p><br>"
    return render(request, 'profiles/deposit.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'acccno': acccno})


def stat_gen(request):
    accounts = cur_customer.accounts
    print(accounts)
    msg = ""
    all_transactions = {}
    for acc in accounts:
        print("acc_no:", acc)
        acc_q = Account_Data.objects.get(Accno=int(acc))
        trans = Classes.Account(acc_q)
        transaction = trans.get_transaction_log()
        trans_objs_list = list(transaction.values())
        all_transactions[acc] = all_transactions.get(acc, [])+trans_objs_list
        print("trans:", transaction)
    return render(request, 'profiles/stat_gen.html', {'customer': cur_customer, 'accounts': accounts, 'transaction': all_transactions, 'msg': msg})


def get_transaction_action(request):
    accounts = cur_customer.accounts
    print("got:", request.GET)
    msg = "filter"
    button_action = request.GET['account_action']
    all_transactions = {}
    if (button_action == 'withdraw'):
        for acc in accounts:
            transaction = Transactions.objects.filter(
                Accno_id=int(acc), Type="withdraw")
            print("withdraw:", transaction)
            all_transactions[acc] = list(transaction)
    elif (button_action == 'deposit'):
        for acc in accounts:
            transaction = Transactions.objects.filter(
                Accno_id=int(acc), Type="deposit")
            all_transactions[acc] = list(transaction)
    elif (button_action == 'all'):
        return redirect('profiles:stat_gen')
    print("all_trans:", all_transactions)
    return render(request, 'profiles/stat_gen.html', {'customer': cur_customer, 'accounts': accounts, 'transaction': all_transactions, 'msg': msg})


def get_function_chosen(request):
    print(request.GET)
    #print("Got menu")
    menu_chosen = request.GET['function_chosen']
    if (menu_chosen == 'view_accounts'):
        # name of view given in urls.py
        return redirect('profiles:account_management')
    elif (menu_chosen == 'withdraw'):
        return redirect('profiles:withdraw')  # name of view given in urls.py
    elif (menu_chosen == 'deposit'):
        return redirect('profiles:deposit')  # name of view given in urls.py
    elif (menu_chosen == 'stat_gen'):
        return redirect('profiles:stat_gen')  # name of view given in urls.py
    elif (menu_chosen == 'money_transfer'):
        return redirect('profiles:money_transfer')


def get_account_action(request):
    print("got:", request.GET)
    account_action = request.GET['account_action']
    # err_msg=""
    if (account_action == 'create'):
        if (cur_customer.accounts):
            pass  # pop up
        else:
            cur_customer.create_account()
    elif (account_action == 'close'):
        print(request.GET)
        print("account:", cur_customer.accounts)
        close_accno = int(request.GET['close_accno'])
        cur_customer.close_account(close_accno)
    else:
        print("Got neither create nor close")
    return redirect('profiles:account_management')

def money_transfer(request):
    acccno = int(list(cur_customer.accounts.keys())[0])
    return render(request, "profiles/transfer.html", {"acccno": acccno})


