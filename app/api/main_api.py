import os
import json
import random
from flask import Flask, jsonify, request

app = Flask(__name__)

# Function to write DNA data to a file
def write_dna_to_file(dna, filename):
    data = dna
    with open(filename, 'w') as f:
        f.write(data)

# Function to save generated sequences to a file
def save_sequences_to_file(sequences, filename):
    with open(filename, 'w') as f:
        for seq in sequences:
            f.write(seq + '\n')

# Function to generate a random DNA sequence of a given length
def generate_dna_sequence(length):
    bases = ['A', 'C', 'G', 'T']
    sequence = ''.join(random.choices(bases, k=length))
    return sequence

# Function to generate DNA sequences
def generate_sequences(num_sequences, min_length, max_length):
    sequences = []
    for _ in range(num_sequences):
        seq_length = random.randint(min_length, max_length)
        seq = generate_dna_sequence(seq_length)
        sequences.append(seq)
    return sequences

# Function to find the longest common subsequence (LCS) between two DNA sequences
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

    max_lcs_length = 0
    relevant_dna = ""

    with open(file2, 'r') as f2:
        lines = f2.readlines()

        for line in lines:
            seq2 = line.strip()
            lcs = find_lcs(seq1, seq2)

            if len(lcs) > max_lcs_length:
                max_lcs_length = len(lcs)
                relevant_dna = seq2

    with open("files/output.json", 'w') as output_file:
        for line in lines:
            seq2 = line.strip()
            lcs = find_lcs(seq1, seq2)
            output_file.write(f"{seq1}\t{seq2}\t{lcs}\n")

    if relevant_dna:
        print("Most relevant DNA sequence:", relevant_dna)
    else:
        print("No relevant DNA sequence found.")

    return relevant_dna

@app.route('/dna', methods=['GET'])
def get_dna():
    file_path = "files/file1.json"

    # Create random DNA sequence of length 4
    dna = generate_dna_sequence(4)
    # Save the DNA sequence in file1.json
    write_dna_to_file(dna, file_path)

    return jsonify({'dna': dna})

@app.route('/generate', methods=['GET'])
def generate_sequences_route():
    num_sequences = request.args.get('num_sequences', default=10, type=int)
    min_length = request.args.get('min_length', default=10, type=int)
    max_length = request.args.get('max_length', default=20, type=int)

    sequences = generate_sequences(num_sequences, min_length, max_length)
    save_sequences_to_file(sequences, "files/file2.json")

    response = {
        'message': f"{num_sequences} DNA sequences have been generated.",
        'sequences': sequences
    }

    return jsonify(response)

@app.route('/find', methods=['GET'])
@app.route('/find', methods=['GET'])
def find_most_relevant_dna():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file1 = os.path.join(script_dir, 'files/file1.json')
    file2 = os.path.join(script_dir, 'files/file2.json')
    relevant_dna = find_relevant_dna(file1, file2)

    if relevant_dna:
        response = {
            'message': 'Most relevant DNA sequence found',
            'relevant_dna': relevant_dna
        }
    else:
        response = {
            'message': 'No relevant DNA sequence found',
            'relevant_dna': None
        }

    return jsonify(response)


@app.route('/', methods=['GET'])
def route_guide():
    response = {
        'routes': [
            {
                'Endpoint': '/dna',
                'Method': 'GET',
                'Description': 'Retrieve the current DNA sequence'
            },
            {
                'Endpoint': '/generate',
                'Method': 'GET',
                'Description': 'Generate DNA sequences and save them to file2.json'
            },
            {
                'Endpoint': '/find',
                'Method': 'GET',
                'Description': 'Find the most relevant DNA sequence based on LCS'
            },
            {
                'Endpoint': '/clear',
                'Method': 'GET',
                'Description': 'Clear the cache by removing file1.json, file2.json, and output.txt'
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=8085)
