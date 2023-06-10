import os
import shutil
import coverage
from glob import glob

gcovPath = "TOOLS\\MinGW\\bin\\gcov.exe"

# ------------------------------------------------------------------------------
#                               FUNCTIONS
# ------------------------------------------------------------------------------

def clear_screen():
    os.system('cls')

def main_menu(folders):
    clear_screen()
    print("╔════════════════════════════════════════════════╗")
    print("║                    MAIN MENU                   ║")
    print("╠════════════════════════════════════════════════╣")
    for i, folder in enumerate(folders):
        print(f"║  [{i+1}] {folder.ljust(41)} ║")
    print("║  [e] Exit".ljust(49) + "║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    option = input("Select an option: ")
    return option.lower()

def menu(modulo_path):
    total_width = 48
    module = modulo_path.split('\\')[-1]
    text_width = len(module)
    padding = (total_width - text_width) // 2
    while True:
        print("╔════════════════════════════════════════════════╗")
        print("║" + " " * padding + module.center(text_width) + " " * padding + "║")
        print("╠════════════════════════════════════════════════╣")
        print("║  [t] Test".ljust(49) + "║")
        print("║  [d] Debug".ljust(49) + "║")
        print("║  [c] Clean".ljust(49) + "║")
        print("║  [e] Exit".ljust(49) + "║")
        print("╚════════════════════════════════════════════════╝")
        print()

        opcion = input("\nSelect an option: ")
        
        if opcion.lower() == "t":
            print("╔════════════════════════════════════════════════╗")
            print("║                  SCONS REPORT                  ║")
            print("╚════════════════════════════════════════════════╝")
            print("")
            target(modulo_path)
        elif opcion.lower() == "d":
            print("╔════════════════════════════════════════════════╗")
            print("║                  SCONS REPORT                  ║")
            print("╚════════════════════════════════════════════════╝")
            print("")
            debug(modulo_path)
        elif opcion.lower() == "c":
            print("╔════════════════════════════════════════════════╗")
            print("║                  SCONS REPORT                  ║")
            print("╚════════════════════════════════════════════════╝")
            print("")
            clean(modulo_path)
        elif opcion.lower() == "e":
            break
        else:
            input("Wrong option. Enter to continue...")
        

def target(modulo_path):
    os.system("scons -u -f TOOLS/SCONS/SConstruct_target PATH="+modulo_path)
    if os.path.isfile(modulo_path + "/main_target.exe"):
        print("╔════════════════════════════════════════════════╗")
        print("║               UNITY TESTS REPORT               ║")
        print("╚════════════════════════════════════════════════╝")
        print()
        os.system(os.path.join(modulo_path, "main_target.exe")) 

def debug(modulo_path):
    os.system("scons -u -f TOOLS/SCONS/SConstruct_debug PATH="+modulo_path)
    if os.path.isfile(modulo_path + "/main_debug.exe"):
        print("╔════════════════════════════════════════════════╗")
        print("║               UNITY TESTS REPORT               ║")
        print("╚════════════════════════════════════════════════╝")
        print()
        os.system(os.path.join(modulo_path, "main_debug.exe"))
        print("")
        print("╔════════════════════════════════════════════════╗")
        print("║                    COVERAGE                    ║")
        print("╚════════════════════════════════════════════════╝")
        src_files = glob(modulo_path + '/**/*.c', recursive = True)
        gcov_files = glob(modulo_path + '/**/*.c.gcov', recursive = True)
        for f in gcov_files:
            os.remove(f)
        for f in src_files:
            src_file_path, file = f.rsplit("\\", 1)
            os.system(gcovPath + " " + f)
            if os.path.exists(file + ".gcov"):
                shutil.move(file + ".gcov", src_file_path)
        fcoverage(modulo_path)

def clean(modulo_path):
    os.system("scons -f TOOLS/SCONS/SConstruct_target -c PATH="+modulo_path)
    os.system("scons -f TOOLS/SCONS/SConstruct_debug -c PATH="+modulo_path)
    os.system("rmdir /s /q " + modulo_path + "\coverage")

def fcoverage(modulo_path):
    module = modulo_path.split("\\")[-1]
    coverage_dir = os.path.join(modulo_path, "coverage")
    if not os.path.exists(coverage_dir):
        os.makedirs(coverage_dir)
    gcovPathMod = gcovPath.replace("\\","/")
    moduleHTML = coverage_dir + "\\" + module + ".html"
    os.system("gcovr --gcov-executable " + gcovPathMod + " -r " + modulo_path + " --html-details -o " + moduleHTML)

    if os.path.exists(moduleHTML):
        os.system(moduleHTML)

# ------------------------------------------------------------------------------
#                               MAIN
# ------------------------------------------------------------------------------

src_path = "SRC"
module_folders = os.listdir(src_path)
while True:
    select_option = main_menu(module_folders)

    if( select_option == "e" or select_option == "E"):
        break

    if (select_option.isdigit()):
        select_option = int(select_option)-1
        if (0 <= select_option < len(module_folders)):
            select_module = module_folders[select_option]
            modulo_path = os.path.join(src_path, select_module)
            clear_screen()
            menu(modulo_path)
            
            
    else:
        print("Invalid option.")

