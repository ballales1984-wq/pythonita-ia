# main.py

from controllore import ciclo_di_controllo

def main():
    print("🧠 Benvenuto in Pythonita IA - main.py:6")

    while True:
        frase = input("Scrivi una frase in italiano:\n")
        if frase.lower() == "esci":
            print("👋 Arrivederci da Pythonita! - main.py:11")
            break

        codice = ciclo_di_controllo(frase)

        print("\n🧾 Codice generato:\n - main.py:16")
        print(codice)

        salva = input("\n💾 Vuoi salvarlo in output.py? (s/n): ").lower()
        if salva == "s":
            with open("output.py", "w", encoding="utf-8") as f:
                f.write(codice)
            print("✅ Codice salvato in output.py\n - main.py:23")

if __name__ == "__main__":
    main()
