import cups


def main():
    filename = '/home/filip/Desktop/test.pdf'
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        # print printer, printers[printer]["device-uri"]
        printer_name = printers.keys()[0]
        conn.printFile(printer_name, filename, "Python_Status_print", {})

if __name__=="__main__":
    main()