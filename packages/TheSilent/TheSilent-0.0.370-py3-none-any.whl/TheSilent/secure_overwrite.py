import os
from TheSilent.clear import clear

CYAN = "\033[1;36m"
RED = "\033[1;31m"

# securely destroys data
def secure_overwrite(device):
    clear()

    if os.path.isfile(device):
        try:
            size = os.path.getsize(device)
            for i in range(1, 8):
                clear()
                print(CYAN + "pass: " + str(i))
                with open(device, "wb") as file:
                    for byte in range(size):
                        file.seek(byte)
                        file.write(b"0")

        except PermissionError:
            print(RED + "ERROR! Permission denied!")
            exit()

        except OSError:
            pass

    if os.path.isdir(device):
        for i in range(1, 8):
            clear()
            print(CYAN + "pass: " + str(i))
            for path, directories, files in os.walk(device,  topdown=True):
                for directory in directories:
                    file_path = os.listdir(path + "/" + directory)
                    for file in file_path:
                        file_path = path + "/" + directory + "/" + file
                        if os.path.isfile(file_path):
                            try:
                                size = os.path.getsize(file_path)
                                print(CYAN + file_path)
                                with open(file_path, "wb") as f:
                                    for byte in range(size):
                                        f.seek(byte)
                                        f.write(b"0")

                            except PermissionError:
                                print(RED + "ERROR! Permission denied!")
                                continue

    print(CYAN + device)
    print(CYAN + "done")
