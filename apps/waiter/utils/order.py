from decimal import Decimal

# Payment methods proccess data
def order_paid_proccess_data(data,total_price):
    cash= Decimal(data["cash"] or 0 ) 
    transfer=Decimal(data["transfer"] or 0) 
    payment_type = data["payment_method"]
    if payment_type == 'efectivo':
      data={
        "cash":total_price,
        "transfer":0,
        "total_paid" : total_price,
        "paid_method":payment_type,
        "total_price" : total_price 
        }
    elif payment_type == 'transferencia':
      data={
        "cash":0,
        "transfer":total_price,
        "total_paid" : total_price,
        "paid_method":payment_type,
        "total_price" : total_price
        }
    else:
        data={
            "cash":cash,
            "transfer":transfer,
            "total_paid" : total_price,
            "paid_method":payment_type,
            "total_price" : cash + transfer
            }
    return data

