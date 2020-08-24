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
m.resetskipfile (2)


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

## Reset skip file to try again if no suggested books
if len(suggestedbooks)<= 0:
    ## reset skip file
    m.resetskipfile(userid)
    
    ## Return suggested books again
    suggestedbooks = m.suggestbooks(userid)
    if len(suggestedbooks)<= 0:
        print ("Sorry. No new book suggestions!")
        raise SystemExit 
        

while True:

    ## Display suggested books
    if len(suggestedbooks)> 0:
        print("\n")
        print("Here are some books I suggested. Enjoy! \n")
        
        for book in suggestedbooks:
            bookid = book[1]
            bookname = book[2]
            booktheme = book[3]
            print(bookid,"|",bookname,"|",booktheme)
            print("\n")

    ## Ask user input
    userselection = input("Enter book ID to borrow the book or type 'S' to skip all or type 'E' to exit. \n")
    
    ## exit
    if userselection == "E":
        print("Thank you for comming! Have a great day!")
        raise SystemExit

    ## Skip and suggest other books          
    elif userselection == "S":

        ## Add skip to file
        for book in suggestedbooks:
            bookid = book[1]
            m.addskip(userid, bookid)
        
        ## Return suggested books again
        suggestedbooks = m.suggestbooks(userid)

        ## Run out all books, reset skip file so that previously skipped file can be displayed again   
        if len(suggestedbooks)<=0:
            ## reset skip file
            m.resetskipfile(userid)
            suggestedbooks = m.suggestbooks(userid)
            if len(suggestedbooks)<= 0:
                print ("Sorry. No new book suggestions!")
                raise SystemExit 

        ## Loop to display new suggestions
        continue


    ## add borrow file                
    else:
        
        bookid = userselection
        if m.bookexisting(bookid):
            m.addborrow(userid, bookid)
            bookname,booktheme = m.getbookinfo(bookid)
            print("\nBook '" + bookname + "' has been borrowed.")
            ## Refreshing the suggested books after borrowing a book
            suggestedbooks = m.suggestbooks(userid)

        else:
            print ("Wrong input!")



