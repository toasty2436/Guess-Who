import sys
import os
from subprocess import Popen, PIPE, STDOUT, check_output




def pip_install(module_name: str) -> Popen:
    command = [
        sys.executable,
        '-m',
        'pip',   
        'install',
        '--upgrade',
        '--trusted-host',
        'pypi.org',
        '--trusted-host',
        'files.pythonhosted.org',
        module_name
    ]
    return Popen(command, text=True, stdout=PIPE, stderr=STDOUT)

def pip_uninstall(module_name: str) -> Popen:
    command = [
        sys.executable,
        '-m',
        'pip',
        'uninstall',
        '-y',  
        module_name
    ]
    return Popen(command, text=True, stdout=PIPE, stderr=STDOUT)

def realtime_print(process: Popen) -> str:
    all_output = ''

    while True:
        realtime_output = process.stdout.readline()

        if realtime_output == '' and process.poll() is not None:
            print()  
            break

        if realtime_output:
            print(realtime_output.strip(), flush=True)
            all_output += realtime_output

    return all_output

def get_module_installation_path(module_name: str) -> str:
    command = [
        sys.executable,
        '-m',
        'pip',
        'show',
        module_name
    ]
    output = check_output(command, text=True)
    for line in output.split('\n'):
        if line.startswith('Location:'):
            return line.split(':', 1)[1].strip()
    return "Installation path not found"

if __name__ == '__main__':
    print(f'Using Python executable: "{sys.executable}"\n')

    while True:
        action = input('Choose action: [1] Install | [2] Uninstall | [Q] Quit : ').strip().lower()

        if action == '1':
            # Install
            while True:
                print("------------------")
                module = input('Module to install: ').strip().lower()
                os.system('cls')
                proc = pip_install(module)
                output = realtime_print(proc)

                if 'DO NOT MATCH THE HASHES' in output:
                    print('Hashing error detected, purging the pip cache...')
                    purge_pip_cache()
                    print(f'Pip caches have been purged, attempting to install the module "{module}" again...\n')
                    
                    proc = pip_install(module)
                    output = realtime_print(proc)
                    if 'DO NOT MATCH THE HASHES' in output:
                        print(f'Second attempt to install "{module}" failed due to another hashing error. Maybe try updating '
                              f'pip?\n')

                if "Successfully installed" in output:
                    installation_path = get_module_installation_path(module)
                    print(f'Module "{module}" successfully installed at: {installation_path}')

                if input('Enter [C] To Continue: ').lower() == 'c':
                    os.system('cls')
                    break


        

        elif action == '2':
            # Uninstall
            while True:
                print("------------------")
                module = input('Module to uninstall: ').strip().lower()
                os.system('cls')
                proc = pip_uninstall(module)
                output = realtime_print(proc)

                if input('Enter [C] To Continue : ').lower() == 'c':
                    os.system('cls')
                    break

        

        else:
            print("Invalid action. Please choose [1] for install, [2] for uninstall, or [Q] to quit.")
