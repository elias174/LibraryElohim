from datetime import datetime, timedelta

CURRENT_YEAR = datetime.now().year
LIST_YEARS = map(str, range(2017, CURRENT_YEAR+1))
LIST_YEARS.insert(0, 'Todos')
INDEX_CURRENT_YEAR = LIST_YEARS.index(str(CURRENT_YEAR))
MATRICULA_MOUNT_DEFAULT = 100.0
MONTHS = {
    'Enero': 1,
    'Febrero': 2,
    'Marzo': 3,
    'Abril': 4,
    'Mayo': 5,
    'Junio': 6,
    'Julio': 7,
    'Agosto': 8,
    'Septiembre': 9,
    'Octubre': 10,
    'Noviembre': 11,
    'Diciembre': 12
}
