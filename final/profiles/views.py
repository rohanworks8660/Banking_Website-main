# sys.path defines paths from which imports can be made



from sqlalchemy import null
from profiles.models import Customer_Data, Account_Data, Transactions, UserInfo
from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
import sys
import random
import mysql.connector as sql

sys.path.append(os.getcwd()+'/profiles/utils')
# Stores customer obj
import Classes
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
    user_dets = UserInfo.objects.get(username=user_log_in.username)
    print("cust_details", user_dets.phone_number)
    if (cust_details):
        print("Existing Customer")
        customer = Classes.Customer(user_log_in)
        print("customer obj", customer)
    else:
        print("Making New Customer")
        customer = Classes.New_Customer(
            user_log_in, user_log_in.username, user_dets.phone_number, user_dets.email_address)
    print("Customer name:", customer.customer_data.Name)
    cur_customer = customer
    if (cur_customer.accounts):
            pass  # pop up
    else:
        cur_customer.create_account()
    name = user_dets.first_name+" "+user_dets.fathers_name+" "+user_dets.last_name
    return render(request, 'profiles/user_account.html', {'customer': customer, "user_dets": user_dets, "name": name})


def account_management(request):
    accounts = cur_customer.accounts
    user_accnos = list(accounts.keys())
    print("user_accnos", user_accnos)
    return render(request, 'profiles/account_details.html', {'customer': cur_customer, 'accounts': accounts, 'can_close_accnos': user_accnos})


def withdraw(request):
    accounts = cur_customer.accounts
    accnnnnno = int(list(cur_customer.accounts.keys())[0])
    acc_num = accnnnnno
    msg = ""
    if request.method == "POST":

        try:
            amount = int(request.POST.get('amount'))
        except:
            msg += "<br>Please Enter a valid amount"
            return render(request, 'profiles/withdraw.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'accnnnnno': accnnnnno})
        print('request POST=', acc_num, type(acc_num))
        if acc_num in accounts:
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
            msg += "<p>Invalid account number</p><br>"
    return render(request, 'profiles/withdraw.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'accnnnnno': accnnnnno})


def deposit(request):
    accounts = cur_customer.accounts
    acccno = int(list(cur_customer.accounts.keys())[0])
    msg = ""
    if request.method == "POST":
        acc_num = acccno

        try:
            amount = int(request.POST.get('amount'))
        except  :
            msg+="<br>Please Enter a valid amount"
            return render(request, 'profiles/deposit.html', {'customer': cur_customer, 'accounts': accounts, 'msg': msg, 'acccno': acccno})

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


# to acc and from acc shld not be same
# from acc --- withdraw-transfer
# to acc ----- deposit-transfer
# add buttons

def money_transfer(request):
    to_accno=0
    amount1=0
    msg=""
    acccno = int(list(cur_customer.accounts.keys())[0])
    #global amount1,to_accno
    if request.method == "POST":
        if(type(request.POST.get('accc_no'))=="int"):
            to_accno = int(request.POST.get('accc_no'))
        else:
            msg="<br> Enter valid 'To Account' No "
        if(type(request.POST.get('amount'))=="int"):
            amount1 = int(request.POST.get('amount'))
        else:
            msg+="<br>Please Enter the valid amount"
        obj1=sql.connect(host="localhost", user="root", passwd="root", database='bank_db', auth_plugin='mysql_native_password')
        cursor1=obj1.cursor()
        c1="select * from account"
        cursor1.execute(c1)
        t=list(cursor1.fetchall())
        l1,l2,l3=[],[],[]
        for i in range(len(t)):
            l1.append(t[i][0])
            l2.append(t[i][1])
            l3.append(t[i][2])
        to_acc=to_accno
        amount=amount1
        from_acc=acccno
        print(from_acc,to_accno,amount1)

        if from_acc in l1 and to_acc in l1:
            f=l1.index(from_acc)
            t=l1.index(to_acc)
            if l2[f]>=amount:
                l2[f]=l2[f]-amount
                l2[t]+=amount
                print("Amount transferred successfully")
                cursor2=obj1.cursor()
                cursor3=obj1.cursor()
                c1="UPDATE account SET balance={} where accno= {};".format(l2[f],l1[f])
                cursor2.execute(c1)
                obj1.commit()

                c2="UPDATE account SET balance={} where accno= {};".format(l2[t],l1[t])
                cursor3.execute(c2)
                obj1.commit()
                msg+="<br>Transaction Successfull"
            else:
                print("Insufficient funds")
                msg+="<br>Insufficient Balance"
        return render(request,"profiles/transfer.html",{"msg":msg,"acccno":acccno})
    return render(request, "profiles/transfer.html",{"acccno":acccno})
