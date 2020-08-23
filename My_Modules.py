import csv
import statistics
import random

## Print File
def printfile(filename):
    readMe = open (filename, 'r').read()
    print (readMe)

## Read user file
def readuser():
    ## Reading user file.
    with open("user.csv") as userfile:
        users = csv.reader(userfile, delimiter=",")
        ## Building user list
        allusers = []
        for user in users:
            ## 0, user id; 1 name; 2 age; 3 gender
            userid = user[0]
            username = user[1]
            userage = user[2]
            usergender = user[3]
            user = (userid, username, userage, usergender)
            allusers.append(user)
        return(allusers)

## Read book file
def readbook():
    ## Reading book file.
    with open("book.csv") as bookfile:
        books = csv.reader(bookfile, delimiter=",")
        ## Building book list
        allbooks = []
        for book in books:
            bookid = book[0]
            bookname = book[1]
            booktheme = book[2]
            ## 0, book id; 1  name; 2 theme
            book = (bookid, bookname, booktheme)
            allbooks.append(book)
        return(allbooks)

## Return user info of userid
def getuserinfo(myuserid):
    ## Read user file
    allusers = readuser()

    ## Find user of userid, return user info
    for user in allusers:
        userid = user[0]
        username = user[1]
        userage = user[2]
        usergender = user[3]
        if userid == myuserid: ## Found user
            ## Return user name, age and gender
            return(username, userage, usergender)
            break

## Return book info of book id
def getbookinfo(mybookid):
    ## Reading book file
    allbooks = readbook()

    ## Find book and return book info
    for book in allbooks:
        bookid = book[0]
        bookname = book[1]
        booktheme = book[2]
        
        if bookid == mybookid: ## Found
            ## Return book name, theme
            return(bookname, booktheme)
            break

## Return userid of username
def getuserid(myusername):
    ## Reading user file
    allusers = readuser()
    
    ## Find user and return username
    for user in allusers:
        username = user[1]
        userid = user[0]
        if username == myusername:
            return(userid)
            break
            
## Read book borrow file
## Return one user's borrow history; return all history when myuserid is None
def readborrowhistory(myuserid):
  
    ## Reading book borrow file.
    with open("user_book.csv") as userbookfile:
        userbooks = csv.reader(userbookfile, delimiter=",")
        ## Building book list
        allborrowhistory = []
        for userbook in userbooks:
            
            #0, user id; 1  book id; 2 rating
            borrowuserid = userbook[0]
            borrowbookid = userbook[1]
            borrowbookrating = userbook[2]

            ## Return all history when myusername is None
            ## Return only the user's history if myusername is not None
            if myuserid is None or borrowuserid == str(myuserid):  

                borrowusername,borrowuserage,borrowusergender = getuserinfo(borrowuserid)
                borrowbookname,borrowbooktheme = getbookinfo(borrowbookid)
                
                borrowhistory = (borrowuserid, borrowbookid, borrowbookrating, borrowusername,borrowuserage,borrowusergender, borrowbookname,borrowbooktheme)
                allborrowhistory.append(borrowhistory)
        return(allborrowhistory)


## Check if user exists
def userexisting(checkusername):
    # Read user file
    allusers = readuser()
            
    ## Check if user exists
    for user in allusers:
        username = user[1] #1 user name
        if checkusername == username:
            return(True)
            break
    return(False)

    
## Add new user to user file
def adduser(userinfo):
    # Read user file
    allusers = readuser()
            
    ## Getting last user id
    lastuser = allusers[len(allusers) - 1]
    lastuserid = lastuser[0] # 0 user id
    
    ## Getting new user id
    newuserid = int(lastuserid) + 1
    
    ## Preparing new user info with the id
    userinfo = str(newuserid) + "," + userinfo
    
    ## Adding new user to the user file
    appenduserfile = open("user.csv","a")
    appenduserfile.write("\n")
    appenduserfile.write(userinfo)
    appenduserfile.close()



## Return top 2 themes of the user borrow history
def returntop2theme (userid):
    
    ## Collect all themes that current user is interested
    allthemes = []
    borrowhistory = readborrowhistory(userid)
    
    # print ("???")
    ## Go through borrow history to build theme counts
    for bhistory in borrowhistory:
        isnewtheme = True
        historytheme = bhistory[7]
        
        for theme in allthemes:
            ## theme[1] stores theme; theme[0] stores counts
            # print("?", theme)
            themename = theme[1]
            themecount = theme[0]
            
            ## counts books of same theme
            if themename == historytheme:
                theme[0] = theme[0] + 1
                isnewtheme = False
                break
            
        ## Add new theme to theme list
        if isnewtheme:
            newtheme = [1, historytheme]
            allthemes.append(newtheme)

    allthemes.sort(reverse=True)

    ## Return top2 theme
    top2theme = []
    i=1
    for theme in allthemes:
        top2theme.append(theme[1])
        if i==2:
            break
        i +=1 
        
    return (top2theme)


## Check the book has ever been borrowed before
def isborrowed(userid, bookid):
    ## Read borrow history
    allborrowhistry = readborrowhistory(userid)

    for borrowhistory in allborrowhistry:
        borrowed = False
        for borrowhistory in allborrowhistry:
            borrowuserid = borrowhistory[0]
            borrowbookid = borrowhistory[1]
            if borrowuserid == userid and borrowbookid == bookid:
                borrowed=True
                break
    return(borrowed)  


## Return book mean rating
def returnbookrating(bookid):

    bookratings = []

    allborrowhistory = readborrowhistory(None)
    
    for borrowhistory in allborrowhistory:

        borrowbookid = borrowhistory[1]
        borrowbookrating = borrowhistory[2]
        
        ## Get all ratings of the book
        # print ("?", bookid, borrowbookid, bookname)
        if borrowbookid == bookid and borrowbookrating != 0: #0 rating should be excluded 
            bookratings.append(int(borrowbookrating))
            
    # print ("?bookratings", bookratings)
    if len(bookratings) >= 1:
        rating = statistics.mean(bookratings)
    else:
        rating = 0
    
    return (rating)



## Return book by theme, with highest average ratings
## Exclude the book the user already borrowed
def returnbookbytheme(userid, mytheme):

    allbooks = readbook()
    returnbooks = []
        
    for book in allbooks:
        # print ("?isborrowed", username, book[0], isborrowed(username, book[0]))
        ## book[0] = book id, book[1]=book name, book[2] = theme

        bookid = book[0]
        bookname = book[1]
        booktheme = book[2]
        
        if booktheme == mytheme and not isborrowed(userid, bookname):
            ## collect all book of same theme and not borrowed before
            ## returnbook 0 - rating, 1- book id, 2- book name
            bookrating = returnbookrating(bookid)
            returnbook = (bookrating, bookid, bookname, booktheme)
            returnbooks.append (returnbook)

    ## Sorting books by rating desc
    returnbooks.sort(reverse=True)

    ## Return top one book 
    ## print ("?returnbooks", returnbooks)
    if len(returnbooks)>0:
        ## Return book of top rating
        returnbook = returnbooks[0]
        return(returnbook)

def maxbookid():
    ## Read book file
    allbooks = readbook()

    ## Getting last book id
    lastbook = allbooks[len(allbooks) - 1]
    lastbookid = lastbook[0] # 0 book id

    return(lastbookid)


## Returning book randomly
def returnbookrandomly(myuserid):

    ## Return largest book it
    largestbookid = maxbookid()

    ## Return random book id
    ## randombookid is required to be string for the function call for getbookinfo
    randombookid = str(random.randint(1,int(largestbookid)))
    
    randombookname,randombooktheme = getbookinfo(randombookid)
    radombookrating = returnbookrating(randombookid)
    suggestbook = (radombookrating, randombookid, randombookname, randombooktheme)

    return(suggestbook)

    
############################################################   

## Return Suggested Books

## A total of 5 books will be suggested
    ## 2 of them are suggested according to the users history
    ## 2 of them are going to be according to the users age group
    ## 1 will be randomly generated
    ## Previously skipped books will not be recommanded again.
    ## High rating books will be recommended first
    ### Recommendations will be getting better and better from machine learning (after more and more user data collected)


    ## Get the list of book ids
    ## Count books by themes
    ## Seach library and get the top books by theme excluding the ones he has already borrowed
    ## For each theme calculate the content percentage
    ## A total of 5 books will be recommended. Determine how many books by theme will be returned
    

def suggestbooks(userid):
    
    ## Store suggested books
    suggestedbooks = []

    ## Find top 2 themes the user may be interesed according to borrow history
    themes = returntop2theme(userid)
    # print ("?themes", themes)

    ## User has history with at least one theme, suggest one book of the theme
    if len(themes)>=1:
        top1theme = themes[0]
        suggestbook = returnbookbytheme(userid, top1theme)
        if suggestbook is not None:
            suggestedbooks.append(suggestbook)

  
    ## User has history with another theme, suggest one book of 2nd theme
    if len(themes)>=2:
        top2theme = themes[1]
        suggestbook = returnbookbytheme(userid, top2theme)
        if suggestbook is not None:
            suggestedbooks.append(suggestbook)

    
    ## Suggest books of same age group



    ## Randomly suggest more books until 5 books
    while len(suggestedbooks) <= 5:
        randomsuggestbook = returnbookrandomly(userid)
        if randomsuggestbook is not None:
            randomsuggestbookid = randomsuggestbook[1]
            ## Checking if this random book is already suggested or not
            issuggested = False
            for book in suggestedbooks:
                bookid = book[1]
                if bookid == randomsuggestbookid:
                    issuggested = True
                    break
            if not isborrowed(userid, randomsuggestbookid) and not issuggested:
                suggestedbooks.append(randomsuggestbook) 

  
    ## return suggested books   
    return (suggestedbooks)
        
############################################################   








