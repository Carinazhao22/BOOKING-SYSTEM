numOfbooking=0
numOfComment=0
import traceback
import pyodbc
conn = pyodbc.connect(
    'driver={SQL Server};server=cypress.csil.sfu.ca;uid=s_caijiez;pwd=jA6emjNf424j6aYq')
# ^^^ 2 values must be change for your own program.
# Since the CSIL SQL Server has configured a default database for each user, there is no need to specify it (<username>354)
cur = conn.cursor()
# to validate the connection, there is no need to change the following line
cur.execute('SELECT username from dbo.helpdesk')
row = cur.fetchone()
while row:
    print('SQL Server standard login name = ' + row[0])
    row = cur.fetchone()


def incrementDate(date):
    month = 0
    day = 0
    year = 0
    if date[1] != '/':
        month = month+int(date[0])
        month = month*10
        month += int(date[1])
        if date[4] != '/':
            day += int(date[3])
            day *= 10
            day += int(date[4])
            year += int(date[6])
            year *= 10
            year += int(date[7])
            year *= 10
            year += int(date[8])
            year *= 10
            year += int(date[9])

        else:
            day += int(date[3])
            year += int(date[5])
            year *= 10
            year += int(date[6])
            year *= 10
            year += int(date[7])
            year *= 10
            year += int(date[8])

    else:
        month = int(date[0])
        if date[3] != '/':
            day += int(date[2])
            day *= 10
            day += int(date[3])
            year += int(date[5])
            year *= 10
            year += int(date[6])
            year *= 10
            year += int(date[7])
            year *= 10
            year += int(date[8])
        else:
            day = int(date[2])
            year += int(date[4])
            year *= 10
            year += int(date[5])
            year *= 10
            year += int(date[6])
            year *= 10
            year += int(date[7])

    if day ==29 and month ==2:
        day = 1
        month+=1
    elif day!=30 and day!=31:
        day+=1
    elif day==30 and month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
        day+=1
    elif day == 31 and month ==1 or month ==3 or month ==5 or month ==7 or month ==8 or month ==10 or month ==12:
        day=1
        month+=1
    elif day == 30 and month ==4 or month ==6 or month ==9 or month ==11:
        day=1
        month+=1
    elif day==31 and month==12:
        year+=1

    result=str(month)+'/'+str(day)+'/'+str(year)
    return result
 
# users' options
cursor = conn.cursor()
cursorA=conn.cursor()
cursorB=conn.cursor()
while True:
    print("Please select any requests that you want!\n Type 1 for Searing Listings.\n Type 2 for Booking Listing.\n Type 3 for Writing Review.")
    queryA = input()  # query will be string
# searching list
    if queryA == '1':
        print("Please enter the minimum price that you want.")
        querymin = input()
        print("Please enter the maximum price that you want.")
        querymax = input()
        print("Please enter the number of bedrooms that you need.")
        querybed = input()
        print("Please enter the start date. e.g.'1/1/2016'Do not add zero.(m/d/y).")
        querystart = input()
        print("Please enter the end date e.g.'1/1/2016'Do not add zero(m/d/y).")
        queryend = input()
        print()
        print()
        try:
            SQLCommand = ("SELECT DISTINCT C.listing_id,C.price FROM Listings L,Calendar C WHERE C.listing_id=L.id AND L.number_of_bedrooms=? AND C.price>=? AND C.price<=? AND C.date=? AND C.available=?;")
            value = [int(querybed), float(querymin), float(querymax),querystart,1] 
            cursor.execute(SQLCommand, value)
        except:
            traceback.print_exc()
            conn.rollback()
        #for loop for checking the availability of these period
        else:
            results = cursor.fetchall()
            count=0
            for row in results:
                temp=row[0]
                total_price=float(row[1])
                # print("total_price1:",total_price)
                date=incrementDate(querystart)
                flag=1
                while date!=queryend and flag==1:
                    try:
                        SQLCommand = (
                            "SELECT C.available,C.price FROM Calendar C WHERE C.listing_id=? AND C.date=?;")
                        value = [int(row[0]),date]
                        cursorA.execute(SQLCommand, value)
                    except Exception as e:
                        print('Sorry ,an error is occurred!',e)
                    else:
                        subresult=cursorA.fetchone()
                        while subresult:
                            if subresult[0]==0 or float(row[1])<float(querymin) or float(row[1])>float(querymax):
                                flag=0
                            else:
                                total_price+=float(row[1])
                            subresult=cursorA.fetchone()
                        if flag==1:
                            date=incrementDate(date)
                        else :
                            break 
                    if date==queryend:
                        try:
                            SQLCommand=(
                                "SELECT DISTINCT L.id,L.name,L.number_of_bedrooms,LEFT(L.description,25) FROM Listings L,Calendar C WHERE C.listing_id=L.id AND L.id=? AND C.price>=? AND C.price<=? AND C.date=? AND C.available=?;")
                            value=[temp,float(querymin),float(querymax),querystart,1]
                            cursorB.execute(SQLCommand,value)
                        except Exception as e:
                            print('Sorry ,an error is occurred!',e)
                        else:
                            final=cursorB.fetchall()
                            for row in final:
                                if count==0:
                                    print("************The following is all the available rooms!************")
                                count+=1
                                print("id:",row[0])
                                print("name:",row[1])
                                print("number of bedrooms:",row[2])
                                print("description:",row[3])
                                print("total_price:",total_price)
                                print()
            if count==0:
                print("There is not available room during these period.\nPlease enter 1 to change your request!")
            print()
    #booking list
    elif queryA=='2':
        print("Please enter the booking info!")
        print("Please enter the listing's id that you want to book!")
        listing_id=int(input())
        print("Please enter you name!")
        guest_name=input()
        print("Please enter the start day!")
        stay_from=input()
        print("Please enter the end day!")
        stay_to=input()
        print("Please enter the number of guests!")
        number_of_guests=int(input())
        try:
            SQLCommand=("INSERT INTO Bookings(id,listing_id,guest_name,stay_from,stay_to,number_of_guests)VALUES(?,?,?,?,?,?)")
            values=[numOfbooking,listing_id,guest_name,stay_from,stay_to,number_of_guests]
            cursor.execute(SQLCommand,values)
        except Exception as e:
            print('Sorry ,an error is occurred!',e)
        else:
            conn.commit()
            numOfbooking+=1
            print("You are successful to book your room!")
            print()
    #write review
    elif queryA=='3':
        print("Please enter your name!")
        guest_name=input()
        try:
            SQLCommand=("SELECT * FROM Bookings B WHERE B.guest_name=?")
            values=[guest_name]
            cursor.execute(SQLCommand,values)
        except Exception as e:
            print('Sorry ,an error is occurred!',e)
        else:
            results=cursor.fetchone()
            print("************The following is your booking info.************")
            while results:
                print("id:", str(results[0]))
                print("listing_id:",str(results[1]))
                print("guest_name:",str(results[2]))
                print("stay_from:",str(results[3]))
                print("stay_to:",str(results[4]))
                print("number of guests:",str(results[5]))
                print()
                results=cursor.fetchone()
            print("Please enter the listing_id that you want to write review and shown above!")
            listing_id=int(input())
            print("Please enter you name!")
            name=input()
            print("Please enter the review you want to write!")
            review=input()
            try:
                SQLCommand=("INSERT INTO Reviews(id,listing_id,comments,guest_name) VALUES(?,?,?,?)")
                values=[numOfComment,listing_id,review,name]
                cursor.execute(SQLCommand,values)
            except Exception as e:
                print('Sorry ,an error is occurred!',e)
            else:
                conn.commit()
                numOfComment+=1
                print("Thanks for writing the comment!")
                print()             
conn.close()
