import random

def insertion_sort(arr, start, end):
    comparions = 0
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            comparions += 1 #porownanie arr[j] > key
        if j >= start:
            comparions += 1
        arr[j + 1] = key
    return comparions 

def merge(arr, left, mid, right):
    comparisons = 0
    left_part = arr[left:mid]
    right_part = arr[mid:right]

    i = j = 0
    k = left

    while i < len(left_part) and j < len(right_part):
        comparisons += 1 #porownanie left_part[i] <= right_part[j]
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1

    while i < len(left_part):
        arr[k] = left_part[i]
        i += 1
        k += 1

    while j < len(right_part):
        arr[k] = right_part[j]
        j += 1
        k += 1
    return comparisons

def run_sort(arr, run_size):
    n = len(arr)
    total_comparisons = 0

    #sortowanie fragmentow przy insertion sort
    for start in range(0, n, run_size):
        end = min(start + run_size, n)
        total_comparisons += insertion_sort(arr, start, end)

    #scalanie fragmentow przy merge sort
    size = run_size
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(left + size, n)
            right = min(left + 2 * size, n)
            if mid <right:
                total_comparisons += merge(arr, left, mid, right)
        size *= 2
    return total_comparisons

# testowanie funkcji

def generated_sorted(n):
    return list(range(n))

def generated_reserved(n):
    return list(range(n-1, -1, -1))

def generated_random(n):
    arr = list(range(n))
    random.shuffle(arr)
    return arr

def generated_nearly_sorted(n, swaps=10):
    arr = list(range(n))
    for _ in range(swaps):
        i ,j = random.sample(range(n), 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def test_exp(n, run_sizes):
    inputs = {
        "posortowana": generated_sorted(n),
        "odwrotnie_posortowana": generated_reserved(n),
        "losowa": generated_random(n),
        "prawie_posortowana": generated_nearly_sorted(n),
    }

    results = {}

    for kind, original_arr in inputs.items():
        results[kind] = {}
        for run_size in run_sizes:
            arr = original_arr.copy()
            comparisons = run_sort(arr, run_size)
            results[kind][run_size] = comparisons
            print(f"Rodzaj: {kind}, Rozmiar uruchomienia: {run_size}, Liczba porownan: {comparisons}")

    return results

#uruchomienie testu
n = 1000
run_sizes = [4,8,16,32]
results = test_exp(n, run_sizes)
