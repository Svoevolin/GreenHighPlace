from datetime import datetime
import pytz

print(str(datetime.now(pytz.timezone('Asia/Bangkok')).strftime("%d/%m/%Y %H:%M")))
