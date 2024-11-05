def float_val(value):
    try:
        val_float = float(value)
        return val_float, True
    except ValueError:
        return 0, False