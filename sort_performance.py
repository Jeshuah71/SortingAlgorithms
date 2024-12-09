import random
import time
import matplotlib.pyplot as plt


def bubble_sort(a_list):
    for i in range(len(a_list)):
        for j in range(len(a_list) - i - 1):
            if a_list[j] > a_list[j + 1]:
                a_list[j], a_list[j + 1] = a_list[j + 1], a_list[j]

def selection_sort(a_list):
    for i in range(len(a_list)):
        min_idx = i
        for j in range(i + 1, len(a_list)):
            if a_list[j] < a_list[min_idx]:
                min_idx = j
        a_list[i], a_list[min_idx] = a_list[min_idx], a_list[i]

def insertion_sort(a_list):
    for i in range(1, len(a_list)):
        current_value = a_list[i]
        pos = i
        while pos > 0 and a_list[pos - 1] > current_value:
            a_list[pos] = a_list[pos - 1]
            pos -= 1
        a_list[pos] = current_value

def merge_sort(a_list):
    if len(a_list) > 1:
        mid = len(a_list) // 2
        left_half = a_list[:mid]
        right_half = a_list[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                a_list[k] = left_half[i]
                i += 1
            else:
                a_list[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            a_list[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            a_list[k] = right_half[j]
            j += 1
            k += 1

def quick_sort(a_list):
    def quick_sort_helper(lst, low, high):
        if low < high:
            pi = partition(lst, low, high)
            quick_sort_helper(lst, low, pi - 1)
            quick_sort_helper(lst, pi + 1, high)

    def partition(lst, low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if lst[j] < pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        return i + 1

    quick_sort_helper(a_list, 0, len(a_list) - 1)

# Setting up the experiment
def generate_random_list(size):
    return [random.randint(1, 100000) for _ in range(size)]

def measure_time(sort_func, data):
    start = time.time()
    try:
        sort_func(data)
        return time.time() - start
    except Exception as e:
        print(f"Error: {e}")
        return float("inf")

sizes = [1000, 10000, 100000, 1000000]
algorithms = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

results = {alg: [] for alg in algorithms}

# Running the experiment
for size in sizes:
    print(f"Testing size: {size}")
    data = generate_random_list(size)
    for alg_name, alg_func in algorithms.items():
        if size > 10000 and alg_name in ["Bubble Sort", "Selection Sort", "Insertion Sort"]:
            print(f"Skipping {alg_name} for size {size} (expected timeout)...")
            results[alg_name].append(None)
            continue

        test_data = data.copy()
        print(f"Testing {alg_name}...")
        exec_time = measure_time(alg_func, test_data)
        results[alg_name].append(exec_time)
        print(f"{alg_name} took {exec_time:.6f} seconds for size {size}")
        if exec_time > 1200:  # Timeout limit of 20 minutes
            print(f"{alg_name} timed out on size {size}!")
            break

# Displaying the results 
print("\nResults:")
for alg_name, times in results.items():
    print(f"{alg_name}: {times}")

# Plotting  the results
for alg_name, times in results.items():
    if any(t is not None for t in times):  
        plt.plot(sizes[:len(times)], times, marker='o', label=alg_name)

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Input Size (log scale)")
plt.ylabel("Time (seconds, log scale)")
plt.title("Sorting Algorithm Performance")
plt.legend()
plt.grid()
plt.show()
