import csv
import My_Modules as m
## from My_Modules import userexisting as isexisting

## Debug - print files  
# m.printfile("user.csv")
# print("\n")
# m.printfile("books.csv")
# print("\n")
# m.printfile("user_book.csv")

## Debug - print data 

'''
print(m.readuser())
print("\n")
print(m.readbook())
print("\n")
print(m.readborrowhistory(None))
print("\n")
print(m.getbookinfo('6'))
'''



## Starting conversation, asking for full name
username = input("Hello I'm Nova, the book suggester! What's your name(First and Last)? \n")

## Collecting user info for new user, save new user to userfile
if not m.userexisting(username):
    print("Welcome",username,"!")
    ######## Add validation to the input later
    userage = input("Can I ask your age? ")
    usergender = input("Can I ask your gender? M-Male/F-Female/O-Other) ")

    ## Saving new user data to user file
    newuser = username + "," + userage + "," + usergender
    m.adduser(newuser)
    
else:
    print("\nWelcome back",username,"!")

## Get userid
userid = m.getuserid(username)

## Return suggested books
suggestedbooks = m.suggestbooks(userid)

if len(suggestedbooks)> 0:

    print("\n")
    print("Here are some books I suggested. Enjoy! \n")
    
    for book in suggestedbooks:
        bookid = book[1]
        bookname = book[2]
        booktheme = book[3]
        print(bookid,"|",bookname,"|",booktheme)
        print("\n")
        
else:
    print ("No book suggestion!!")
    raise SystemExit

while True:
    userselection = input("Enter book ID to borrow the book or type 'S' to skip all or type 'E' to exit. \n")
    
    ## exit
    if userselection == "E":
        print("Thank you for comming! Have a great day!")
        raise SystemExit

    ## Skip and suggest books again          
    elif userselection == "S":

        ## Update skip file
        for book in suggestedbooks:
            bookid = book[1]
            m.addskip(userid, bookid)
        
        ## Return suggested books again
        suggestedbooks = m.suggestbooks(userid)

        if len(suggestedbooks)> 0:

            print("\n")
            print("Here are some books suggested. Enjoy! \n")
        
            for book in suggestedbooks:
                bookid = book[1]
                bookname = book[2]
                booktheme = book[3]
                print(bookid,"|",bookname,"|",booktheme)
                print("\n")
                
        else:
            print ("No book suggestions!!")
            raise SystemExit

    ## add borrow file                
    else:
        
        bookid = userselection
        if m.bookexisting(bookid):
            m.addborrow(userid, bookid)
            bookname,booktheme = m.getbookinfo(bookid)
            print("'" + bookname + "' has been borrowed.")
        else:
            print ("Wrong input!")



