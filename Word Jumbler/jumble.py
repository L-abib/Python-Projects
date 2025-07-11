import random

print("Welcome To Word Jumble Game!")
print("Prepared By Hojaifa Hossain, Md Labib, Md Shadman Tahsin Khan.")
print("===============================================================")
print("===============================================================")

def scoreboard():
    with open('scoreboard.txt', 'r') as file:
        score=file.readlines()
        for x in score:
            print(x) 
        
def play(pname):
    print("#############################################################################################")
    a="""TUTORIAL: You'll be given a Jumbled word. You have to guess it. 
          Each correct guess will reward you 10 points. 
          You can also ask for a clue. In that case, correct guess will reward you 5 points. 
          If your guess is wrong three times the game will end. 
          In each level you'll have to guess three words to advance to next level. 
          Higher levels will have bigger words to guess. Good luck!"""
    print(a)
    print("#############################################################################################")
    with open('wlist.txt','r') as  file:
        wlist=file.readlines()
    
    print("################################################")
    print("Welcome! You are at level 1.")
    print("################################################")
    letter=3
    score=0
    life=3
    level=1
    correct=0
    nextlevel=3
    while True:
        bruh=[]
        for x in wlist:
            word,clue=x.strip().split(' : ')
            if len(word.strip())==letter:
                bruh.append((word,clue))
    
        if not bruh:
            print("No words available for this level. Exiting the game.")
            break
        rword,rclue=random.choice(bruh)
        jword = ''.join(random.sample(rword, len(rword)))
        print("================================================")
        print(f"Remaining life: {life} \nThe game will end if you have no life left.")
        print("================================================-")
        print("Jumbled word: "+jword)
        print("Enter 1 to get a clue. Enter 2 to quit.")
        
        print("------------------------------------------------")
        guess = input("Your guess: ")
        
        
        if guess.lower()==rword:
            score += 10
            print("Correct! You've earned 10 points.")
            correct+=1
        elif guess=='1':
            print("The clue is: "+rclue)
            print("------------------------------------------------")
            guess = input("Your guess: ")
            if guess.lower()==rword:
                score += 5
                print("Correct! You've earned 5 points.")
                correct+=1
            else:
                life-=1
                print(f"Wrong! The correct word was '{rword}'.")
        elif guess=='2':
            print("You've quit the game! Better luck next time...")
            break
        else:
            life-=1
            print(f"Wrong! The correct word was '{rword}'.")
        
        print(f"Your current score: {score}")
    
        if life==0:
            print("************************************************")
            print("You ran out of life! Better luck next time...")
            print("************************************************")
            break
    
        if correct>=nextlevel:
            level += 1
            letter += 1
            nextlevel+=3
            if level==6:
                print("################################################")
                print("Congratulations! You have cleared the game!")
                print("################################################")
                break
            else:
                print("################################################")
                print(f"Congratulations! You've reached level {level}")
                print(f"You'll have to guess {letter} letter words in this level!")
                print("################################################")

    with open('scoreboard.txt','a') as  file:
        file.write(f"{pname}: {score}\n")
    
    print("************************************************")
    print(f"Game over! \nYour final score: {score}")
    print("************************************************")


def register():
    pname=input("Enter a Player Name: ")
    pemail=input("Enter your email address: ")
    passw=input("Enter a Password: ")

    with open('info.txt','r') as file:
        pinfo=file.readlines()
        
        for x in pinfo:            
            if not x.strip():
                continue
            else:
                vname,vemail,vpass=x.strip().split(',') 
                if vname==pname:
                    print("Username already exists! Please try again.")
                    return
                
    with open('info.txt','a') as file:
        file.write(f"{pname},{pemail},{passw}\n")
    print("Registration Successful!")

    


def login():
    pname=input("Enter your player name: ")
    ppass=input("Enter your password: ")

    with open('info.txt','r') as file:
        pinfo=file.readlines()
        for x in pinfo:
            if not x.strip():
                continue
            else:
                vname,vemail,vpass=x.strip().split(',')
                if vname==pname and vpass==ppass:
                    print("Login Successful!")
                    play(pname)
                    return
        print("Wrong username or password!")



def leaderboard():
    print("========================================")
    print("The leaderboard:\n")
    with open('scoreboard.txt','r') as file:
        board=file.readlines()
    for x in board:
        print(x)
    print("========================================") 




def admin():
    aname=input("Enter admin name: ")
    apass=input("Enter password: ")

    if aname=='admin' and apass=='admin':
        print("You've successfully logged in as admin! \nWelcome to admin page!")
    else:
        print("Wrong username or password!")
        return

    while True:
        print("1. Check user information")
        print("2. Edit user information")
        print("3. Check leaderboard")
        print("4. Exit")
        print("========================================")
        option=input("Choose an option: ")
        if option=='1':
            print("===============================================================")
            print("All user information:\n")
            with open('info.txt','r') as file:
                pinfo=file.readlines()
                for x in pinfo:
                    print(x)
            print("===============================================================")
        elif option=='2':
            ename=input("Enter the player name whose information you want to edit: ")
    
                
            with open('info.txt','r') as file:
                pinfo=file.readlines()
    
            found=False
            uinfo=[]
            for x in pinfo:
                if not x.strip():
                    continue
                pname,pemail,ppass=x.strip().split(',')
    
                if pname==ename:
                    found=True
                    print(f"User's current Information - Email: {pemail}, Password: {ppass}")
                    nemail=input("Enter new email (or press Enter to keep the current): ")
                    npassword=input("Enter new password (or press Enter to keep the current): ")
    
                    pemail=nemail if nemail else pemail
                    ppass= npassword if npassword else ppass
    
                    uinfo.append(f"{pname},{pemail},{ppass}\n")
                    print(f"Information for {pname} updated successfully!")
                else:
                    uinfo.append(x)
    
            if not found:
                print(f"Player {ename} not found!")
    
            with open('info.txt', 'w') as file:
                file.writelines(uinfo)
        elif option=='3':
            leaderboard()   
        elif option=='4':
            break
        else:
            print("Please choose a valid option!")
            print("========================================")
            
    


def start():
    while True:
        print("1. Register")
        print("2. Login")
        print("3. Login as admin")
        print("4. Exit")
        print("========================================")
        option=input("Choose an option: ")

        if option=='1':
            register()
            print("========================================")
        elif option=='2':
            while True:
                print("1. Login as existing player")
                print("2. Check leaderboard")
                print("3. Exit")
                print("========================================")
                op=input("Choose an option: ")
                if op=='1':
                    login()
                    print("========================================")
                elif op=='2':
                    leaderboard()
                    print("========================================")
                elif op=='3':
                    break
                else:
                    print("Please choose a valid option!")
                    print("========================================")
        elif option=='3':
            admin()
            print("========================================")
        elif option=='4':
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option!")
            print("========================================")


start()
