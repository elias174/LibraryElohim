from datetime import datetime, timedelta

CURRENT_YEAR = datetime.now().year
LIST_YEARS = map(str, range(2017, CURRENT_YEAR+1))
LIST_YEARS.insert(0, 'Todos')
INDEX_CURRENT_YEAR = LIST_YEARS.index(str(CURRENT_YEAR))
