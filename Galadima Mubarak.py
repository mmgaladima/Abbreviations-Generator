import re

# Load the letter values from the file
with open('values.txt', 'r') as f:
    letter_values = {line.split()[0]: int(line.split()[1]) for line in f}

def calculate_score(abbr, name):
    score = 0
    words = re.split(r'\W+', name.upper())
    for i in range(1, len(abbr)):
        for word in words:
            if abbr[i] in word:
                if word.index(abbr[i]) == 0:
                    score += 0
                elif word.index(abbr[i]) == len(word) - 1:
                    score += 5 if abbr[i] != 'E' else 20
                else:
                    score += word.index(abbr[i]) + 1 + letter_values[abbr[i]]
    return score

def generate_abbreviations(name):
    # Convert to upper case and remove apostrophes
    name = name.upper().replace("'", "")
    # Split the name into words at non-letter characters
    words = re.split(r'\W+', name)
    abbreviations = []
    for word in words:
        for i in range(1, len(word)):
            for j in range(i+1, len(word)):
                abbr = word[0] + word[i] + word[j]
                abbreviations.append((abbr, calculate_score(abbr, name)))
    return abbreviations

def main():
    input_file = input("Enter the name of the input file: ")
    surname = input("Enter your surname: ")
    output_file = f"{surname}_{input_file.split('.')[0]}_abbrevs.txt"

    with open(input_file, 'r') as f:
        names = f.readlines()

    all_abbreviations = []
    results = {}
    for name in names:
        name = name.strip()
        abbreviations = generate_abbreviations(name)
        all_abbreviations.extend(abbreviations)
        results[name] = abbreviations

    for name, abbreviations in results.items():
        # Filter out abbreviations that appear in more than one name
        abbreviations = [abbr for abbr in abbreviations if all_abbreviations.count(abbr) == 1]
        # If abbreviations list is empty, skip to the next iteration
        if not abbreviations:
            continue
        # Choose the abbreviation(s) with the lowest score
        min_score = min(abbr[1] for abbr in abbreviations)
        results[name] = [abbr[0] for abbr in abbreviations if abbr[1] == min_score]

    with open(output_file, 'w') as f:
        for name, abbreviations in results.items():
            f.write(name + '\n')
            for abbr in abbreviations:
                score = next(abbr_info[1] for abbr_info in all_abbreviations if abbr_info[0] == abbr)
                f.write(f"{abbr} - Score: {score}\n")
            f.write('\n')

if __name__ == "__main__":
    main()

