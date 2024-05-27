from datetime import (
    datetime,
    timezone,
    timedelta
)

from database import BotDatabase

database = BotDatabase("src/bot.db")

def get_now_time(time: datetime = None, hours = 8) -> datetime:
    ori = datetime.now(timezone(timedelta(hours=hours))) if not time else time
    return datetime(ori.year, ori.month, ori.day, ori.hour, ori.minute, ori.second)

def get_time_left():
    time: datetime = datetime.strptime(database.get('start_time'), '%Y/%m/%d %H:%M:%S')
    now: datetime = get_now_time()
    time_left = time-now
    return time_left if now < time else "無資料"
    
def get_time_left_str():
    time_left = get_time_left()
    
    if time_left == "無資料":
        return time_left
        
    times = str(time_left).split()
    if time_left.days > 0:
        mi = times[2].split(':')
        times = f"{times[0]} 天 {mi[0]} 小時 {mi[1]} 分鐘"

    else:
        mi = times[0].split(':')
        times = f"0 天 {mi[0]} 小時 {mi[1]} 分鐘"
            
    return times