
from datetime import datetime

# Fő osztályok a Repülőjegy Foglalási Rendszerben
class Jarat():
    def __init__(self, jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas):
        self.jaratszam = jaratszam
        self.indulasi_allomas = indulasi_allomas
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.indulasi_idopont = indulasi_idopont
        self.utas_kapacitas = utas_kapacitas
        self.foglalasok_szama = 0


    def jarat_tipus(self):
        pass

    def display_details(self):
        print(f"Járatszám: {self.jaratszam}")
        print(f"Indulási állomás: {self.indulasi_allomas}")
        print(f"Célállomás: {self.celallomas}")
        print(f"Jegyár: {self.jegyar} Ft")
        print(f"Indulás ideje: {self.indulasi_idopont.strftime('%Y-%m-%d %H:%M')}")
        print(f"Kapacitás: {self.foglalasok_szama}/{self.utas_kapacitas}")

    def van_szabad_hely(self):
        return self.foglalasok_szama < self.utas_kapacitas
        

# Belföldi Járatok osztály
class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas):
        super().__init__(jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas)

    def jarat_tipus(self):
        return "Belföldi Járat"

# Nemzetközi Járatok osztály
class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas):
        super().__init__(jaratszam, indulasi_allomas, celallomas, jegyar, indulasi_idopont, utas_kapacitas)

    def jarat_tipus(self):
        return "Nemzetközi Járat"

# Légitársaság osztály
class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = {}

    def jarat_hozzaadasa(self, jarat):
        if jarat.jaratszam not in self.jaratok:
            self.jaratok[jarat.jaratszam] = jarat
            print(f"Járat {jarat.jaratszam} hozzáadva a {self.nev} légitársasághoz.")
        else:
            print(f"Járat {jarat.jaratszam} már létezik.")

    def jarat_reszletek(self, jaratszam):
        if jaratszam in self.jaratok:
            jarat = self.jaratok[jaratszam]
            print(f"Légitársaság: {self.nev}")
            jarat.display_details()
            print(f"Típus: {jarat.jarat_tipus()}")
        else:
            print(f"Nincs ilyen járat: {jaratszam}.")

# Jegyfoglalási osztály
class JegyFoglalas:
    def __init__(self):
        self.foglalasok = []
        self.not_recommended_destinations = ["War Zone City", "Conflict Region", "Danger Zone", "Kijev", "Tel Aviv"]

    def foglalas(self, jarat, utas):
        if jarat.celallomas in self.not_recommended_destinations:
            print(f"Hiba: A {jarat.celallomas} célállomásra nem lehet foglalni biztonsági okok miatt.")
            return
        
        current_time = datetime.now()
        if current_time >= jarat.indulasi_idopont:
            print(f"Hiba: A {jarat.jaratszam} járat indulása már lejárt. Nem lehet több foglalást végrehajtani.")
            return
        
        if jarat.van_szabad_hely():
            self.foglalasok.append({"jarat": jarat, "utas": utas})
            jarat.foglalasok_szama += 1
            print(f"Jegy foglalva: {utas} számára a {jarat.jaratszam} számú járatra.")
            print(f"Jegyár: {jarat.jegyar} Ft")

            megmaradt_helyek = jarat.utas_kapacitas - jarat.foglalasok_szama
            if megmaradt_helyek == 1:
                print(f"Figyelem: A {jarat.jaratszam} járaton csak egy szabad hely maradt.")
        else:
            print(f"Hiba: A {jarat.jaratszam} járat megtelt. Foglalás nem lehetséges.")

    def foglalas_lista(self):
        if self.foglalasok:
            print("Foglalások listája:")
            for idx, foglalas in enumerate(self.foglalasok, 1):
                jarat = foglalas["jarat"]
                utas = foglalas["utas"]
                print(f"{idx}. Utas: {utas}, Járat: {jarat.jaratszam}, Indulási állomás: {jarat.indulasi_allomas}, Célállomás: {jarat.celallomas}, Indulás: {jarat.indulasi_idopont.strftime('%Y-%m-%d %H:%M')}, Jegyár: {jarat.jegyar} Ft")
        else:
            print("Nincsenek foglalások.")

    def torles(self, jarat, utas):
        existing_reservation = None

        for foglalas in self.foglalasok:
            if foglalas["jarat"] == jarat and foglalas["utas"] == utas:
                existing_reservation = foglalas
                break

        if existing_reservation:
            self.foglalasok.remove(existing_reservation)
            jarat.foglalasok_szama -= 1
            print(f"A {utas} nevű utas foglalása a {jarat.jaratszam} számú járaton törölve lett.")
            return
        print(f"Hiba: A {utas} nevű utas nem rendelkezik foglalással a {jarat.jaratszam} számú járaton.")


if __name__ == "__main__":
    # Légitársaság
    wizzair = LegiTarsasag("WizzAir")

    # Járatok hozzáadása
    jarat1 = BelfoldiJarat("WZ101", "Debrecen", "Budapest", 15000, datetime(2024, 12, 1, 8, 30), 1)
    jarat2 = NemzetkoziJarat("WZ201","Budapest", "London", 50000, datetime(2024, 12, 1, 12, 45), 3)
    jarat3 = BelfoldiJarat("WZ301", "Budapest", "Debrecen", 10000, datetime(2024, 12, 2, 19, 15), 2)
    jarat4 = NemzetkoziJarat("WZ401", "Reykjavik", "London", 90000, datetime(2024, 12, 5, 21, 45), 2)
    jarat5 = NemzetkoziJarat("WZ501", "London", "Párizs", 90000, datetime(2024, 11, 28, 8, 00), 2)
    jarat6 = NemzetkoziJarat("WZ201", "Budapest", "War Zone City", 50000, datetime(2024, 12, 1, 12, 45), 3)

    wizzair.jarat_hozzaadasa(jarat1)
    wizzair.jarat_hozzaadasa(jarat2)
    wizzair.jarat_hozzaadasa(jarat3)
    wizzair.jarat_hozzaadasa(jarat4)
    wizzair.jarat_hozzaadasa(jarat5)
    wizzair.jarat_hozzaadasa(jarat6)

    # Részletek mutatása
    wizzair.jarat_reszletek("WZ101")
    wizzair.jarat_reszletek("WZ201")
    wizzair.jarat_reszletek("WZ301")
    wizzair.jarat_reszletek("WZ401")
    wizzair.jarat_reszletek("WZ501")
    wizzair.jarat_reszletek("WZ601")

    # Foglalások készítése
    foglalas_rendszer = JegyFoglalas()
    foglalas_rendszer.foglalas(jarat1, "Lapos Jocóka")
    foglalas_rendszer.foglalas(jarat2, "Fancy Ursula")
    foglalas_rendszer.foglalas(jarat3, "Pici Ubulka")
    foglalas_rendszer.foglalas(jarat4, "Vén Tengeri Medve")
    foglalas_rendszer.foglalas(jarat4, "Jack Sparrow kapitány")
    foglalas_rendszer.foglalas(jarat1, "Bömbölő Bika")
    foglalas_rendszer.foglalas(jarat5, "Mindig elkések Bömbi")
    foglalas_rendszer.foglalas(jarat6, "Terminator")

    # Foglalások törlése
    foglalas_rendszer.torles(jarat1, "Lapos Jocóka")

    # Testing
    foglalas_rendszer.torles(jarat1, "Bolyhos Nyuszitappancs")

        # Foglalások listázása
    foglalas_rendszer.foglalas_lista()
