from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as Login,logout as Logout
from django.contrib.auth.models import User
from django.contrib import messages


from datetime import datetime

from django.http import HttpResponse


from .models import TodoList,Task


def main(request):
    return render(request, "main.html", {})



def login(request):
    return render(request, "login.html", {"error": False})




def loadTodoLists(user):
    todo_lists = TodoList.objects.filter(user=user)
    if todo_lists:
        data = [{
            'id': i.id,
            "title":i,
            "user":i.user,
            "created_at":i.created_at
        } for i in todo_lists]
        return data
    return []

def app(request):
    previewsURL = request.META.get('HTTP_REFERER', None)
    print(previewsURL)
    if not request.user.is_authenticated and previewsURL.find("login") == -1 and previewsURL.find("app") == -1:
        return redirect('../login/')
    
    try:
        username = request.POST.get("username")
        password = request.POST.get("password")
        

        
        user = authenticate(request,username=username,password=password)
        
        if (user is not None):
            
            # load Todo Lists
            todoLists = loadTodoLists(user)
            
            Login(request, user)
            return render(request, "app.html", {'account': user, 'todoLists': todoLists,"todoListsLen":len(todoLists)})
        else:
            if (request.user.is_authenticated):
                todoLists = loadTodoLists(request.user)
                return render(request, "app.html", {'account': request.user, 'todoLists': todoLists,"todoListsLen":len(todoLists)})
            else:
                return redirect("../login/", {"error": "Please Login Again !"})


    except: 
        return redirect("../app/",{"account":request.user,"messageType":"danger","message":"There is an error! Try again later.","todoLists":loadTodoLists(request.user),"todoListsLen":len(loadTodoLists(request.user))})
    
    # fix daymen to login
        


def register(request):
    
    username = request.POST.get("username")
    gmail = request.POST.get("gmail")
    password = request.POST.get("password")
    re_password = request.POST.get("re_password")
    
    if (not username or not gmail or not password or not re_password):
        return render(request, "register.html", {"error": False})
    
    if (password != re_password):
        return render(request, "register.html", {"error": "Incorrect Password Confermation !"})
    
    try:
        alreadyUser = User.objects.get(username=username)
        if (alreadyUser ):
            return render(request, "register.html", {"error": "Username already used. try another one !"})
    except:
        pass 
    
    
    try:
        alreadyUser = User.objects.get(gmial=gmail)
        if (alreadyUser ):
            return render(request, "register.html", {"error": "Gmail already used. try another one !"})
    except:
        pass 
        

    newAccount = User.objects.create_user(username,gmail,password)
    newAccount.save()
    msg = False 
    if (newAccount):
        msg = "Your account has been created successfully!"
    
    return redirect("../login/", {"error": msg})

    
    
    
def logout(request):
    Logout(request)
    messages.add_message(request,1,"Logout successfully !")
    return redirect("../login/") 
    
    
    
    
def taskView(request, todolistid):
    
    # try:
    testTasks = Task.objects.filter(todoList=todolistid)
    
    return render(request,"task.html",{"show_back":True,"tasks":testTasks, 'tasksLen':len(testTasks), 'todoList': TodoList.objects.get(id=todolistid)})
    # except:
        # return render(request,"base.html", {"show_back":True,"custom_message":"Invalid Task !"}) 



def remove_todo(request, todolistid):
    message = ""
    messageType = 'success'
    try :
        todoList = TodoList.objects.get(id=int(todolistid))
        todoList.delete()
        message = "Todo list removed successfully."
    
    except:
        message = f"Unable to remove todo list #{str(todolistid)}."
        messageType = 'danger'
        
        
    return redirect("../app/", {"account": request.user,"messageType":messageType,"message":message,"todoLists":loadTodoLists(request.user),"todoListsLen":len(loadTodoLists(request.user))})


def add_todo(request):
    
    try:    
        todoListName = request.POST.get("todoListName")
        # alreadyUsed = TodoList.objects.get(title=todoListName)
        # if (alreadyUsed):
        #     return redirect("../app/", {"account": request.user,"messageType":"warning","message":"There is already Todo List with this name ! Try another name."}) 
        newTodoList = TodoList(user=request.user,title=todoListName,created_at=datetime.now())
        newTodoList.save()
        
        return redirect("../app/", {"account": request.user,"messageType":"success","message":"Todo list created successfully.","todoLists":loadTodoLists(request.user),"todoListsLen":len(loadTodoLists(request.user))})
    except:
        return redirect("../app/",{"account":request.user,"messageType":"danger","message":"There is an error! Try again later.","todoLists":loadTodoLists(request.user),"todoListsLen":len(loadTodoLists(request.user))})
    
    
def create_task(request, todolistid):

    try:
        
        text = request.POST.get("content_input")

        newList = Task(todoList=TodoList.objects.get(id=todolistid),content=text,complete=False,created_at=datetime.now())

        newList.save()        
        
    except:

        message = "Unable to add task."
        messageType = 'danger'
        
        return redirect("../app/",{"account":request.user,"messageType":messageType,"message":message,"todoLists":loadTodoLists(request.user),"todoListsLen":len(loadTodoLists(request.user))})
        
        
    return redirect("../task/" + str(todolistid))



def remove_task(request, todolistid, taskid):
    
    try:
        taskToRemove = Task.objects.filter(todoList=todolistid,id=taskid)
        if (taskToRemove):
            taskToRemove.delete()
    except:
        print("Unable to remove the task !")
    
    return redirect(f'../../task/{todolistid}')


def save_task(request, todolistid, taskid):
    # try:
        
    taskToSave = Task.objects.filter(todoList=todolistid,id=taskid)
    if (taskToSave):
        taskToSave.update(complete= not taskToSave[0].complete)
        taskToSave[0].save()
    # except:
        # print("Unable to remove the task !")
    
    return redirect(f'../../task/{todolistid}')


