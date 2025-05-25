#!/bin/bash

clean_env() {
    echo "Cleaning apt cache..."
    sudo apt-get clean

    echo "Cleaning history bash"
    sudo history -c -y

    echo "Removing unused dependencies..."
    sudo apt-get autoremove

    echo "Checking kernel versions to be removed..."
    KERNELS_TO_REMOVE=$(dpkg -l 'linux-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d')

    echo "The following kernels will be removed:"
    echo "$KERNELS_TO_REMOVE"
    
    read -p "Are you sure you want to remove these kernels? (y/N): " CONFIRM
    if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
        echo "Aborting kernel removal."
        return
    fi

    echo "Removing old kernels..."
    sudo apt-get remove --purge $KERNELS_TO_REMOVE

    echo "Vacuuming journal logs to 10MB..."
    sudo journalctl --vacuum-size=10M

    echo "Deleting old log files"
    sudo find /var/log -type f -iname '*.log' -exec rm -f {} \;
    
    echo "Deleting system log"
    sudo logrotate --force /etc/logrotate.conf
    
    echo "Deleting unused local snap package"
    sudo snap list --all | awk '/disabled/{print $1, $3}' | while read snapname revision; do sudo snap remove "$snapname" --revision="$revision"; done
    
    echo "Clear thumbnails cache"
    rm -rf ~/.cache/thumbnails/*
    
    echo "Deleting cache mozilla firefox"
    rm -rf ~/.cache/mozilla
    
    echo "All done"
}

clean_env

