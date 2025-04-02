from itertools import combinations

def create_candidate_itemsets(prev_itemsets, k):

    candidates = set()
    prev_items = list(prev_itemsets)
    
    for i in range(len(prev_items)):
        for j in range(i + 1, len(prev_items)):
            new_set = prev_items[i] | prev_items[j]  
            
            if len(new_set) == k:  
                candidates.add(new_set)

    return candidates

def create_n_freq_itemsets(candidates, transactions, min_support, num_transactions):

    itemset_counts = {itemset: 0 for itemset in candidates}
    for transaction in transactions.values():
        transaction_set = set(transaction)
        for itemset in candidates:
            if itemset.issubset(transaction_set):
                itemset_counts[itemset] += 1
    frequent_itemsets = {itemset: count for itemset, count in itemset_counts.items()
                         if count / num_transactions >= min_support}

    return frequent_itemsets

def create_association_rules(frequent_itemsets, min_confidence):
    association_rules = []
    for itemset, count in frequent_itemsets.items():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):  
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    confidence = count / frequent_itemsets[antecedent]

                    if confidence >= min_confidence:
                        association_rules.append((antecedent, consequent, confidence))

    return association_rules

def apriori(transactions, min_support, min_confidence):
    num_transactions = len(transactions)
    item_counts = {}

    for transaction in transactions.values():
        for item in transaction:
            item_counts[item] = item_counts.get(item, 0) + 1

    frequent_itemsets = {frozenset([item]): count for item, count in item_counts.items()
                         if count / num_transactions >= min_support}

    global_item_counts = frequent_itemsets.copy()  
    k = 2  
    while frequent_itemsets:
        candidates = create_candidate_itemsets(frequent_itemsets.keys(), k)
        new_frequent_itemsets = create_n_freq_itemsets(candidates, transactions, min_support, num_transactions)
        
        if not new_frequent_itemsets:
            break

        frequent_itemsets = new_frequent_itemsets
        global_item_counts.update(frequent_itemsets)  
        k += 1
    association_rules = create_association_rules(global_item_counts, min_confidence)

    return global_item_counts, association_rules

transactions = {
    1: ['A', 'B', 'C'],
    2: ['A', 'B'],
    3: ['A', 'C'],
    4: ['B', 'C'],
    5: ['A', 'B', 'C', 'D'],
}

min_support = 0.4  
min_confidence = 0.6

freq_itemsets, rules = apriori(transactions, min_support, min_confidence)

print("Frequent Itemsets:")
for itemset, count in freq_itemsets.items():
    print(f"{set(itemset)}: {count}")

print("\nAssociation Rules:")
for antecedent, consequent, confidence in rules:
    print(f"{set(antecedent)} → {set(consequent)} (Confidence: {confidence:.2f})")
