import os
import re

# Konstante für das Base58-Muster
BASE58_PATTERN = r'[13][a-km-zA-HJ-NP-Z0-9]{52}'


def validate_linux_path(path):
    """
    Überprüft, ob der angegebene Pfad ein gültiges und existierendes Linux-Verzeichnis ist.
    """
    return os.path.exists(path) and os.path.isdir(path)


def scan_directory_for_private_keys(start_path):
    """
    Durchsucht das angegebene Verzeichnis rekursiv nach privaten Schlüsseln
    im Base58-Format anhand eines festgelegten Musters.
    """
    found_keys = []

    print(f"Durchsuche Verzeichnis: {start_path}...")
    for root, dirs, files in os.walk(start_path, topdown=True):
        print(f"Verzeichnis: {root}")  # Debugging-Ausgabe

        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    matches = re.findall(BASE58_PATTERN, content.decode('utf-8', errors='ignore'))
                    if matches:
                        print(f"Schlüssel gefunden in Datei: {file_path}")  # Debugging-Ausgabe
                        found_keys.extend(matches)
            except (PermissionError, FileNotFoundError) as e:
                # Fehler beim Zugriff auf die Datei (z. B. Berechtigung verweigert)
                print(f"Überspringe Datei {file_path} aufgrund eines Fehlers ({e}).")
            except Exception as e:
                # Allgemeine Ausnahme behandeln
                print(f"Fehler beim Verarbeiten der Datei {file_path}: {e}")

    return list(set(found_keys))  # Entferne Duplikate


def convert_base58_to_wif(base58_key):
    """
    Konvertiert einen Base58-Privatschlüssel in das WIF-Format.
    """
    prefix = '80' if len(base58_key) == 52 else '00'
    return f"{prefix}{base58_key}"


# Hauptprogramm
start_path = input("Geben Sie einen gültigen Pfad zum Starten der Suche ein (z. B. '/home/user'): ").strip()
if not validate_linux_path(start_path):
    print(f"Ungültiger Pfad: {start_path}")
    exit()

private_keys = scan_directory_for_private_keys(start_path)
if private_keys:
    print("\nGefundene Privatschlüssel:")
    for key in private_keys:
        print(f"Schlüssel: {key}")
        wif_key = convert_base58_to_wif(key)
        print(f"WIF-Version des Schlüssels: {wif_key}")
        print("---")
else:
    print("Keine Privatschlüssel gefunden.")