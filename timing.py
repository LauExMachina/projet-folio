from datetime import datetime


def timing():

    date = datetime.now()

    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    timing_list = [year, month, day, hour, minute]

    return timing_list




if __name__=="__main__":
    
    pass