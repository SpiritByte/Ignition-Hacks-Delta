import csv
import statistics
import random

## Print File
def printfile(filename):
    readMe = open (filename, 'r').read()
    print (readMe)

## Reset skip book file
def resetskipfile(userid):

    ## Reading skip file.
    skiprows = []
    with open("user_book_skip.csv") as skipfile:
        allskiprows = csv.reader(skipfile, delimiter=",")
        for skiprow in allskiprows:
            if len(skiprow)>0:
                rowuserid = skiprow[0]
                if rowuserid != str(userid):
                    skiprows.append(skiprow)


    ## Empty skip file
    file = open("user_book_skip.csv","w")
    file.close()

    ## Add back skip records of other users
    appenduserfile = open("user_book_skip.csv","a")
    i=1
    for skiprow in skiprows:
        userid = skiprow[0]
        bookid = skiprow[1]
        
        userinfo = userid + "," + bookid

        appenduserfile.write(userinfo)
        # print (i,len(skiprows), userinfo)
        if i != len(skiprows):
            appenduserfile.write ("\n")

        i+=1
        
    appenduserfile.close()



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

## Read user skip book file
def readskiphistory(myuserid):
    ## Reading user skip book file.
    with open("user_book_skip.csv") as skiphistoryfile:
        allskiphistory = csv.reader(skiphistoryfile, delimiter=",")
       
        ## Building skip book list
        allskipbooks = []
        for skiphistory in allskiphistory:
            if len(skiphistory) <=0:
                break
            skipuserid = skiphistory[0]
            if skipuserid == myuserid:
                skipbookid = skiphistory[1]
                skipbook = (skipuserid, skipbookid)
                allskipbooks.append(skipbook)
        return(allskipbooks)

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

## Check if book exists
def bookexisting(mybookid):
    # Read user file
    allbooks = readbook()
            
    ## Check if user exists
    for book in allbooks:
        bookid = book[0] #1 user name
        if bookid == mybookid:
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


## Add new borrows 
def addborrow(userid, bookid):

    borrow = str(userid) + "," + str(bookid) + ",0"
    
    ## Adding new borrow to the borrow file
    appenduserfile = open("user_book.csv","a")
    appenduserfile.write("\n")
    appenduserfile.write(borrow)
    appenduserfile.close()


## Add skip books  
def addskip(userid, bookid):

    skip = str(userid) + "," + str(bookid)
    
    ## Adding new skip to the skip file
    appenduserfile = open("user_book_skip.csv","a")
    appenduserfile.write("\n")
    appenduserfile.write(skip)
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

    borrowed = False
    for borrowhistory in allborrowhistry:
        borrowuserid = borrowhistory[0]
        borrowbookid = borrowhistory[1]
        
        if borrowuserid == userid and borrowbookid == bookid:
            borrowed=True
            break
    
    return(borrowed)  


## Check the book has ever been skipped before
def isskipped(userid, bookid):
    ## Read skip history
    allskiphistry = readskiphistory(userid)

    skipped = False
    for skiphistory in allskiphistry:
        skipuserid = skiphistory[0]
        skipbookid = skiphistory[1]
        if skipuserid == userid and skipbookid == bookid:
            skipped = True
            break
    return(skipped)



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
## Exclude the book the user already borrowed or skipped
def returnbookbytheme(userid, mytheme):

    allbooks = readbook()
    returnbooks = []
        
    for book in allbooks:
        # print ("?isborrowed", username, book[0], isborrowed(username, book[0]))
        ## book[0] = book id, book[1]=book name, book[2] = theme

        bookid = book[0]
        bookname = book[1]
        booktheme = book[2]
        
        if booktheme == mytheme and not isborrowed(userid, bookid) and not isskipped(userid, bookid):
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

## Return book by age, with highest average ratings
## Exclude the book the user already borrowed or skipped
def returnbookbyage(userid):

    username,userage,usergender = getuserinfo(userid)
    
    ## Store return books
    returnbooks = []
    
    ## Read borrow history
    allborrowhistory = readborrowhistory(None)

    for borrowhistory in allborrowhistory:
        borrowuserid = borrowhistory[0]
        borrowuserage = borrowhistory[4]
        borrowusergender = borrowhistory[5]
        borrowbookid = borrowhistory[1]
        borrowbookname = borrowhistory[6]
        borrowbooktheme = borrowhistory[7]

        borrowusername,borrowuserage,borrowusergender = getuserinfo(borrowuserid)
        
        ## Skip current user history, and retrun book of same age group (age differnece <=2)
        if borrowuserid != userid and abs(int(userage) - int(borrowuserage)) <= 2:

            borrowbookrating = returnbookrating(borrowbookid)
            
            returnbook = (borrowbookrating, borrowbookid, borrowbookname, borrowbooktheme)       
            returnbooks.append (returnbook)

    ## Sorting books by rating desc
    returnbooks.sort(reverse=True)

    ## Return 2 books of toping rating 
    ## print ("?returnbooks", returnbooks)
    returnbook1=None
    if len(returnbooks)>=1:
        returnbook1 = returnbooks[0]
    returnbook2 = None
    if len(returnbooks)>=2:
        returnbook2 = returnbooks[1]
    return(returnbook1, returnbook2)

    
## Returning book randomly
def returnbookrandomly(myuserid):
    ## Prepare book list
    availblebooklist = []

    allbooks = readbook()
    rowid = 1
    for book in allbooks:
        bookid = book[0]
        
        if not isborrowed(myuserid,bookid) and not isskipped (myuserid, bookid):
            availblebook = (rowid,bookid)
            availblebooklist.append(availblebook)
            rowid += 1
    
    ## Return max rows 
    maxrowid = rowid - 1
    ## No book availble
    if maxrowid<=0:
        return

    ## Return random book id
    ## randombookid is required to be string for the function call for getbookinfo
    randomrowid = random.randint(1,int(maxrowid))
    randombook = availblebooklist[randomrowid-1]
    randombookid = str(randombook[1])
   
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
############################################################  

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
    suggestbook1,suggestbook2 = returnbookbyage (userid)
    if suggestbook1 is not None:
        suggestedbooks.append(suggestbook1)
    if suggestbook2 is not None:
        suggestedbooks.append(suggestbook2)


    ## Randomly suggest more books until 5 books
    trycount = 1
    while len(suggestedbooks) < 5:
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
            if not isborrowed(userid, randomsuggestbookid) and not issuggested and not isskipped(userid, randomsuggestbookid):
                suggestedbooks.append(randomsuggestbook) 

        trycount += trycount
        ## stop if trycount >10000 
        if trycount>10000:
            break
    
    ## return suggested books   
    return (suggestedbooks)
        
############################################################   








