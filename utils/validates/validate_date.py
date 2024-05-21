def validate_dates(start_date, end_date):
            try:
                
                if start_date and end_date:
                    return True,''
                elif start_date:
                    return False, "La fecha final está vacía."
                elif end_date:
                    return False, "La fecha inicial está vacía."
                else:
                    return False, "Ambas fechas están vacías."
            except ValueError:
                return False, "Las fechas tienen un formato incorrecto."