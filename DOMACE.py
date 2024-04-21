import pytz
import datetime


def raisecom():
    """Vygeneruje prikazy a ostatne veci pre domace raisecom"""

    local = datetime.date.today()

    print("sh int gpon-onu creation-information | i {}".format(local))
    print("show interface gpon-onu online-information")

    print("=" * 50)
    print("UDAJE")

    print("Cislo zmluvy: ", end='')
    zmluva = input()

    print("Meno: ", end='')
    meno = input()

    print("Port: ", end='')
    port = input()

    print("Nic, +, M+ : ", end='')
    zariadenie = input()

    print("sh gpon-onu {} transceiver".format(port))

    print("KONFIGURACIA: Zmena description")
    print("=" * 50)
    print("conf\nint gpon-onu {}\ndescription {}_{}_{}\nend\nwr st".format(port, zmluva, meno, zariadenie))

    print("=" * 50)
    print("MIKROTIK KOMENT:")
    print("{} - ONU {} - {}".format(zmluva, port, meno))
    return


raisecom()