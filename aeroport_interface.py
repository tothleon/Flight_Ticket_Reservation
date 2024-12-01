from aeroport import LegiTarsasag, JegyFoglalas, BelfoldiJarat, NemzetkoziJarat
from datetime import datetime

ADMIN_PASSWORD = "admin"

def admin_menu(foglalas_rendszer, wizzair):
    while True:
        print("\nAdmin Menü")
        print("1. Új járat hozzáadása")
        print("2. Foglalások megtekintése")
        print("3. Vissza a főmenübe")

        choice = input("> ").strip()

        if choice == "1":  # Adjon hozzá uj járatot
            print("\nÚj járat hozzáadása\n------------------")
            try:
                jaratszam = input("Járatszám: ").strip()
                indulasi_allomas = input("Indulási állomás: ").strip()
                celallomas = input("Célállomás: ").strip()
                jegyar = int(input("Jegyár (Ft): ").strip())
                indulasi_idopont = datetime.strptime(input("Indulás ideje (YYYY-MM-DD HH:MM): ").strip(), "%Y-%m-%d %H:%M")
                utas_kapacitas = int(input("Kapacitás: ").strip())

                if input("Nemzetközi járat? (igen/nem): ").strip().lower() == "igen":
                    new_flight = NemzetkoziJarat(jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas)
                else:
                    new_flight = BelfoldiJarat(jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas)

                wizzair.jarat_hozzaadasa(new_flight)
            except Exception as e:
                print(f"Hiba történt: {e}")

        elif choice == "2":  # Foglalások megtekintése
            print("\nFoglalások megtekintése\n----------------------")
            if not foglalas_rendszer.foglalasok:
                print("Nincsenek aktív foglalások.")
            else:
                print("Jelenlegi foglalások:")
                for idx, foglalas in enumerate(foglalas_rendszer.foglalasok, 1):
                    jarat = foglalas["jarat"]
                    utas = foglalas["utas"]
                    print(f"{idx}. Utas: {utas}, Járat: {jarat.jaratszam}, "
                          f"Indulási állomás: {jarat.indulasi_allomas}, Célállomás: {jarat.celallomas}, "
                          f"Indulás: {jarat.indulasi_idopont.strftime('%Y-%m-%d %H:%M')}, Jegyár: {jarat.jegyar} Ft")

        elif choice == "3":  # Vissza a főmenühöz
            break
        else:
            print("Hiba: Kérjük, válasszon érvényes lehetőséget (1, 2 vagy 3).")


def passenger_menu(foglalas_rendszer, wizzair):
    while True:
        print("\nÜdvözöljük a Légitársaság Foglalási Rendszerében!")
        print("------------------------------------------------")
        print("Lehetőségek:")
        print("1. Foglalás készítése")
        print("2. Foglalás lemondása")
        print("3. Foglalások megtekintése")
        print("4. Vissza a főmenübe")

        choice = input("> ").strip()

        if choice == "1":  # Foglalás végrehajtása
            print("\nFoglalás készítése\n------------------")

            current_time = datetime.now()
            available_flights = [jarat for jarat in wizzair.jaratok.values() if jarat.indulasi_idopont > current_time]

            if available_flights:
                print("Elérhető járatok:")
                for idx, jarat in enumerate(available_flights, 1):
                    print(f"{idx}. {jarat.jaratszam} - {jarat.indulasi_allomas} -> {jarat.celallomas}, "
                          f"Indulás: {jarat.indulasi_idopont.strftime('%Y-%m-%d %H:%M')}, "
                          f"Jegyár: {jarat.jegyar} Ft, Kapacitás: {jarat.foglalasok_szama}/{jarat.utas_kapacitas}")
            else:
                print("Nincsenek elérhető járatok.")
                continue

            jarat_szam = input("\nAdja meg a járatszámot a foglaláshoz: ").strip()
            if jarat_szam not in wizzair.jaratok:
                print(f"Hiba: Nincs ilyen járatszám ({jarat_szam}).")
                continue

            jarat = wizzair.jaratok[jarat_szam]
            print("Adja meg az utas nevét:")
            utas_nev = input("> ").strip()

            foglalas_rendszer.foglalas(jarat, utas_nev)

        elif choice == "2":  # Foglallás lemondása
            print("\nFoglalás lemondása\n-----------------")
            if not foglalas_rendszer.foglalasok:
                print("Nincsenek foglalások, amelyeket le lehetne mondani.")
                continue

            print("Jelenlegi foglalások:")
            for idx, foglalas in enumerate(foglalas_rendszer.foglalasok, 1):
                jarat = foglalas["jarat"]
                utas = foglalas["utas"]
                print(f"{idx}. Utas: {utas}, Járat: {jarat.jaratszam}, "
                      f"Indulási állomás: {jarat.indulasi_allomas}, Célállomás: {jarat.celallomas}")

            try:
                cancel_idx = int(input("\nAdja meg a lemondani kívánt foglalás számát: ").strip()) - 1
                if 0 <= cancel_idx < len(foglalas_rendszer.foglalasok):
                    reservation = foglalas_rendszer.foglalasok[cancel_idx]
                    foglalas_rendszer.torles(reservation["jarat"], reservation["utas"])
                else:
                    print("Hiba: Érvénytelen foglalás szám.")
            except ValueError:
                print("Hiba: Kérjük, adjon meg egy érvényes számot.")

        elif choice == "3":  # Foglalások megtekintése
            print("\nFoglalások megtekintése\n----------------------")
            if not foglalas_rendszer.foglalasok:
                print("Nincsenek aktív foglalások.")
            else:
                print("Jelenlegi foglalások:")
                for idx, foglalas in enumerate(foglalas_rendszer.foglalasok, 1):
                    jarat = foglalas["jarat"]
                    utas = foglalas["utas"]
                    print(f"{idx}. Utas: {utas}, Járat: {jarat.jaratszam}, "
                          f"Indulási állomás: {jarat.indulasi_allomas}, Célállomás: {jarat.celallomas}, "
                          f"Indulás: {jarat.indulasi_idopont.strftime('%Y-%m-%d %H:%M')}, Jegyár: {jarat.jegyar} Ft")

        elif choice == "4":  # Vissza a főmenühöz
            break
        else:
            print("Hiba: Kérjük, válasszon érvényes lehetőséget (1, 2, 3 vagy 4).")



def start_terminal_interface():
    foglalas_rendszer = JegyFoglalas()
    wizzair = LegiTarsasag("WizzAir")

    jarat1 = BelfoldiJarat("WZ101", "Debrecen", "Budapest", 15000, datetime(2024, 12, 1, 8, 30), 10)
    jarat2 = NemzetkoziJarat("WZ201","Budapest", "London", 50000, datetime(2024, 12, 1, 12, 45), 5)
    jarat3 = BelfoldiJarat("WZ301", "Budapest", "Debrecen", 10000, datetime(2024, 12, 2, 19, 15), 6)
    jarat4 = NemzetkoziJarat("WZ401", "Reykjavik", "London", 90000, datetime(2024, 12, 5, 21, 45), 2)
    jarat5 = NemzetkoziJarat("WZ501", "London", "Párizs", 90000, datetime(2024, 11, 28, 8, 00), 2)
    jarat6 = NemzetkoziJarat("WZ601", "Budapest", "War Zone City", 50000, datetime(2024, 12, 1, 12, 45), 3)

    wizzair.jarat_hozzaadasa(jarat1)
    wizzair.jarat_hozzaadasa(jarat2)
    wizzair.jarat_hozzaadasa(jarat3)
    wizzair.jarat_hozzaadasa(jarat4)
    wizzair.jarat_hozzaadasa(jarat5)
    wizzair.jarat_hozzaadasa(jarat6)

    foglalas_rendszer.foglalas(jarat1, "Lapos Jocóka")
    foglalas_rendszer.foglalas(jarat2, "Fancy Ursula")
    foglalas_rendszer.foglalas(jarat3, "Pici Ubulka")
    foglalas_rendszer.foglalas(jarat4, "Vén Tengeri Medve")
    foglalas_rendszer.foglalas(jarat4, "Jack Sparrow kapitány")
    foglalas_rendszer.foglalas(jarat1, "Bömbölő Bika")
    foglalas_rendszer.foglalas(jarat5, "Mindig elkések Bömbi")
    foglalas_rendszer.foglalas(jarat6, "Terminator")

    while True:
        print("\n Üdvözlünk a légitársaság honlapján!")
        print("\nKérjük, válassza ki a felhasználói típusát:")
        print("1. Utas")
        print("2. Adminisztrátor")
        print("3. Kilépés")

        choice = input("> ").strip()

        if choice == "1":
            passenger_menu(foglalas_rendszer, wizzair)
        elif choice == "2":
            password = input("Adja meg az adminisztrátori jelszót: ").strip()
            if password == ADMIN_PASSWORD:
                admin_menu(foglalas_rendszer, wizzair)
            else:
                print("Hiba: Érvénytelen jelszó.")
        elif choice == "3":
            print("\nKöszönjük, hogy a Légitársaság Foglalási Rendszerét használta. Viszlát!")
            break
        else:
            print("Hiba: Kérjük, válasszon érvényes lehetőséget (1, 2 vagy 3).")


# CLI inditása
if __name__ == "__main__":
    start_terminal_interface()
