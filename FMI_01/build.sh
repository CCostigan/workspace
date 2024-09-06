#!/bin/bash

# Nice cleanup idea
# https://stackoverflow.com/questions/4632028/how-to-create-a-temporary-directory

cwdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -ne 1 ] ; then
    echo "Wrong number of arguments.  "
    exit 1
fi
echo "Right number of arguments.  "
tempdir=`mktemp -d -t Delete-XXXX`

if [[ ! "${tempdir}" || ! -d "${tempdir}" ]]; then
  echo "Could not create temp dir"
  exit 1
fi

# deletes the temp directory
function cleanup {      
  rm -rf "${tempdir}"
  echo "...Deleted temp working directory ${tempdir}"
}
# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

# Need to use * because it seems like the case sometimes gets changed when making an FMU file
buildcommand="pythonfmu build -f Scratchpad/${1}.py -d ${tempdir} && fmpy validate ${tempdir}/*.fmu && cp ${tempdir}/*.fmu ${cwdir}"
#    pythonfmu build -f Scratchpad/${1}.py -d Scratchpad/ && fmpy validate Scratchpad/${1}.fmu
echo "Executing: ${buildcommand}"
pythonfmu build -f Scratchpad/${1}.py -d ${tempdir}

if [ $? -eq 0 ] ; then
  # echo "Processing file at ${tempdir}"
  # ls -lrt ${tempdir}
  fmpy validate ${tempdir}/*.fmu 
fi

if [ $? -eq 0 ] ; then
  # echo "Copying file from ${tempdir} to ${cwdir}"
  cp ${tempdir}/* ${cwdir}
fi


# Delete all fmu files just in case
# find . -name "*.fmu" -exec rm {} \;

# Run the GUI
# python3 -m fmpy.gui &


