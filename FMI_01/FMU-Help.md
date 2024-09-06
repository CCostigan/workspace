

# Functional Mock-up Interface Specification
  https://fmi-standard.org/docs/3.0/

# PythonFMU and PythonFMU3 - Generate FMU from Python code
  * version 2
    https://github.com/NTNU-IHB/PythonFMU
  * version 3
    https://github.com/stephensmith25/PythonFMU3

    https://pythonfmu3.readthedocs.io/en/stable/usage/

# FMPy - Run Models in Python
  https://fmpy.readthedocs.io/en/latest/tutorial/

# Modelon link & guide
  https://github.com/modelon-community

# CATIA is the new name for Cameo 
  * Convert Python to FMU
    https://github.com/CATIA-Systems/FMPy/tree/main
  * Connect Unity to FMI (Cameo?)  Directly?              <--- Windows only?  >
    https://github.com/CATIA-Systems/Unity-FMI-Addon

# Build "OpenModelica" locally - aka the Massive Rabbit Hole
  * Build OpenModelica
    https://github.com/OpenModelica

    Add to CMakeLists.txt (I put it aftert the CMAKE_MODULE_PATH line)
      set(OM_USE_CCACHE off)
    Install Fortran
      sudo apt install gfortran
    Install some other garbage Basic Linear Algebra
      sudo apt install -y libopenblas-dev
    And naturally it needs some fucking BOOST library, do we need all of these???
      sudo apt install libboost-system-dev libboost-thread-dev libboost-program-options-dev #libboost-test-dev
      sudo apt install libboost-filesystem-dev
    Could NOT find CURL (missing: CURL_LIBRARY CURL_INCLUDE_DIR)
      sudo apt install curl libcurl4-openssl-dev
      sudo apt install libssl-dev
    Readline
      sudo apt-get install libreadline-dev
    qt5?  srsly?
    *Fucking gave up at this point.  Don't fucking force me to install a whole SHIT IDE from Europe just to build this piece of shit*
    *Qt is GARBAGE.  I tried Qt and it sucked. Else I would be uising it rigth now*
    *They just didn't want to make it an Eclipse project, cause that Modella asshole already fucked that up beyond repair with v5*
      sudo apt install libqt5svg5-dev
      apt list | grep "libqt5web.*/"
      sudo apt install libqt5webkit5-dev
      sudo apt install libqt5xmlpatterns5-dev
      sudo apt install libopenscenegraph-dev
      OMG finally done.  What was I building again?


# Link for FMUSDK if you'd rather do this in C
https://stackoverflow.com/questions/44964787/how-to-export-c-file-function-to-fmu-using-fmusdk

# Tutorial link
https://pythonfmu3.readthedocs.io/en/stable/usage/
https://pythonfmu3.readthedocs.io/en/latest/usage/

# Java
https://github.com/NTNU-IHB/FMI4j

# WTF is Vico?
https://github.com/NTNU-IHB/Vico


# Unrelated:  maybe?  learn how Unity uses FMI
https://unity.com/
# Unrelated: GLFW CMake not working
https://discourse.glfw.org/t/glfw-on-linux-cmake-finds-no-libraries/2733/4


##### COMMAND SYNTAX #####

# pythonfmu build -h 

usage: pythonfmu build [-h] -f SCRIPT_FILE [-d DEST]
                       [--doc DOCUMENTATION_FOLDER] [--no-external-tool]
                       [--no-variable-step] [--interpolate-inputs]
                       [--only-one-per-process] [--handle-state]
                       [--serialize-state]
                       [Project files ...]

Build an FMU from a Python script.

positional arguments:
  Project files         Additional project files required by the Python
                        script.

options:
  -h, --help            show this help message and exit
  -f SCRIPT_FILE, --file SCRIPT_FILE
                        Path to the Python script.
  -d DEST, --dest DEST  Where to save the FMU.
  --doc DOCUMENTATION_FOLDER
                        Documentation folder to include in the FMU.
  --no-external-tool    If given, needsExecutionTool=false
  --no-variable-step    If given, canHandleVariableCommunicationStepSize=false
  --interpolate-inputs  If given, canInterpolateInputs=true
  --only-one-per-process
                        If given, canBeInstantiatedOnlyOncePerProcess=true
  --handle-state        If given, canGetAndSetFMUstate=true
  --serialize-state     If given, canSerializeFMUstate=true


# pythonfmu deploy -h 

usage: pythonfmu deploy [-h] -f FMU [-e ENVIRONMENT] [{pip,conda}]

Deploy a Python FMU. The command will look in the `resources` folder for one
of the following files: `requirements.txt` or `environment.yml`. If you
specify a environment file but no package manager, `conda` will be selected
for `.yaml` and `.yml` otherwise `pip` will be used. The tool assume the
Python environment in which the FMU should be executed is the current one.

positional arguments:
  {pip,conda}           Python packages manager

options:
  -h, --help            show this help message and exit
  -f FMU, --file FMU    Path to the Python FMU.
  -e ENVIRONMENT, --env ENVIRONMENT
                        Requirements or environment file.


# pythonfmu buildcsv -h 

usage: pythonfmu buildcsv [-h] -f CSV_FILE [-d DEST]
                          [--doc DOCUMENTATION_FOLDER] [--no-external-tool]
                          [--no-variable-step] [--interpolate-inputs]
                          [--only-one-per-process] [--handle-state]
                          [--serialize-state]

Build an FMU from a CSV file.

options:
  -h, --help            show this help message and exit
  -f CSV_FILE, --file CSV_FILE
                        Path to the CSV file.
  -d DEST, --dest DEST  Where to save the FMU.
  --doc DOCUMENTATION_FOLDER
                        Documentation folder to include in the FMU.
  --no-external-tool    If given, needsExecutionTool=false
  --no-variable-step    If given, canHandleVariableCommunicationStepSize=false
  --interpolate-inputs  If given, canInterpolateInputs=true
  --only-one-per-process
                        If given, canBeInstantiatedOnlyOncePerProcess=true
  --handle-state        If given, canGetAndSetFMUstate=true
  --serialize-state     If given, canSerializeFMUstate=true
