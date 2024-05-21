import calendar

months = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]


colorPalette = ["#55efc4", "#81ecec", "#a29bfe", "#ffeaa7", "#fab1a0", "#ff7675", "#fd79a8"]
colorPrimary, colorSuccess, colorDanger = "#79aec8", colorPalette[0], colorPalette[5]
days = []
days_of_week = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo',
}


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette


def get_month_dict():
    day_dict = dict()
    
    for day in days:
        day_dict[day] = 0

    return day_dict

def get_product_month_dict(year,month):
    day_dict = dict()
    day_month=[]
    num_day = calendar.monthrange(year, month)[1]
    for day_m in range(1, num_day + 1):
        if day_m < 10:
            day_month.append(f'0{day_m}')
        else: day_month.append(f'{day_m}')
    for day in day_month:
        day_dict[day] = 0

    return day_dict