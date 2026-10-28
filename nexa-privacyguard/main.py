"""Interface de terminal do NEXA PrivacyGuard."""

from privacy_guard import mask_text, scan_text


def main() -> None:
    print("NEXA PrivacyGuard")
    print("Cole o texto que deseja analisar.")
    print("Digite uma linha contendo apenas FIM para concluir.\n")

    lines: list[str] = []

    while True:
        try:
            line = input()
        except EOFError:
            break

        if line.strip().casefold() == "fim":
            break

        lines.append(line)

    original = "\n".join(lines)

    if not original.strip():
        print("\nNenhum texto informado.")
        return

    findings = scan_text(original)
    masked = mask_text(original)

    print(f"\nOcorrências identificadas: {len(findings)}")

    if findings:
        categories = sorted({item.category for item in findings})
        print("Categorias: " + ", ".join(categories))
    else:
        print("Nenhum padrão conhecido foi identificado.")

    print("\n--- Texto mascarado ---")
    print(masked)


if __name__ == "__main__":
    main()
