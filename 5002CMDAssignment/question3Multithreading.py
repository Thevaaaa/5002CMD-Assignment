import random
import threading
import time

# ====================================================
# FUNCTION: Generate 100 random numbers
# ====================================================
def generate_random_numbers():
    return [random.randint(0, 10000) for _ in range(100)]

# ====================================================
# FUNCTION: Multithreading task
# ====================================================
def thread_task(results, index, start_times, end_times, thread_index):
    start_times[thread_index] = time.time_ns()
    results[index] = generate_random_numbers()
    end_times[thread_index] = time.time_ns()

# ====================================================
# FUNCTION: One round of multithreading timing
# ====================================================
def run_multithreaded_round():
    results = [None] * 3
    threads = []
    start_times = [0] * 3
    end_times = [0] * 3

    for i in range(3):
        t = threading.Thread(target=thread_task, args=(results, i, start_times, end_times, i))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return max(end_times) - min(start_times)

# ====================================================
# FUNCTION: One round of non-multithreading timing
# ====================================================
def run_non_multithreaded_round():
    start_time = time.time_ns()
    _ = generate_random_numbers()
    _ = generate_random_numbers()
    _ = generate_random_numbers()
    end_time = time.time_ns()
    return end_time - start_time

# ====================================================
# FUNCTION: Run comparison for 10 rounds
# ====================================================
def run_comparison(rounds=10):
    mt_times = []
    non_mt_times = []
    differences = []

    print("\n🧪 Starting Performance Test (10 Rounds)\n")
    print("╔════════╦═══════════════════════╦══════════════════════════╦══════════════════════╗")
    print("║ Round  ║ Multithreading Time   ║ Non-Multithreading Time  ║ Difference (MT - NMT)║")
    print("╠════════╬═══════════════════════╬══════════════════════════╬══════════════════════╣")

    for i in range(rounds):
        mt_time = run_multithreaded_round()
        non_mt_time = run_non_multithreaded_round()
        diff = mt_time - non_mt_time

        mt_times.append(mt_time)
        non_mt_times.append(non_mt_time)
        differences.append(diff)

        print(f"║   {i+1:2}   ║{mt_time:>21,}ns║{non_mt_time:>24,}ns║{diff:>20,}ns║")

    print("╚════════╩═══════════════════════╩══════════════════════════╩══════════════════════╝")

    return mt_times, non_mt_times, differences

# ====================================================
# FUNCTION: Display summary table
# ====================================================
def display_summary(mt_times, non_mt_times, differences):
    total_mt = sum(mt_times)
    total_nmt = sum(non_mt_times)
    total_diff = total_mt - total_nmt

    avg_mt = total_mt / len(mt_times)
    avg_nmt = total_nmt / len(non_mt_times)
    avg_diff = avg_mt - avg_nmt
    ratio = avg_mt / avg_nmt

    print("\n📊 Summary of Results")
    print(" ╔═══════════════════════╦══════════════════════╗")
    print(" ║ Metric                ║ Value (in ns)        ║")
    print(" ╠═══════════════════════╬══════════════════════╣")
    print(f" ║ Total MT Time         ║ {total_mt:>20,} ║")
    print(f" ║ Total Non-MT Time     ║ {total_nmt:>20,} ║")
    print(f" ║ Total Time Difference ║ {total_diff:>20,} ║")
    print(" ╠═══════════════════════╬══════════════════════╣")
    print(f" ║ Avg MT Time           ║ {avg_mt:>20,.1f} ║")
    print(f" ║ Avg Non-MT Time       ║ {avg_nmt:>20,.1f} ║")
    print(f" ║ Avg Time Difference   ║ {avg_diff:>20,.1f} ║")
    print(f" ║ MT is {ratio:>6.2f}x slower                         ║")
    print(" ╚═══════════════════════╩══════════════════════╝")

# ====================================================
# MAIN EXECUTION
# ====================================================
def main():
    mt_times, non_mt_times, differences = run_comparison(10)
    display_summary(mt_times, non_mt_times, differences)

if __name__ == "__main__":
    main()
