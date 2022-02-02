from django.http import request
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import *
from datetime import date,time
from datetime import datetime,timedelta
from .form import *
from pytz import timezone
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        if int(request.user.MealBill) > 0 or request.user.permission==True:
            morinig_meal=Morning_Meal.objects.all()
            afternoon_meal=Afternoon_Meal.objects.all()
            denar_meal=Denar_Meal.objects.all()
            appstortitel=Meal_Order.objects.filter(Roll__icontains=request.user,Date_Time=date.today()+timedelta(days=1))
            notice=Notice.objects.all()
            titel=''
            for i in notice:
                titel = titel +i.Titel
            appstor=appstortitel
            Odate=date.today()+timedelta(days=1)
            now = datetime.now()
            bd = timezone('Asia/Dhaka')
            current_time = str(datetime.now(bd).strftime('%H-%M-%S'))
            now_time=datetime.now(bd).time()
            print(now_time)
            print(type(now_time))
            if str(now_time) >= '21:01:00.000':
                fine(request)
            sendv={
                "morning":morinig_meal,
                "afternoon":afternoon_meal,
                "denar":denar_meal,
                "todyfood":appstor,
                'titel':titel,
                "current_time":current_time,
                "date":Odate
                
            }
            return render(request,"index.html",sendv)
        return redirect(billnotice)
    return redirect(login)

def login(request):
    email=request.POST.get("email")
    passw=request.POST.get("password")
    if request.method=="POST":
       user=auth.authenticate(username=email,password=passw)
       if user is not None:
            auth.login(request,user)
            return redirect(index) 
       else:
            return render(request,"login.html",{'error':"Invalide User Password"})
    return render(request,"login.html")
def logout(request):
    auth.logout(request)
    return redirect(index)
def mealorder(request):
    '''Oname=request.POST.get("name")
    Owhen=request.POST.get("when")
    Oprice=request.POST.get("price")
    Oqun=request.POST.get("Quantity")
    Oid=request.POST.get("id")
    Odate=date.today()+timedelta(days=1)
    print(Oname,Oprice,Oqun,Oid,Odate)
    if request.method=="POST":
        order=Meal_Order(Name=request.user.first_name + request.user.last_name,Roll=request.user,When=Owhen,Room_Number=request.user.profilupdate.Room_Number,Hostel=request.user.profilupdate.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
        allorder=All_Meal_Order(Name=request.user,When=Owhen,Hostel=request.user.profilupdate.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
        order.save()
        allorder.save()
        return redirect(index)'''
    '''if request.method=="POST":
        Odate=date.today()+timedelta(days=1)
        try:
            t =Meal_Order.objects.get(Roll=request.user,Date_Time=Odate)
            t.Available = aval
            t.save()
            return render(request,"add.html",{'error':"User already exists"})
        except User.DoesNotExist:
            pass'''
    return redirect(index)
def confirm(request,id):
    if request.user.is_authenticated:
        if int(request.user.MealBill) > 0 or request.user.permission==True:
            qun=request.POST.get("qun")
            qunt=int(qun)
            if request.method=="POST":
                Oname=request.POST.get("name")
                Owhen=request.POST.get("when")
                Oprice=request.POST.get("price")
                Oqun=qun
                Oid=id
                Odate=date.today()+timedelta(days=1)
                try:
                    order=Meal_Order.objects.get(Roll=request.user,When="Breakfast",Date_Time=Odate)
                    order.Name+','+Oname
                    order.Price = int(order.Price) + int(Oprice)
                    order.Quantity = int(order.Quantity) + int(Oqun)
                    order.save()
                except Meal_Order.DoesNotExist:
                    order=Meal_Order(Name=request.user.first_name + request.user.last_name,Roll=request.user,When=Owhen,Room_Number=request.user.Room_Number,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    allorder=All_Meal_Order(Name=request.user,When=Owhen,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    order.save()
                    allorder.save()
                pk=Morning_Meal.objects.filter(pk=id)
            #Price counter Meal####################
                for i in pk:
                    name=i.Name
                    dam=i.Price
                    fid=i.id
                    when=i.When
                price=int(dam)*qunt
            #Available Meal####################
                for i in pk:
                    ava=i.Available
                    aval=int(ava)-int(qunt)
                t = Morning_Meal.objects.get(id=id)
                t.Available = aval
                t.save()
                try:
                    Odate=date.today()+timedelta(days=1)
                    t =Demo.objects.get(Roll=request.user,Date_Time=Odate)
                    t.Break_qun = t.Break_qun + qunt
                    t.Break = t.Break +","+ Oname
                    t.Break_price = t.Break_price + price
                    t.save()
                except Demo.DoesNotExist:
                    order=Demo(Name=request.user.first_name + request.user.last_name,Roll=request.user,Hostel=request.user.Hostel,Room_Number=request.user.Room_Number,Break_qun=1,Break=Oname,Break_price=price,Date_Time=Odate)
                    order.save()
            #Meal Bill################################
                mealbillMinus=CastomUser.objects.filter(username=request.user)
                for i in mealbillMinus:
                    mealardam=i.MealBill
                    dam=int(mealardam)-int(price)
                mealbill=CastomUser.objects.get(username=request.user)
                mealbill.MealBill = dam
                mealbill.save()
            return redirect(index)
        return redirect(billnotice)
    return redirect(login)
def confirmlunch(request,id):
    if request.user.is_authenticated:
        if int(request.user.MealBill) > 0 or request.user.permission==True:
            qun=request.POST.get("qun")
            qunt=int(qun)
            if request.method=="POST":
                Oname=request.POST.get("name")
                Owhen=request.POST.get("when")
                Oprice=request.POST.get("price")
                Oqun=qun
                Oid=id
                Odate=date.today()+timedelta(days=1)
                try:
                    order=Meal_Order.objects.get(Roll=request.user,When="Lunch",Date_Time=Odate)
                    order.Name+','+Oname
                    order.Price = int(order.Price) + int(Oprice)
                    order.Quantity = int(order.Quantity) + int(Oqun)
                    order.save()
                except Meal_Order.DoesNotExist:
                    order=Meal_Order(Name=request.user.first_name + request.user.last_name,Roll=request.user,When=Owhen,Room_Number=request.user.Room_Number,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    allorder=All_Meal_Order(Name=request.user,When=Owhen,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    order.save()
                    allorder.save()
                
                pk=Afternoon_Meal.objects.filter(pk=id)
            #Price counter Meal####################
                for i in pk:
                    name=i.Name
                    dam=i.Price
                    fid=i.id
                    when=i.When
                price=int(dam)*qunt
            #Available Meal####################
                for i in pk:
                    ava=i.Available
                    aval=int(ava)-int(qunt)
                t = Afternoon_Meal.objects.get(id=id)
                t.Available = aval
                t.save()
                try:
                    Odate=date.today()+timedelta(days=1)
                    t =Demo.objects.get(Roll=request.user,Date_Time=Odate)
                    t.Lunch_qun = t.Lunch_qun + qunt
                    t.Lunch = t.Lunch +","+ Oname
                    t.Lunch_price = t.Lunch_price + price
                    t.save()
                except Demo.DoesNotExist:
                    order=Demo(Name=request.user.first_name + request.user.last_name,Roll=request.user,Hostel=request.user.Hostel,Room_Number=request.user.Room_Number,Lunch_qun=1,Lunch=Oname,Lunch_price=price,Date_Time=Odate)
                    order.save()
            #Meal Bill################################
                mealbillMinus=CastomUser.objects.filter(username=request.user)
                for i in mealbillMinus:
                    mealardam=i.MealBill
                    dam=int(mealardam)-int(price)
                mealbill=CastomUser.objects.get(username=request.user)
                mealbill.MealBill = dam
                mealbill.save()
            return redirect(index)
        return redirect(billnotice)
    return redirect(login)
def confirmdener(request,id):
    if request.user.is_authenticated:
        if int(request.user.MealBill) > 0 or request.user.permission==True:
            qun=request.POST.get("qun")
            qunt=int(qun)
            if request.method=="POST":
                Oname=request.POST.get("name")
                Owhen=request.POST.get("when")
                Oprice=request.POST.get("price")
                Oqun=qun
                Oid=id
                Odate=date.today()+timedelta(days=1)

                try:
                    order=Meal_Order.objects.get(Roll=request.user,When="Dinner",Date_Time=Odate)
                    order.Name+','+Oname
                    order.Price = int(order.Price) + int(Oprice)
                    order.Quantity = int(order.Quantity) + int(Oqun)
                    order.save()
                except Meal_Order.DoesNotExist:
                    order=Meal_Order(Name=request.user.first_name + request.user.last_name,Roll=request.user,When=Owhen,Room_Number=request.user.Room_Number,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    allorder=All_Meal_Order(Name=request.user,When=Owhen,Hostel=request.user.Hostel,Food_Name=Oname,Food_ID=Oid,Price=Oprice,Quantity=Oqun,Date_Time=Odate)
                    order.save()
                    allorder.save()
                pk=Denar_Meal.objects.filter(pk=id)
            #Price counter Meal####################
                for i in pk:
                    name=i.Name
                    dam=i.Price
                    fid=i.id
                    when=i.When
            #Available Meal####################
                for i in pk:
                    ava=i.Available
                    aval=int(ava)-int(qunt)
                t = Denar_Meal.objects.get(id=id)
                t.Available = aval
                t.save()
                price=int(dam)*qunt
                try:
                    Odate=date.today()+timedelta(days=1)
                    t =Demo.objects.get(Roll=request.user,Date_Time=Odate)
                    t.Denar_qun = t.Denar_qun + qunt
                    t.Denar = t.Denar +","+ Oname
                    t.Denar_price = t.Denar_price + price
                    t.save()
                except Demo.DoesNotExist:
                    order=Demo(Name=request.user.first_name + request.user.last_name,Roll=request.user,Hostel=request.user.Hostel,Room_Number=request.user.Room_Number,Denar_qun=1,Denar=Oname,Denar_price=price,Date_Time=Odate)
                    order.save()
                #Meal Bill################################
                mealbillMinus=CastomUser.objects.filter(username=request.user)
                for i in mealbillMinus:
                    mealardam=i.MealBill
                    dam=int(mealardam)-int(price)
                mealbill=CastomUser.objects.get(username=request.user)
                mealbill.MealBill = dam
                mealbill.save()
            return redirect(index)
        return redirect(billnotice)
    return redirect(login)

def singup(request):
    if request.user.is_superuser:
        f_name=request.POST.get("f_name")
        l_name=request.POST.get("l_name")
        email=request.POST.get("email")
        passw=request.POST.get("password")
        cpassw=request.POST.get("confirmpassword")
        bio=request.POST.get("bio")
        hostel=request.POST.get("hostel")
        room=request.POST.get("room")
        if request.method=="POST":
            if passw==passw:
                try:
                    user=CastomUser.objects.get(username=email)
                    return render(request,"add.html",{'error':"User already exists"})  
                except CastomUser.DoesNotExist:
                    user=CastomUser.objects.create_user(username=email,password=cpassw,first_name=f_name,last_name=l_name,StudentName=f_name+" "+l_name,Numer=bio,Hostel=hostel,Room_Number=room,Class_Roll=email)
                    return render(request,"add.html",{'success':"user created successfully"})    
            else:
                return render(request,"add.html") 
        return render(request,"add.html")
    return redirect(index) 


def profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html')
    return redirect(login)

def updateprofile(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            #ufrom=UserForm(request.POST,instance=request.user)
            pfrom=ProForm(request.POST,request.FILES,instance=request.user)
            if pfrom.is_valid():
                #ufrom.save()
                pfrom.save()
                return render(request,"profile.html",{"error":"Profile Update successfully"})
        else:
            #ufrom=UserForm(instance= request.user)
            pfrom=ProForm(instance=request.user)
            return render(request,"updateprofile.html",{"profrom":pfrom})
    else:
        return redirect(login)

def Alluser(request):

    return render(request,"updateprofile.html")

def panelhed(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            morinig_meal=Morning_Meal.objects.all()
            afternoon_meal=Afternoon_Meal.objects.all()
            denar_meal=Denar_Meal.objects.all()
            today=date.today()+timedelta(days=1)
            #morning
            breakfast1=[]
            count1=[]
            for i in morinig_meal:
                breakfast1.append(i.Name)
            for i in breakfast1:
                hostel1=Meal_Order.objects.filter(Hostel=1,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel1:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count1.append(order1)
    

            
            #AfterNooon
            lunch1=[]
            lcount1=[]
            for i in afternoon_meal:
                lunch1.append(i.Name)
            for i in lunch1:
                hostel1=Meal_Order.objects.filter(Hostel=1,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel1:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount1.append(order1)
            for i in lcount1:
                print(i)

            #Diner
            diner1=[]
            dcount1=[]
            for i in denar_meal:
                diner1.append(i.Name)
                print(i.Name)
            for i in diner1:
                hostel1=Meal_Order.objects.filter(Hostel=1,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel1:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount1.append(order1)
            
            


            #morning
            breakfast2=[]
            count2=[]
            for i in morinig_meal:
                breakfast2.append(i.Name)
                print(i.Name)
            for i in breakfast2:
                hostel2=Meal_Order.objects.filter(Hostel=2,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel2:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count2.append(order1)
            
            
            #AfterNooon
            lunch2=[]
            lcount2=[]
            for i in afternoon_meal:
                lunch2.append(i.Name)
                print(i.Name)
            for i in lunch2:
                hostel2=Meal_Order.objects.filter(Hostel=2,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel2:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount2.append(order1)
            


            #Diner
            diner2=[]
            dcount2=[]
            for i in denar_meal:
                diner2.append(i.Name)
                print(i.Name)
            for i in diner2:
                hostel2=Meal_Order.objects.filter(Hostel=2,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel2:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount2.append(order1)
            

            

            #morning
            breakfast3=[]
            count3=[]
            for i in morinig_meal:
                breakfast3.append(i.Name)
                print(i.Name)
            for i in breakfast3:
                hostel3=Meal_Order.objects.filter(Hostel=3,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel3:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count3.append(order1)
            
            
            #AfterNooon
            lunch3=[]
            lcount3=[]
            for i in afternoon_meal:
                lunch3.append(i.Name)
                print(i.Name)
            for i in lunch3:
                hostel3=Meal_Order.objects.filter(Hostel=3,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel3:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount3.append(order1)
            
            

            #Diner
            diner3=[]
            dcount3=[]
            for i in denar_meal:
                diner3.append(i.Name)
                print(i.Name)
            for i in diner3:
                hostel3=Meal_Order.objects.filter(Hostel=3,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel3:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount3.append(order1)
            
            
            

            #morning
            breakfast4=[]
            count4=[]
            for i in morinig_meal:
                breakfast4.append(i.Name)
                print(i.Name)
            for i in breakfast4:
                hostel4=Meal_Order.objects.filter(Hostel=4,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel4:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count4.append(order1)
            
            

            
            #AfterNooon
            lunch4=[]
            lcount4=[]
            for i in afternoon_meal:
                lunch4.append(i.Name)
                print(i.Name)
            for i in lunch4:
                hostel4=Meal_Order.objects.filter(Hostel=4,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel4:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount4.append(order1)
            
            


            #Diner
            diner4=[]
            dcount4=[]
            for i in denar_meal:
                diner4.append(i.Name)
                print(i.Name)
            for i in diner4:
                hostel4=Meal_Order.objects.filter(Hostel=4,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel4:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount4.append(order1)
            
            



            #morning
            breakfast5=[]
            count5=[]
            for i in morinig_meal:
                breakfast5.append(i.Name)
                print(i.Name)
            for i in breakfast5:
                hostel5=Meal_Order.objects.filter(Hostel=5,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel5:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count5.append(order1)
            
            

            
            #AfterNooon
            lunch5=[]
            lcount5=[]
            for i in afternoon_meal:
                lunch5.append(i.Name)
                print(i.Name)
            for i in lunch5:
                hostel5=Meal_Order.objects.filter(Hostel=5,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel5:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount5.append(order1)
            
            

            #Diner
            diner5=[]
            dcount5=[]
            for i in denar_meal:
                diner5.append(i.Name)
                print(i.Name)
            for i in diner5:
                hostel5=Meal_Order.objects.filter(Hostel=5,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel5:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount5.append(order1)
            

            #morning
            breakfast6=[]
            count6=[]
            for i in morinig_meal:
                breakfast6.append(i.Name)
                print(i.Name)
            for i in breakfast6:
                hostel6=Meal_Order.objects.filter(Hostel=6,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel6:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count6.append(order1)
            
            #AfterNooon
            lunch6=[]
            lcount6=[]
            for i in afternoon_meal:
                lunch6.append(i.Name)
                print(i.Name)
            for i in lunch6:
                hostel6=Meal_Order.objects.filter(Hostel=6,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel6:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount6.append(order1)

            #Diner
            diner6=[]
            dcount6=[]
            for i in denar_meal:
                diner6.append(i.Name)
                print(i.Name)
            for i in diner6:
                hostel6=Meal_Order.objects.filter(Hostel=6,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel6:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount6.append(order1)
            

            #morning
            breakfast7=[]
            count7=[]
            for i in morinig_meal:
                breakfast7.append(i.Name)
                print(i.Name)
            for i in breakfast7:
                hostel7=Meal_Order.objects.filter(Hostel=7,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel7:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                count7.append(order1)
            
            #AfterNooon
            lunch7=[]
            lcount7=[]
            for i in afternoon_meal:
                lunch7.append(i.Name)
                print(i.Name)
            for i in lunch7:
                hostel7=Meal_Order.objects.filter(Hostel=7,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel7:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                lcount7.append(order1)

            #Diner
            diner7=[]
            dcount7=[]
            for i in denar_meal:
                diner7.append(i.Name)
                print(i.Name)
            for i in diner7:
                hostel7=Meal_Order.objects.filter(Hostel=7,Food_Name=i,Date_Time=today)
                mealname=i
                qun=0
                for i in hostel7:
                    qun +=int(i.Quantity)
                order1=mealname,qun
                dcount7.append(order1)

            sendvar={
                
                'breakfast1':breakfast1,
                "count1":count1,
                "lunch1":lunch1,
                "lcount1":lcount1,
                "diner1":diner1,
                "dcount1":dcount1,

                'breakfast2':breakfast2,
                "count2":count2,
                "lunch2":lunch2,
                "lcount2":lcount2,
                "diner2":diner2,
                "dcount2":dcount2,

                'breakfast3':breakfast3,
                "count3":count3,
                "lunch3":lunch3,
                "lcount3":lcount3,
                "diner3":diner3,
                "dcount3":dcount3,

                'breakfast4':breakfast4,
                "count4":count4,
                "lunch4":lunch4,
                "lcount4":lcount4,
                "diner4":diner4,
                "dcount4":dcount4,

                'breakfast5':breakfast5,
                "count5":count5,
                "lunch5":lunch5,
                "lcount5":lcount5,
                "diner5":diner5,
                "dcount5":dcount5,

                'breakfast6':breakfast6,
                "count6":count6,
                "lunch6":lunch6,
                "lcount6":lcount6,
                "diner6":diner6,
                "dcount6":dcount6,

                'breakfast7':breakfast7,
                "count7":count7,
                "lunch7":lunch7,
                "lcount7":lcount7,
                "diner7":diner7,
                "dcount7":dcount7,

            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
def mealsheet(request,id):
        hostelNo=id
        order=Demo.objects.filter(Hostel=hostelNo,Date_Time=date.today())
        sortorder=order.order_by("Room_Number")
        sendvar={
        'sortorder':sortorder, 
        'hostelNo':hostelNo,
        }
        return render(request,"mealsheet.html",sendvar)
def delete(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            pk=Meal_Order.objects.get(pk=id)
            pk.delete()
            return redirect(panelhed)
    return redirect(login)
def mealhiostry(request):
    allmeal=All_Meal_Order.objects.filter(Name__icontains=request.user)
    sendvar={
        "allmeal":allmeal
    }
    return render(request,"allmeal.html",sendvar)
'''#hostel##################################
def hostelmeal1(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=1)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal2(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=2)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal3(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=3)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal4(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=4)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal5(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=5)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal6(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=6)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)
#hostel##################################
def hostelmeal7(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            allorder=Meal_Order.objects.filter(Hostel=7)
            sendvar={
                "meal":allorder,
            }
            return render(request,"panelhed.html",sendvar)
        return redirect(index)
    return redirect(login)'''

def hostelmealsearch(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method=="POST":
                search=request.POST.get("searchmel")
                searchhoste=request.POST.get("searchhost")
                searchwhen=request.POST.get("when")
                appstortitel=Meal_Order.objects.filter(Food_Name__icontains=search,Hostel__icontains=searchhoste,When=searchwhen)
                appstor=appstortitel
                countsiam=0
                for i in appstor:
                    countsiam +=int(i.Quantity)
                sendvar={
                'apppost':appstor,
                "countsiam":countsiam,
                }
                return render(request,"serchmeal.html",sendvar)
        return redirect(index)
    return redirect(login)

def mealsearch(request):
    if request.method=="POST":
        search=request.POST.get("findman")
        findman=Meal_Order.objects.filter(Name__icontains=search)
        sendvar={
            "find":findman
                }
    return render(request,"findman.html",sendvar)

def notice(request):
    notice=Notice.objects.get()
    sendvar={
        'notice':notice
    }
    return render(request,"notice.html",sendvar)

def billnotice(request):
    return render(request,"billnotice.html")

def setting(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            newpass=request.POST.get("password")
            u = User.objects.get(username=request.user)
            u.set_password(newpass)
            u.save()
            return render(request,"setting.html",{"succes":"Password Update Successfully"})
        return render(request,"setting.html")
    return redirect(login)

def makepayment(request):
    if request.user.is_superuser:
        if request.method=="POST":
            day=date.today()
            userrol=request.POST.get('userroll')
            fixed=request.POST.get('fixed')
            food=request.POST.get('food')
            pleedge=request.POST.get('pleedge')
            development=request.POST.get('development')
            amount=request.POST.get('amount')
            try:
                search=CastomUser.objects.get(Class_Roll=userrol)
                Name=search.StudentName
                Mobile=search.Numer
                search.MealBill = int(search.MealBill) + int(amount)
                search.save()
                paynow=Payment_History(User=userrol,Mobile=Mobile,Name=Name,Fixed=fixed,Food=food,Pledge=pleedge,Development=development,Amount=amount,Receiver=request.user,Date=day)
                paynow.save()
                return render(request,"makepament.html",{"Success":"Payment Complete"})
            except CastomUser.DoesNotExist:
                return render(request,"makepament.html",{"error":"Student Not Exitst "})
        return render(request,"makepament.html")
    return redirect(index)
def paymenthistory(request):
    payhistory=Payment_History.objects.filter(User=request.user.Class_Roll)
    sendvar={
        "payhistory":payhistory
    }
    return render(request,"pymenthostory.html",sendvar)
def Usersearch(request):
    userlist=CastomUser.objects.all()
    sendvar={
        'userlist':userlist
    }
    return render(request,"Usersearch.html",sendvar)
def student(request,id):
    if request.user.is_superuser:
        if request.method=="POST":
            pk=CastomUser.objects.get(pk=id)
            p_u_from=AllUser(request.POST,request.FILES,instance=pk)
            if p_u_from.is_valid():
                p_u_from.save()
                return redirect(Usersearch)
        else:
            pk=CastomUser.objects.get(pk=id)
            p_u_from=AllUser(instance=pk)
        return render(request,"studentlist.html",{"p_u_from":p_u_from})
    if request.user.hostel_incharje is True:
        if request.method=="POST":
            pk=CastomUser.objects.get(pk=id)
            p_u_from=Hostel(request.POST,request.FILES,instance=pk)
            if p_u_from.is_valid():
                p_u_from.save()
                return render(request,"studentlist.html",{"p_u_from":p_u_from})
        else:
            pk=CastomUser.objects.get(pk=id)
            p_u_from=Hostel(instance=pk)
        return render(request,"studentlist.html",{"p_u_from":p_u_from})
    return redirect(index)
def Alluser(request):
    if request.user.is_authenticated:
        getuser=request.POST.get('username')
        if request.method=="POST":
            prmition=CastomUser.objects.get(Class_Roll=getuser)
            return render(request,"Allusers.html",{"prmition":prmition})

def fine(request):
    fine=CastomUser.objects.all()
    for i in fine:
        if i.Leave==False:
            try:
                find=Fine_Count.objects.get(Student_Name=i.Class_Roll,When="Breakfast",Date=date.today())
            except Fine_Count.DoesNotExist:
                try:
                    getfine=Meal_Order.objects.get(Roll=i.Class_Roll,When="Breakfast",Date_Time=date.today())
                except Meal_Order.DoesNotExist:
                    i.MealBill=int(i.MealBill)-3
                    i.save()
                    fine=Fine_Count(Student_Name=i.Class_Roll,Fine_amount=3,When="Breakfast",Date=date.today())
                    fine.save()

            try:
                find=Fine_Count.objects.get(Student_Name=i.Class_Roll,When="Lunch",Date=date.today())
            except Fine_Count.DoesNotExist:
                try:
                    getfine=Meal_Order.objects.get(Roll=i.Class_Roll,When="Lunch",Date_Time=date.today())
                except Meal_Order.DoesNotExist:
                    i.MealBill=int(i.MealBill)-3
                    i.save()
                    fine=Fine_Count(Student_Name=i.Class_Roll,Fine_amount=3,When="Lunch",Date=date.today())
                    fine.save()

            try:
                find=Fine_Count.objects.get(Student_Name=i.Class_Roll,When="Dinner",Date=date.today())
            except Fine_Count.DoesNotExist:
                try:
                    getfine=Meal_Order.objects.get(Roll=i.Class_Roll,When="Dinner",Date_Time=date.today())
                except Meal_Order.DoesNotExist:
                    i.MealBill=int(i.MealBill)-3
                    i.save()
                    fine=Fine_Count(Student_Name=i.Class_Roll,Fine_amount=3,When="Dinner",Date=date.today())
                    fine.save()
        
    return redirect(index)