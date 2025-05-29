#!/bin/bash
set -euo pipefail # Lebih aman

# Fungsi untuk logging dengan timestamp (opsional)
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

clean_env() {
    log_message "Starting comprehensive Linux environment cleanup..."

    log_message "Cleaning apt cache..."
    sudo apt-get clean -y

    log_message "Clearing current user's bash history file and current session history..."
    if [ -f ~/.bash_history ]; then
        > ~/.bash_history # Kosongkan file riwayat (lebih singkat)
        log_message "Bash history file emptied."
    fi
    history -c # Bersihkan riwayat sesi saat ini
    history -r # Baca ulang dari file (yang sekarang kosong atau tidak ada)
    log_message "Current session history cleared."

    log_message "Removing unused dependencies..."
    sudo apt-get autoremove -y

    log_message "Checking kernel versions to be removed..."
    CURRENT_KERNEL=$(uname -r)
    # Ambil versi dasar tanpa sub-versi ABI, misal 5.15.0-78 dari 5.15.0-78-generic
    # Regex ini sudah cukup baik, tapi bisa disesuaikan jika ada pola kernel yang sangat berbeda
    CURRENT_KERNEL_BASE=$(uname -r | sed -E 's/-[0-9]+([.-].*|(-generic|-lowlatency|-aws|-azure|-gcp|-oem|-signed))?$//')

    # Menggunakan dpkg-query untuk daftar paket yang lebih bersih
    # Menambahkan linux-modules-extra
    INSTALLED_KERNELS_IMAGES=$(dpkg-query -W -f='${Package}\n' 'linux-image-[0-9]*' 2>/dev/null || true)
    INSTALLED_KERNELS_HEADERS=$(dpkg-query -W -f='${Package}\n' 'linux-headers-[0-9]*' 2>/dev/null || true)
    INSTALLED_KERNELS_MODULES_EXTRA=$(dpkg-query -W -f='${Package}\n' 'linux-modules-extra-[0-9]*' 2>/dev/null || true)

    ALL_KERNEL_PACKAGES=$(echo -e "${INSTALLED_KERNELS_IMAGES}\n${INSTALLED_KERNELS_HEADERS}\n${INSTALLED_KERNELS_MODULES_EXTRA}" | grep -v '^$' | sort -u)

    KERNELS_TO_REMOVE=""
    if [ -n "$ALL_KERNEL_PACKAGES" ]; then
        KERNELS_TO_REMOVE=$(echo "$ALL_KERNEL_PACKAGES" | \
                            grep -vE "linux-(image|headers|modules-extra)-${CURRENT_KERNEL_BASE}(\.|$)" | \
                            grep -vE "linux-(image|headers|modules-extra)-${CURRENT_KERNEL}(\.|$)" | \
                            tr '\n' ' ' | sed 's/ $//') # Hapus spasi di akhir jika ada
    fi
    
    if [ -n "$KERNELS_TO_REMOVE" ]; then
        log_message "The following kernel packages might be removable (please double check):"
        echo "$KERNELS_TO_REMOVE" | tr ' ' '\n'
        
        read -r -p "Are you sure you want to remove these kernel packages? (y/N): " CONFIRM
        if [[ "${CONFIRM,,}" == "y" ]]; then # Konversi ke huruf kecil untuk perbandingan
            log_message "Removing old kernels: $KERNELS_TO_REMOVE"
            # shellcheck disable=SC2086 # $KERNELS_TO_REMOVE sengaja di-word-split
            sudo apt-get remove --purge $KERNELS_TO_REMOVE
        else
            log_message "Aborting kernel removal."
        fi
    else
        log_message "No old kernels found to remove with this method."
    fi

    log_message "Vacuuming journal logs to 10MB..."
    sudo journalctl --vacuum-size=10M

    log_message "Forcing log rotation..."
    sudo logrotate --force /etc/logrotate.conf
    
    log_message "Removing disabled local snap package revisions..."
    # Menggunakan loop yang lebih aman jika nama snap mengandung spasi (jarang terjadi)
    snap list --all | awk '/disabled/{print $1, $3}' | while IFS= read -r line; do
        snapname=$(echo "$line" | awk '{print $1}')
        revision=$(echo "$line" | awk '{print $2}')
        if [ -n "$snapname" ] && [ -n "$revision" ]; then # Pastikan keduanya tidak kosong
            log_message "Removing $snapname revision $revision"
            sudo snap remove "$snapname" --revision="$revision"
        fi
    done
    
    log_message "Clearing thumbnails cache for current user..."
    if [ -d ~/.cache/thumbnails ]; then
        find ~/.cache/thumbnails -mindepth 1 -delete
        log_message "Thumbnails cache cleared."
    else
        log_message "Thumbnails cache directory not found for current user."
    fi
    
    log_message "Cleaning Firefox cache (disk cache only) for current user..."
    # Ini akan membersihkan untuk semua profil yang ditemukan di bawah .cache/mozilla/firefox
    # Catatan: Jika Firefox dari Snap/Flatpak, path akan berbeda.
    if [ -d ~/.cache/mozilla/firefox ]; then
        find ~/.cache/mozilla/firefox/ -type d -name "cache2" -exec rm -rf {} + 2>/dev/null
        # find ~/.cache/mozilla/firefox/ -type f -name "startupCache.json" -delete 2>/dev/null # Opsional
        log_message "Firefox disk cache cleared for current user."
    else
        log_message "Firefox cache directory not found for current user."
    fi

    # Opsi tambahan:
    # log_message "Cleaning Flatpak unused runtimes..."
    # if command -v flatpak &> /dev/null; then
    #     flatpak uninstall --unused -y
    # else
    #     log_message "Flatpak not found."
    # fi

    # log_message "Cleaning user's trash can..."
    # if [ -d ~/.local/share/Trash/files ]; then
    #    rm -rf ~/.local/share/Trash/files/*
    #    rm -rf ~/.local/share/Trash/info/*
    #    log_message "User's trash can emptied."
    # else
    #    log_message "User's trash can not found or already empty."
    # fi
    
    log_message "All cleanup tasks done."
}

# Skrip ini dirancang untuk dijalankan oleh pengguna biasa.
# Perintah yang memerlukan hak akses root akan menggunakan sudo.
# Jika Anda ingin menjalankan seluruh skrip sebagai root, uncomment blok di bawah dan hapus 'sudo' dari perintah-perintah di atas.
# if [[ "$EUID" -ne 0 ]]; then
#   echo "This script uses sudo for many commands. You will be prompted for your password."
#   echo "Alternatively, consider running it with: sudo $0 (dan modifikasi skrip untuk tidak menggunakan sudo secara internal)"
# fi

clean_env
