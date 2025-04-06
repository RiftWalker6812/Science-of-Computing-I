import random

def transform_word(word):
    """Randomly transform characters in a word."""
    transformed = []
    for char in word:
        if random.random() < 0.3:  # 30% chance to transform
            if char.lower() in 'aeios':
                # Replace with symbols or numbers
                replacements = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
                transformed.append(replacements.get(char.lower(), char))
            else:
                # Randomly make uppercase
                transformed.append(char.upper())
        else:
            # Keep the character as is
            transformed.append(char)
    return ''.join(transformed)

def generate_password():
    # Step 1: Input collection
    words = []
    for i in range(3):
        while True:
            word = input(f"Enter word {i + 1} (at least 3 letters): ").strip()
            if len(word) >= 3:
                words.append(word)
                break
            else:
                print("Each word must be at least 3 letters long. Try again.")

    # Step 2: Reorder the words randomly
    random.shuffle(words)

    # Step 3: Transform each word
    transformed_words = [transform_word(word) for word in words]

    # Step 4: Combine the transformed words
    password = ''.join(transformed_words)

    # Step 5: Output the result
    print(f"Generated password: {password}")

# Run the program
if __name__ == "__main__":
    generate_password()