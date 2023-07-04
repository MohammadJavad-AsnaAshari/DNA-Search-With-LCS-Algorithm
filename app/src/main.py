import random
import os


def find_lcs(seq1, seq2):
    m = len(seq1)
    n = len(seq2)

    # Create a table to store the lengths of LCS
    table = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the table in a bottom-up manner
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if seq1[i - 1] == seq2[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])

    # Retrieve the LCS from the table
    lcs = ""
    i, j = m, n
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            lcs = seq1[i - 1] + lcs
            i -= 1
            j -= 1
        elif table[i - 1][j] > table[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs


def find_relevant_dna(file1, file2):
    with open(file1, 'r') as f1:
        seq1 = f1.read().strip()

    relevant_dna = ""
    exact_match_found = False

    with open(file2, 'r') as f2:
        lines = f2.readlines()

        for line in lines:
            seq2 = line.strip()
            n = len(seq2)

            if seq1 == seq2:
                exact_match_found = True
                relevant_dna = seq2
                break

            lcs = find_lcs(seq1, seq2)
            if len(lcs) > len(relevant_dna):
                relevant_dna = seq2

    with open("files/output.txt", 'w') as output_file:
        for line in lines:
            seq2 = line.strip()
            n = len(seq2)
            lcs = find_lcs(seq1, seq2)
            output_file.write(f"{seq1}\t{seq2}\t{lcs}\n")

    if exact_match_found:
        print("Exact match found in the second file.")
    else:
        print("No exact match found.")

    print("Most relevant DNA sequence:", relevant_dna)


def write_dna_to_file(dna, filename):
    with open(filename, 'w') as f:
        f.write(dna)


def generate_random_sequence(length):
    nucleotides = ['A', 'C', 'G', 'T']
    sequence = ''.join(random.choice(nucleotides) for _ in range(length))
    return sequence


def generate_sequences(num_sequences):
    sequences = []
    for _ in range(num_sequences):
        length = random.randint(5, 100)
        sequence = generate_random_sequence(length)
        sequences.append(sequence)
    return sequences


def save_sequences_to_file(sequences, filename):
    with open(filename, 'w') as f:
        for sequence in sequences:
            f.write(sequence + '\n')


# Prompt the user for input
dna = input("Enter a DNA: ")

# Write the user's input to file1.txt if it doesn't exist
file1 = "files/file1.txt"
if not os.path.exists(file1):
    write_dna_to_file(dna, file1)
    print(f"{file1} created and {dna} written to it.")
else:
    print(f"{file1} already exists.")

# Generate and save DNA sequences to file2.txt if it doesn't exist
file2 = "files/file2.txt"
if not os.path.exists(file2):
    num_sequences = int(input("Enter the number of sequences to generate: "))
    sequences = generate_sequences(num_sequences)
    save_sequences_to_file(sequences, file2)
    print(f"{file2} created and {num_sequences} DNA sequences have been generated and saved to it.")
else:
    print(f"{file2} already exists.")

# Find the relevant DNA sequence
find_relevant_dna(file1, file2)

# Ask the user if they want to clear the cache
clear_cache = input("Do you want to clear the cache? (yes/no): ")
if clear_cache.lower() == "yes":
    # Delete file1.txt, file2.txt, and output.txt if they exist
    files_to_delete = [file1, file2, "files/output.txt"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"{file} deleted.")
else:
    print("Cache not cleared.")
