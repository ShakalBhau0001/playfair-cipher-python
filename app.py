import string


def build_matrix(keyword, merge_choice):
    keyword = keyword.upper().replace(" ", "")

    # Determine which letter to remove
    remove_letter = "J" if merge_choice == "I" else "I"

    seen = set()
    key_string = ""

    # Processing keyword
    for ch in keyword:
        if ch == remove_letter:
            ch = merge_choice
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            key_string += ch

    # Adding remaining alphabet into the 5x5 matrix
    for ch in string.ascii_uppercase:
        if ch == remove_letter:
            continue
        if ch not in seen:
            seen.add(ch)
            key_string += ch

    # Creating 5x5 matrix
    matrix = [list(key_string[i : i + 5]) for i in range(0, 25, 5)]
    return matrix


def preprocess_text(text, merge_choice):
    text = text.upper().replace(" ", "")

    # Apply merging rule for "I" and "J"
    replace_letter = "J" if merge_choice == "I" else "I"
    text = text.replace(replace_letter, merge_choice)

    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        b = ""

        if i + 1 < len(text):
            b = text[i + 1]
        else:
            b = "X"

        if a == b:
            pairs.append(a + "X")
            i += 1
        else:
            pairs.append(a + b)
            i += 2

    if len(pairs[-1]) == 1:
        pairs[-1] += "X"

    return pairs


def find_position(matrix, letter):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == letter:
                return r, c


def encrypt(matrix, pairs):
    cipher = ""

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        # Same row
        if r1 == r2:
            cipher += matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r2][(c2 + 1) % 5]

        # Same column
        elif c1 == c2:
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]

        # Rectangle rule
        else:
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]

    return cipher


def decrypt(matrix, pairs):
    plain = ""

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plain += matrix[r1][(c1 - 1) % 5]
            plain += matrix[r2][(c2 - 1) % 5]

        elif c1 == c2:
            plain += matrix[(r1 - 1) % 5][c1]
            plain += matrix[(r2 - 1) % 5][c2]

        else:
            plain += matrix[r1][c2]
            plain += matrix[r2][c1]

    return plain


print("\n--- Playfair Cipher ---\n")

keyword = input("Enter keyword: ")

merge_choice = input("Merge I/J as which letter? (I or J): ").upper()
while merge_choice not in ["I", "J"]:
    merge_choice = input("Please enter I or J: ").upper()

matrix = build_matrix(keyword, merge_choice)

print("\nKey Matrix:")
for row in matrix:
    print(row)

mode = input("\nEncrypt or Decrypt Press (E/D): ").upper()
message = input("Enter Message: ")

pairs = preprocess_text(message, merge_choice)

if mode == "E":
    result = encrypt(matrix, pairs)
    print("\nEncrypted Message:", result)

elif mode == "D":
    result = decrypt(matrix, pairs)
    print("\nDecrypted Message:", result)

else:
    print("Invalid mode selected.")
