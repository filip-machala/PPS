import cups


def main():
    filename = '/home/filip/Desktop/Test.pdf'
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        print(printer, printers[printer]["device-uri"])
        printer_name = printers[printer]["printer-info"]
        print(printer_name)
        printer_name = "HP_LaserJet_P2055dn"
        print(printers.keys())
        conn.printFile(printer_name, filename, "Python_Status_print", {})


if __name__=="__main__":
    main()