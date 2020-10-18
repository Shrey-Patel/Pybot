#!/bin/bash

pybotpath=$PWD
touch pybot
chmod +rwx pybot
exec 3<> pybot

    echo "#!/bin/bash" >&3
    echo "source $pybotpath/env/bin/activate" >&3
    echo "python $pybotpath/pybotcli/" >&3

exec 3>&-

sudo mv pybot /usr/local/bin/pybot

UNAME=$(uname -s)



# Debian based
if [[ -f "/etc/apt/sources.list" ]]; then
  sudo apt-get install ffmpeg python-pip python-imdbpy python-notify2
  sudo apt-get install python-dbus python-dbus-dev libssl-dev libffi-dev libdbus-1-dev libdbus-glib-1-dev
  sudo apt-get install chromium-chromedriver python2.7


#Mac
elif [[ "$UNAME" == "Darwin" ]]; then
  brew install ffmpeg
  brew install openssl
  virtualenv env
  . env/bin/activate
  pip install -r requirements.txt
  exit 0
else
  echo "Operating system not supported"
  exit 1
fi

# Check if sudo is required
pip install virtualenv
if [[ "$?" -eq 2 ]]; then
  sudo pip install virtualenv
fi

virtualenv env --python=python2.7
source env/bin/activate
pip install -r requirements.txt
pip install dbus-python
