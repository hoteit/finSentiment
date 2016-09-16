
### set of utility functions



def float_or_na(value):
    # converts values to floating point
    return float(value if value != 'n/a' else 'nan')

def millions(val):
    ### strips M or B from decimals, converts billions into millions and assumes everything in millions.
    lookup = {'M': 1, 'B': 1000}
    if (val is 'n/a'):
        return "0.0"
    else:
        unit = val[-1]
        try:
            number = float(val[1:-1]) if '$' in val else float(val[:-1])
            if unit in lookup:
                return lookup[unit] * number
            else:
                return number
        except ValueError:
            return "0.0"
