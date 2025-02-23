import tkinter as tk
from tkinter import ttk
import random
import csv
import mysql.connector as con

#Creates a connection to the quizDB database and creates a cursor to execute queries
def create_connection():
    db = con.connect(
        host = "localhost",
        user = "root",
        password = "password",
        database = "quizDB"
    )
    
    cursor = db.cursor()
    
    return cursor,db

#Closes the connection to the database
def close_connection(cursor,db):
    cursor.close()
    db.close()

#Sorts the array of tuples passed in using bubble sort in descending order
def bubble_sort_desc(array):
    n = len(array)
    swapped = True
    while swapped == True:
        swapped = False
        for i in range(0,n-1):
            if array[i][1]<array[i+1][1]:
                array[i],array[i+1] = array[i+1],array[i]
                swapped = True
        n = n-1
    return array

#Opens a connection to the database, executes the sql query using
#the values passed in and closes the connection
def execute_query(sql,values):
    cursor,db = create_connection()
    cursor.execute(sql,values)
    db.commit()
    close_connection(cursor,db)

#Opens a connection to the database, executes the sql query passed in
#,returns the results as a list of tuples and closes the connection
def select_query(sql):
    cursor,db = create_connection()
    cursor.execute(sql)
    results = cursor.fetchall()
    close_connection(cursor,db)
    
    return results

#Destroys the current screen and calls the function for the next screen
def new_screen(currentScreen,newScreenFunction):
    currentScreen.destroy()
    newScreenFunction()

#Creates the first screen
def first_screen():
    screen1 = tk.Tk()
    screen1.title("Sign up/Login")
    screen1.geometry("500x300")
    
    text = tk.Label(screen1,text = "Do you want to sign up or login?")
    text.pack(pady=10)
    
    signup = tk.Button(screen1,text="Sign up",command= lambda: new_screen(screen1,signup_screen)) #"lambda:" is used to prevent immediate execution 
    signup.pack(pady=10)                                                                          #the function                 
     
    login = tk.Button(screen1,text="Login",command= lambda: new_screen(screen1,login_screen))
    login.pack(pady=10)
    
    screen1.mainloop()

#Checks that the length of the password doesn't exceed 20 characters
#and that it isn't empty
def validate_password(password,errorMessage):
    errorMessage.config(text = "",fg = "red")
    valid = True
    if len(password.get()) == 0:
        errorMessage.config(text = "Password cannot be empty",fg = "red")
        valid = False
    elif len(password.get())>20:
        errorMessage.config(text = "Password must be under 20 characters",fg = "red")
        valid = False
    return valid

#Checks that the username is unique, its length doesn't exceed 20 characters
#and that it isn't empty
def validate_username_signup(username,errorMessage):
    errorMessage.config(text = "",fg = "red")
    valid = True
    if len(username.get()) == 0:
        errorMessage.config(text = "Username cannot be empty",fg = "red")
        valid = False
    elif len(username.get())>20:
        errorMessage.config(text = "Username must be under 20 characters",fg = "red")
        valid = False
    else:
        results = select_query("SELECT username FROM Details")
        for row in results:
            if row[0] == username.get():
                valid = False
                errorMessage.config(text = "Username is already in use",fg = "red")
                break
    return valid

#Checks that an account with this username exists, the user username doesn't
#exceed 20 characters and that it isn't empty 
def validate_username_login(username,errorMessage):
    errorMessage.config(text = "",fg = "red")
    valid = False
    if len(username.get()) == 0:
        errorMessage.config(text = "Username cannot be empty",fg = "red")
    elif len(username.get())>20:
        errorMessage.config(text = "Username must be under 20 characters",fg = "red")
    else:
        results = select_query("SELECT username FROM Details")
        for row in results:
            if row[0] == username.get():
                valid = True
                break
    if valid == False:
        errorMessage.config(text = "Account with this username doesn't exist",fg = "red")
    return valid

#Checks if the username and password input are valid. If they are valid 
#an insert query is executed to add the data and the login screen is opened
def validate_signup_details(username,password,errorMessageUser,errorMessagePass,signupScreen):
    if (validate_username_signup(username,errorMessageUser) == True) and (validate_password(password,errorMessagePass) == True):
        execute_query("INSERT INTO Details(username,password,highScore) VALUES(%s,%s,%s)",(username.get(),password.get(),0))
        new_screen(signupScreen,login_screen)
    
#Checks if the password and username are valid, if they are valid a select query
#is executed to check if the password matches, if it does the quiz screen is opened
def validate_login_details(username,password,errorMessageUser,errorMessagePass,screen):
    if (validate_username_login(username,errorMessageUser) == True) and (validate_password(password,errorMessagePass) == True):
        results = select_query("SELECT username,password FROM Details")
        for row in results:
            if row[0] == username.get() and row[1] != password.get():
                errorMessagePass.config(text = "Password is incorrect",fg = "red")
            elif row[0] == username.get() and row[1] == password.get():
                new_screen(screen,lambda : quiz_screen(username))

#Creates the signup screen
def signup_screen():
    signupScreen = tk.Tk()
    signupScreen.title("Sign up")
    signupScreen.geometry("500x300")
    
    usernameLabel = tk.Label(signupScreen,text = "Username:")
    usernameLabel.grid(column=0,row=0,pady=10)
    
    username = tk.StringVar() #StringVar objects are used to allow
                              #for dynamic updating of value
    usernameEntry = tk.Entry(signupScreen,textvariable = username)
    usernameEntry.grid(column=1,row=0,pady=10)
    
    
    
    userValidationLabel = tk.Label(signupScreen,text = "",fg = "red")
    userValidationLabel.grid(column=0,row=1,pady=10)
    
    passwordLabel = tk.Label(signupScreen,text = "Password:")
    passwordLabel.grid(column=0,row=2,pady=10)
    
    password = tk.StringVar()
    
    passwordEntry = tk.Entry(signupScreen,textvariable = password)
    passwordEntry.grid(column=1,row=2,pady=10)
    
    passValidationLabel = tk.Label(signupScreen,text = "",fg = "red")
    passValidationLabel.grid(column=0,row=3,pady=10)
    
    submitButton = tk.Button(signupScreen,text = "Submit",command=lambda:validate_signup_details(username,password,userValidationLabel,passValidationLabel,signupScreen))
    submitButton.grid(column=0,row=4,pady=10)
    
    backButton = tk.Button(signupScreen,text = "Back",command = lambda: new_screen(signupScreen,first_screen))
    backButton.grid(column=0,row=5,pady=10)
    
    signupScreen.mainloop()
    

#Creates the login screen
def login_screen():
    loginScreen = tk.Tk()
    loginScreen.title("Login")
    loginScreen.geometry("500x300")
    
    usernameLabel = tk.Label(loginScreen,text = "Username:")
    usernameLabel.grid(column=0,row=0,pady=10)
    
    username = tk.StringVar()
    
    usernameEntry = tk.Entry(loginScreen,textvariable = username)
    usernameEntry.grid(column=1,row=0,pady=10)
        
    userValidationLabel = tk.Label(loginScreen,text = "",fg = "red")
    userValidationLabel.grid(column=0,row=1,pady=10)
    
    passwordLabel = tk.Label(loginScreen,text = "Password:")
    passwordLabel.grid(column=0,row=2,pady=10)
    
    password = tk.StringVar()
    
    passwordEntry = tk.Entry(loginScreen,textvariable = password)
    passwordEntry.grid(column=1,row=2,pady=10)
    
    passValidationLabel = tk.Label(loginScreen,text = "",fg = "red")
    passValidationLabel.grid(column=0,row=3,pady=10)
    
    submitButton = tk.Button(loginScreen,text = "Submit",command= lambda: validate_login_details(username,password,userValidationLabel,passValidationLabel,loginScreen))
    submitButton.grid(column=0,row=4,pady=10)
    
    backButton = tk.Button(loginScreen,text = "Back",command = lambda: new_screen(loginScreen,first_screen))
    backButton.grid(column=0,row=5,pady=10)
    
    loginScreen.mainloop()



#Returns a record to store a question, four potential answers and the correct answer
def create_questions_record(question,answerA,answerB,answerC,answerD,answerCorrect):
    class Record():
        def __init__(self,question,answerA,answerB,answerC,answerD,answerCorrect):
            self.question=question
            self.answerA=answerA
            self.answerB=answerB
            self.answerC=answerC
            self.answerD=answerD
            self.answerCorrect=answerCorrect
    return Record(question,answerA,answerB,answerC,answerD,answerCorrect)

#Returns an array of records that stores 10 random questions from the questions text file
def get_random_questions():
    questionsArray = []
    quizArray = []
    
    file = open("questions.txt","r")
    for row in file:
        rowparts = row.split(",")
        questionsArray.append(create_questions_record(rowparts[0],rowparts[1],rowparts[2],rowparts[3],rowparts[4],rowparts[5]))
    file.close()
    
    questionNo = random.sample(range(len(questionsArray)),10) #Chooses 10 random numbers within the length of the questionsArray
                                                              #array of records
    for i in range(0,10):                                     
        quizArray.append(questionsArray[questionNo[i]])       #Appends the chosen records from questionsArray to quizArray  
        
    return quizArray

#Updates the labels and buttons of the quiz screen after an answer is submitted,
#this function also updates i, which iterates through quizArray, and increments the score
#if the answer is correct. The post quiz screeen is opened after the last question.
def next_question(choice,i,quizArray,score,A,B,C,D,Question,screen,QCount,CScore,username):
    quizArray[i.get()].answerCorrect = quizArray[i.get()].answerCorrect[:-1]
    if choice.get() == quizArray[i.get()].answerCorrect:
        score.set(score.get()+1)
        
    if i.get() == 9:
        new_screen(screen,lambda: post_quiz_screen(score,quizArray,username))
    else:
        i.set(i.get()+1)
        A.config(text = quizArray[i.get()].answerA)
        B.config(text = quizArray[i.get()].answerB)
        C.config(text = quizArray[i.get()].answerC)
        D.config(text = quizArray[i.get()].answerD)
        Question.config(text = quizArray[i.get()].question)
        QCount.config(text = "Question number: " + str(i.get()+1))
        CScore.config(text = "Current score: " + str(score.get()))

#Updates the user's choice
def get_choice(answer,choice):
    choice.set(answer)
    
#Creates the quiz screen
def quiz_screen(username):
    quizArray = get_random_questions() #quizArray is initialised to store questions and answers
    
    quiz = tk.Tk()
    quiz.title("Quiz")
    quiz.geometry("1000x200")
    
    score = tk.IntVar(value = 0)       #Holds the users score for the quiz
    i = tk.IntVar(value = 0)           #Holds the position of the current record being accessed in quizArray
    choice = tk.StringVar(value = "")  #Holds the user's answer for the currente question
    
    QCount = tk.Label(quiz,text = "Question number: " + str(i.get()+1))
    QCount.grid(column = 0,row = 0,padx = 30)
    
    Question = tk.Label(quiz,text = quizArray[i.get()].question)
    Question.grid(column = 1,row = 0,padx = 30)
    
    CScore = tk.Label(quiz,text = "Current score: " + str(score.get()))
    CScore.grid(column = 2,row = 0,padx = 30)
    
    
    A = tk.Button(quiz,text = quizArray[i.get()].answerA,command = lambda: [get_choice("A",choice),next_question(choice,i,quizArray,score,A,B,C,D,Question,quiz,QCount,CScore,username)])
    A.grid(column=0,row=1,padx = (250,0),pady = 10)
    
    B = tk.Button(quiz,text = quizArray[i.get()].answerB,command = lambda: [get_choice("B",choice),next_question(choice,i,quizArray,score,A,B,C,D,Question,quiz,QCount,CScore,username)])
    B.grid(column=1,row=1,padx = (50),pady = 10)
        
    C = tk.Button(quiz,text = quizArray[i.get()].answerC,command = lambda: [get_choice("C",choice),next_question(choice,i,quizArray,score,A,B,C,D,Question,quiz,QCount,CScore,username)])
    C.grid(column=0,row=2,padx = (250,0),pady = 10)
        
    D = tk.Button(quiz,text = quizArray[i.get()].answerD,command = lambda: [get_choice("D",choice),next_question(choice,i,quizArray,score,A,B,C,D,Question,quiz,QCount,CScore,username)])
    D.grid(column=1,row=2,padx = (50),pady = 10)
    
#Queries the database and updates the user's score if it's greater than
#their high score
def update_high_score(score,username):
    results = select_query("SELECT username,highScore FROM Details")
    for row in results:
        if row[0] == username.get():
            if (row[1] == None) or (row[1] < score.get()):
                execute_query("UPDATE Details SET highScore = %s WHERE username =%s",(score.get(),username.get()))
            break

#Creates the post quiz screen
def post_quiz_screen(score,quizArray,username):
    postQuiz = tk.Tk()
    postQuiz.title("Post quiz")
    postQuiz.geometry("400x300")
    
    finalScore = tk.Label(postQuiz,text = "You scored: " + str(score.get()))
    finalScore.grid(column = 0,row = 0,padx = 50,pady = 10)
    
    update_high_score(score,username)
    
    retake = tk.Button(postQuiz,text = "Retake quiz",command = lambda: new_screen(postQuiz,lambda: quiz_screen(username)))
    retake.grid(column = 0,row = 1,padx = 10,pady = 10)   
    
    leaderboard = tk.Button(postQuiz,text = "View leaderboard",command = lambda: new_screen(postQuiz,lambda: leaderboard_screen(score,quizArray,username)))
    leaderboard.grid(column = 1,row = 1,padx = 5, pady = 10)

#Displays data from an array to the table
def display_data(array,table):
    table.delete(*table.get_children()) #Clears the table
    for row in array:
        table.insert("","end",values = row)  

#Displays all users
def table_users():
    results = select_query("SELECT username,highScore FROM Details")
    return results
    
#Displays users sorted by score descending
def table_sort_score():
    results = select_query("SELECT username,highScore FROM Details")
    results = bubble_sort_desc(results)
    return results

#Creates the leaderboard screen
def leaderboard_screen(score,quizArray,username):
    leaderboard = tk.Tk()
    leaderboard.title("Leaderboard")
    leaderboard.geometry("500x500")
    
    fields = ("Username","High Score") #used to identify the columns
    
    table = ttk.Treeview(leaderboard,columns = fields,show = "headings")
    
    table.heading("Username",text = "Username")
    table.column("Username",width = 100,anchor = "center")
    
    table.heading("High Score",text = "High Score")
    table.column("High Score",width = 100,anchor = "center")
    
    table.pack(expand=True, fill="both")
    
    back = tk.Button(leaderboard,text = "Back",command = lambda: new_screen(leaderboard,post_quiz_screen(score,quizArray,username)))
    back.pack(padx = 50,pady = 20)
    
    highScores = tk.Button(leaderboard,text = "View high scores",command = lambda: display_data(table_sort_score(),table))
    highScores.pack(padx = 50,pady = 20)
    
    users = tk.Button(leaderboard,text = "View all users",command = lambda: display_data(table_users(),table))
    users.pack(padx = 50,pady = 20)
    

first_screen()

                    
