from statistics import median


def rolling_median(array, window):
    smoothed_array = []
    for i in range(len(array)):
        start = max(0, i - window // 2)
        end = min(len(array), i + window // 2 + 1)
        smoothed_array.append(median(array[start:end]))
    return smoothed_array
