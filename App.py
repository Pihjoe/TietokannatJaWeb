import sqlite3

DB = "sovellus.db"


#Tietokanta

def yhteys():
    return sqlite3.connect(DB)


def alusta_tietokanta():
    with yhteys() as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)""")
        c.execute("""CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, content TEXT, FOREIGN KEY (user_id) REFERENCES users(id))""")


#Käyttäjä

def luo_tunnus():
    username = input("Käyttäjänimi: ")
    password = input("Salasana: ")

    try:
        with yhteys() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (x, y)", (username, password))
            print("Onnistui")

    except sqlite3.IntegrityError:
        print("Käyttäjänimi on jo olemassa")


def kirjaudu_sisaan():
    username = input("Käyttäjänimi: ")
    password = input("Salasana: ")

    with yhteys() as conn:
        cur = conn.execute("SELECT id FROM users WHERE username=x AND password=y",(username, password))
        rivi = cur.fetchone()
        if rivi:
            print(f"Tervetuloa")
            tietovalikko(rivi[0])
        else:
            print("Käyttäjä tai salasana virheellinen")


#Tiedot

def hae_tiedot(user_id):
    with yhteys() as conn:
        return conn.execute("SELECT id, content FROM items WHERE user_id = x", (user_id,)).fetchall()


def hae_tiedot_haulla(user_id, hakusana):
    with yhteys() as conn:
        return conn.execute("SELECT id, content FROM items WHERE user_id=? AND content LIKE ?", (user_id, f"%{hakusana}%")).fetchall()


def lisaa_tieto(user_id):
    tieto = input("Uusi tietokohde: ")
    
    with yhteys() as conn:
        conn.execute("INSERT INTO items (user_id, content) VALUES (?, ?)", (user_id, tieto))


def muokkaa_tieto(item_id):
    uusi = input("Uusi sisältö: ")

    with yhteys() as conn:
        conn.execute("UPDATE items SET content=? WHERE id=?", (uusi, item_id))


def poista_tieto(item_id):
    with yhteys() as conn:
        conn.execute("DELETE FROM items WHERE id=?", (item_id,))


#Päävalikko

def paavalikko():
    alusta_tietokanta()

    while True:
        print("\n1 = Luo tunnus")
        print("2 = Kirjaudu sisään")
        print("3 = Lopeta")

        valinta = input("Valitse: ")

        if valinta == "1":
            luo_tunnus()
        elif valinta == "2":
            kirjaudu_sisaan()
        elif valinta == "3":
            print("Heippa!")
            break


# Valikko

def tietovalikko(user_id):
    while True:
        print("\n--- TIETOKOHTEET ---")
        print("1 = Näytä kaikki")
        print("2 = Lisää")
        print("3 = Muokkaa")
        print("4 = Poista")
        print("5 = Hae")
        print("6 = Kirjaudu ulos")

        valinta = input("Valitse: ")

        if valinta == "1":
            tiedot = hae_tiedot(user_id)
            for i, (_, sisältö) in enumerate(tiedot, 1):
                print(f"{i}. {sisältö}")

        elif valinta == "2":
            lisaa_tieto(user_id)

        elif valinta == "3":
            tiedot = hae_tiedot(user_id)
            for i, (_, sisältö) in enumerate(tiedot, 1):
                print(f"{i}. {sisältö}")
            nro = int(input("Muokattava numero: ")) - 1
            if 0 <= nro < len(tiedot):
                muokkaa_tieto(tiedot[nro][0])

        elif valinta == "4":
            tiedot = hae_tiedot(user_id)
            for i, (_, sisältö) in enumerate(tiedot, 1):
                print(f"{i}. {sisältö}")
            nro = int(input("Poistettava numero: ")) - 1
            if 0 <= nro < len(tiedot):
                poista_tieto(tiedot[nro][0])

        elif valinta == "5":
            hakusana = input("Anna hakusana: ")
            tulokset = hae_tiedot_haulla(user_id, hakusana)
            print("Hakutulokset:")
            for i, (_, sisältö) in enumerate(tulokset, 1):
                print(f"{i}. {sisältö}")

        elif valinta == "6":
            print("Uloskirjattu")
            break




paavalikko()