# ClassCharts-Notification-API 

This will log into the ClassCharts API using a wrapper made by [NCPlayz](https://github.com/NCPlayz/classcharts.py). I have modified it a tiny bit to suit my needs, however the underlying code is the same. This will use the [Pushover](https://pushover.net/) API and Mobile app to send notifications as they are currently not supported by the app itself. Other Dependencies needed are:

- Urllib
- Httplib
- Asyncio

# Setup
First install all of the PyPi dependencies

You must also have a way to send the notification. I have been using the Pushover application and it has been set up for this, however if you have an alternative just change the 'notification' function to complete something different. There are examples here. The only problem is that you must pay for a one time liscence of about £5 per platform however i feel that this is worth it.

The 'Removed.txt' is used as a backup for a bad read. If a homework is not read insted of being completely removed it will be moved to this file instead and added back to 'Homeworks.txt' next time. This prevents getting false 'New Homework' notifications

Clone the repository and then edit the 'UserDetails.txt' file to contain your usercode and your date of birth in the format provided, simply replace the x's with your data.

Lines 25 & 26 are the api tokens for the [Pushover](https://pushover.net/) API, i have two as i use a different one based on whether it is a homework that is due tomorrow or just in the future. Line 124 must be changed to the correct User ID for [Pushover](https://pushover.net/).

If i have forgotten something, you don't understand something, or something breaks feel free to create an issue, create a pull request or add me on discord as Ollie#0175 
I understand that my code may not have all the features you needed / may break so feel free to create a pull request with some changes if you make them!

# Thanks 
