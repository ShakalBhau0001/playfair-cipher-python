from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
import string

console = Console()


def build_matrix(keyword, merge_choice):
    keyword = keyword.upper().replace(" ", "")
    remove_letter = "J" if merge_choice == "I" else "I"

    seen = set()
    key_string = ""

    for ch in keyword:
        if ch == remove_letter:
            ch = merge_choice
        if ch not in seen and ch.isalpha():
            seen.add(ch)
            key_string += ch

    for ch in string.ascii_uppercase:
        if ch == remove_letter:
            continue
        if ch not in seen:
            seen.add(ch)
            key_string += ch

    matrix = [list(key_string[i : i + 5]) for i in range(0, 25, 5)]
    return matrix


def preprocess_text(text, merge_choice):
    text = text.upper().replace(" ", "")
    replace_letter = "J" if merge_choice == "I" else "I"
    text = text.replace(replace_letter, merge_choice)

    pairs = []
    i = 0

    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "X"

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

        if r1 == r2:
            cipher += matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]
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


def display_matrix(matrix):
    table = Table(title="🔑 Key Matrix", show_header=False)

    for _ in range(5):
        table.add_column(justify="center")

    for row in matrix:
        table.add_row(*row)

    console.print(table)


def main():
    console.clear()
    console.print(
        Panel.fit(
            "[bold cyan]🔐 Playfair Cipher Tool[/bold cyan]",
            border_style="cyan",
        )
    )

    keyword = Prompt.ask("\n[bold yellow]Enter keyword[/bold yellow]")
    merge_choice = Prompt.ask(
        "[bold yellow]Merge I/J as which letter?[/bold yellow]",
        choices=["I", "J"],
        default="I",
    )

    matrix = build_matrix(keyword, merge_choice)
    console.print()
    display_matrix(matrix)
    mode = Prompt.ask(
        "\n[bold yellow]Choose mode[/bold yellow]", choices=["E", "D"], default="E"
    )

    message = Prompt.ask("[bold yellow]Enter message[/bold yellow]")
    pairs = preprocess_text(message, merge_choice)

    if mode == "E":
        result = encrypt(matrix, pairs)
        title = "Encrypted Message"
        style = "bold green"
    else:
        result = decrypt(matrix, pairs)
        title = "Decrypted Message"
        style = "bold magenta"

    console.print(
        Panel(f"[{style}]{result}[/{style}]", title=f" {title}", border_style="blue")
    )


if __name__ == "__main__":
    main()
