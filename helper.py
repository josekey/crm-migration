from datetime import timezone, datetime
from dateutil.parser import parse


def ISO_to_UNIX(d):
    dt = parse(d)
    return int(round(dt.replace(tzinfo=timezone.utc).timestamp(),0))

def test():
    print(ISO_to_UNIX('2021-06-08T20:30:19.333000+00:00'))

if __name__ == "__main__":
    test()