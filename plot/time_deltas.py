from datetime import datetime

FMT='%H:%M:%S.%f'
stamptime_origin="20:58:08.104209"
stamptime_end="20:58:13.795155"

Origin = datetime.strptime(stamptime_origin, FMT)
tdelta = datetime.strptime(stamptime_end, FMT) - Origin

print tdelta
