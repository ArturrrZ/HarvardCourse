import datetime

now=datetime.datetime.now()
d=now.date()
print(now)
date=now.strftime("%D %H:%M")
print(date)
print(type(date))


print(datetime.datetime.now().date())