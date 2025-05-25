#!/bin/bash

install_zsh() {
    echo "zsh terminal rc start to install..."
    sudo apt install -y zsh

    if ! command -v wget &> /dev/null; then
        echo "wget not found"
        sudo apt install -y wget
    fi

    echo "Installing OhMyZsh"
    wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh

    echo "Zsh and OhMyZsh allready installed successfully"
}

automatic_reboot_after_install() {
    read -p "The system need to restart to actually make something happen. Are you sure (Y/N): " user_input

    if [[ -z "$user_input"  ]]; then 
        echo "You must enter something (Y/N)"
    elif [[ "$user_input" =~ ^[Yy]$ ]]; then
        echo "Rebooting..."
        chsh -s `which zsh`
        sudo reboot
    elif [[ "$user_input" =~ ^[Nn]$ ]]; then
        chsh -s `which zsh` && exit
        echo "No reboot, installation complete."
    fi
}

install_zsh
automatic_reboot_after_install
