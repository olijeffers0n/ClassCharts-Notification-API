import http.client, urllib
import time
import datetime
import sys
import asyncio
import json

#Initiating Classcharts Module:
sys.path.append("./classcharts")
import classcharts
#Initiated Classcharts Module

async def main():
     var = (await sc.homeworks())
     await sc.logout()
     return var

###    Defining Needed Empty Variables   ###

hwks = []
removedhwks = []

###    Defining The User Id's for the Notification   ###

normal = "API TOKEN FOR NORMAL NOTIFICATION"
tomorrow = "API TOKEN FOR ALERT NOTIFICATION"

###   Dictionary for the number of days in each month   ###
daycountdict = {
              "01":"31", "02":"28", "03":"31", "04":"30", "05":"31", "06":"30", "07":"31", "08":"31", "09":"30", "10":"31", "11":"30", "12":"31"}

###   Creates the list of existing homeworks   ###
file = open("Homeworks.txt","r")
contents = file.readlines()
for hw in contents:
    hw = hw.replace('\n','')
    hwks.append(hw)
file.close()

###   Adds the homeworks that were removed last time to add resiliency to bad reads   ###
file = open("Removed.txt","r")
contents = file.readlines()
for hw in contents:
    hw = hw.replace('\n','')
    removedhwks.append(hw)
    hwks.append(hw)
file.close()
hwlist_for_removing = hwks[:]

###   Reads the User Details   ###
file = open("UserDetails.txt","r")
contents = file.readlines()
CODE = contents[0]
CODE = CODE.replace("USERCODE: ","")
CODE = CODE.replace("\n","")
DOB = contents[1]
DOB = DOB.replace("DOB: ","")
DOB = DOB.split("/")

###   Returns the amount of days until the homework is due   ###
def daycount(date):
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    today = today.split("/")
    date = date.split("/")
    check = int(date[1]) - int(today[1])

    if int(today[2]) != int(date[2]):
        return "Next Year"
    elif today[1] == date[1]:
        countdown = int(date[0]) - int(today[0])
        if countdown > 0:
            return "In " + str(countdown) + " day(s)"
        else:
        
            return "It was due " + str(abs(countdown)) + " day(s) ago"
    elif check == 1:
        numberofdays = daycountdict[today[1]]
        daysleft = int(numberofdays) - int(today[0])
        daysleft = daysleft + int(date[0])
        return "In " + str(daysleft) + " days"
    else:
        return "Later than next month"

###   Calculates whether the homework is due tomorrow and if it is 3pm. If so, it will return True   ###
def datecomp(due):
    now = datetime.datetime.now()
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    current_time = now.strftime("%S:%M:%H")
    current_time = current_time.split(":")
    today = today.split("/")
    day = int(today[0]) + 1
    del today[0]
    day = str(day)
    today.insert(0,day)
    today.insert(1,"/")
    today.insert(3,"/")
    res = "".join(today)
    due = due.split("/")
    day = due[0]
    if "0" in day:
        day = day.replace("0","")
        due[0] = day
    due.insert(1,"/")
    due.insert(3,"/")
    due = "".join(due)
    if res == due:
        if current_time[2] == "15":
            if int(current_time[1]) <= 15:
                return True
            else:
                return False
        else:
            return False
    elif res != due:
        return False

###   Function That can have the title and the body passed to it   ###

def notification(token,title,message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": token,
        "user": "<<<<YOUR USER ID>>>>",
        "message": message,
        "title": title,
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

###   Sends a message with more detailed info on exceptions
def ExceptionDealing():
    exception = str(sys.exc_info())
    exception = exception.split(",")
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno
    ErrorMessageContent = str(exception_type) + "\n" + str(exception[1]) + "\nAt Line: " + str(line_number)
    notification(normal,"An Error has Occurred",ErrorMessageContent)

###   Shortens the 'time.sleep()' 
def sleep(length):
    time.sleep(length)

#Getting and Parsing data:

try:
    sc = classcharts.StudentClient(CODE, datetime.datetime(year=int(DOB[2]), month=int(DOB[1]), day=int(DOB[0])))
    hwkReturnArray = asyncio.get_event_loop().run_until_complete(main())
    number_of_hwks = len(hwkReturnArray)

    print("You have",number_of_hwks,"Homework(s) left to do")

    file = open("Homeworks.txt","w")

    for homework in hwkReturnArray:
        new = False

        teacher = homework.teacher
        lesson = homework.lesson
        title = homework.title

        due = homework.due_date
        dateparts = due.split("-")
        due = [dateparts[2],"/",dateparts[1],"/",dateparts[0]]
        date = ''.join(due)
        datedaysleft = daycount(date)


        hwinfo_for_notification = title + "\n" + "Set by: " + teacher + " for " + lesson +"\n"+ "Due on: " + date + " - "+datedaysleft
        fullhwinfo = title + " | Set by: " + teacher + " for " + lesson + " | Due on: " + date
        tom_hwinfo = title + " | Set by: " + teacher + " for " + lesson

        #Works out if it is a new homework or not

        if hwks.count(fullhwinfo) == 1:
            print(fullhwinfo+" - Which is Old")
            file.write(fullhwinfo+'\n')

        if hwks.count(fullhwinfo) == 0:
            new = True
            print(fullhwinfo+" - Which is New")
            messagetitle = "New Home Work: " + title
            notification(normal,messagetitle,hwinfo_for_notification)
            file.write(fullhwinfo+'\n')

        #Runs the comparison to check if a notification is needed for the homework tomorrow
        
        if datecomp(date) == True:
            if new == False:

                notification(tomorrow,"Homework Due Tomorrow",hwinfo_for_notification)
        
        if fullhwinfo in hwlist_for_removing:
            hwlist_for_removing.remove(fullhwinfo)

    file.close()

    #Writes homeworks that didn't appear to 'Removed.txt' for one bad read of resiliency to stop incorrect notifications
    file = open("Removed.txt","w")
    for hwk in hwlist_for_removing:
        if hwk not in removedhwks:
            file.write(hwk+'\n')
    file.close()

    #Does some logging of when the program runs in case of the need to troubleshoot
    file = open("Log.txt","a")
    today = datetime.datetime.today().strftime('%d/%m/%Y')
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    file.write("The Script run at: "+current_time+" On the "+today+"\n")
    file.close()

except Exception as e:

    #Does some error handling to make sure that the program is always terminated and doesn't leave web drivers running

    ExceptionDealing()
    
    #Writes all the homeworks back to the file so that they don't all send notifications upon next run
    f = open("Homeworks.txt","w")
    for homework in hwks:
        f.write(homework+"\n")
    f.close()