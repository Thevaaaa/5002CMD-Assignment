import random
from collections import defaultdict

# --- folding hash function ---
def folding_hash(ic_num, table_size):
    ic_str = str(ic_num)
    group_size = 4
    total = 0
    for i in range(0, len(ic_str), group_size):
        group = int(ic_str[i:i+4])
        total += group
    return total % table_size

# --- generate random 12-digit IC number ---
def generate_ic():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

# --- hash table class with separate chaining ---
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.collisions = 0

    def insert(self, key):
        index = folding_hash(key, self.size)
        if self.table[index]:  # Collision occurs
            self.collisions += 1
        self.table[index].append(key)

    def reset(self):
        self.table = [[] for _ in range(self.size)]
        self.collisions = 0

# --- display hash table (shortened & clean) ---
def display_hash_table(hash_table, label="", limit=15):
    print(f"\n{'='*60}")
    print(f"📦 {label} - Hash Table with Size {hash_table.size}")
    print(f"{'='*60}")
    count = 0
    for i, bucket in enumerate(hash_table.table):
        if bucket:
            print(f"[{i:>4}] ➜ {' → '.join(bucket)}")
            count += 1
            if count >= limit:
                remaining = len([b for b in hash_table.table if b]) - limit
                if remaining > 0:
                    print(f"... ({remaining} more non-empty rows hidden)")
                break
    print(f"{'-'*60}\n")

# --- simulation class ---
class ICSimulation:
    def __init__(self, table_sizes, ic_count=1000, rounds=10):
        self.ic_count = ic_count
        self.rounds = rounds
        self.tables = [HashTable(size) for size in table_sizes]
        self.results = defaultdict(list)
        self.total_collisions_per_round = []

    def run(self):
        print("Round |", " | ".join([f"Collisions (size={t.size})" for t in self.tables]), "| Total Collisions")
        print("-" * (10 + 30 * len(self.tables)))

        for r in range(1, self.rounds + 1):
            ic_numbers = [generate_ic() for _ in range(self.ic_count)]
            row_data = [f"{r:>5}"]
            round_total = 0

            for table in self.tables:
                table.reset()
                for ic in ic_numbers:
                    table.insert(ic)
                self.results[table.size].append(table.collisions)
                round_total += table.collisions
                row_data.append(f"{table.collisions:^25}")

                # show sample of hash table only for round 1
                if r == 1:
                    display_hash_table(table, label=f"Round {r} - Table size {table.size}", limit=15)

            self.total_collisions_per_round.append(round_total)
            row_data.append(f"{round_total:^18}")
            print(" | ".join(row_data))

        # summary of averages
        print("\n📊 Total Collisions per Round:")
        for i, total in enumerate(self.total_collisions_per_round, start=1):
            print(f" - Round {i}: {total} total collisions")

        print("\n📊 Average Collisions and Collision Rates Per Table:")
        for table in self.tables:
            avg_collisions = sum(self.results[table.size]) / self.rounds
            collision_rate = (avg_collisions / self.ic_count) * 100
            print(f"\n- Table Size {table.size}:")
            print(f"  Average Collisions per Round: {avg_collisions:.2f}")
            print(f"  Average Collision Rate: {collision_rate:.2f}%")

# --- main execution ---
if __name__ == "__main__":
    table_sizes = [1009, 2003]
    sim = ICSimulation(table_sizes=table_sizes, ic_count=1000, rounds=10)
    sim.run()


