import platform
try:    
    from pip import get_installed_distributions
    installed_packages = get_installed_distributions()
except ImportError as e: 
    try:
        from pip._internal.utils.misc import get_installed_distributions
        installed_packages = get_installed_distributions()
    except ImportError as e:
        import pkg_resources
        installed_packages = [d for d in pkg_resources.working_set]

depend_python_version = "3.10.12"

depend_packages = (
    ("pyserial", "3.5"),
    ("psutil", "5.9.5"),
    ("keyboard", "0.13.5"),
    ("notebook", "Any"),
    ("matplotlib", "3.7.2"),
    ("Pillow", "10.0.0"),
    ("tensorflow", "2.13.0"),
    ("opencv-python", "4.8.0.74"),
    ("playsound", "1.3.0"),
    ("gtts", "2.3.2"),
    ("SpeechRecognition", "3.10.0"),
    ("PyAudio", "0.2.13")
)
is_installed = []

for depack in depend_packages:
    for inpack in installed_packages:
        if depack[0].lower() == inpack.project_name.lower():
            if depack[1] == "Any" or depack[1] == inpack.version:
                # code 0
                is_installed.append((0, inpack.project_name, inpack.version))
                break
            else:
                # code 1
                is_installed.append((1, inpack.project_name, depack[1], inpack.version))
                break
    else:
        # code 2
        is_installed.append((2, depack[0], depack[1]))

checked_all = True
checked_all = (platform.python_version() == depend_python_version) and checked_all
if checked_all:
    print("Python Version: O (Installed: {})".format(platform.python_version()))
else: 
    print("Python Version: X (Installed: {}, Dependent: {})".format(platform.python_version(), depend_python_version))

for code in is_installed:
    checked_all = (code[0] == 0) and checked_all
    if code[0] == 0:
        print("Package: '{}', Installed: O, Version: O (Installed: {})".format(*code[1:]))
    elif code[0] == 1:
        print("Package: '{}', Installed: O, Version: X (Dependent: {}, Installed: {})".format(*code[1:]))
    elif code[0] == 2:
        print("Package: '{}', Installed: X, Version: X (Dependent: {})".format(*code[1:]))

if checked_all:
    print("Python and all dependent packages are installed with the right version. Success!")
else:
    print("Python or some dependent packages have problem. This may cause unexpected errors.")