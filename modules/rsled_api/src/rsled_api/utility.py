def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

def clamp_array(arr, min_value, max_value):
    return [clamp(val, min_value, max_value) for val in arr]
