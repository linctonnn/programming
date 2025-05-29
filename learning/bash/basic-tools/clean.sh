#!/usr/bin/env bash
set -euo pipefail

LOGFILE="$HOME/clean_env_$(date +%Y%m%d_%H%M%S).log"
DRY_RUN=false
CONFIRM_GLOBAL=true

# Direktori cache yang sering dipakai
THUMBNAIL_CACHE_DIR="$HOME/.cache/thumbnails"
FIREFOX_CACHE_DIR="$HOME/.cache/mozilla/firefox"
CHROME_CACHE_DIR="$HOME/.cache/google-chrome"
CHROMIUM_CACHE_DIR="$HOME/.cache/chromium"
TRASH_DIR="$HOME/.local/share/Trash/files"

usage() {
  cat <<EOF
Usage: $0 [OPTIONS] [TASKS...]

Options:
  --dry-run        Show commands without executing them
  --no-confirm     Skip global confirmation prompt
  -h, --help       Show this help message

Tasks (default: all):
  apt              Clean apt cache and autoremove
  history          Clear shell histories
  kernels          Remove old kernel packages (keep current + 2 previous)
  journal          Vacuum journal logs to 10MB
  logrotate        Force logrotate run
  snap             Remove disabled snap revisions
  thumbnails       Clear thumbnail cache
  firefox          Clear Firefox disk cache (all profiles)
  trash            Empty user trash can
  logs             Truncate large log files in /var/log older than 7 days
  docker           Cleanup Docker (dangling images, stopped containers)
  npm              Clean npm cache
  pip              Clean pip3 cache
  swap             Reset swap
  all              Run all tasks (default)

Examples:
  $0 --dry-run all
  $0 apt history kernels

EOF
  exit 0
}

log_message() {
    local msg="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $msg" | tee -a "$LOGFILE"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

run_cmd() {
  if $DRY_RUN; then
    echo "[DRY-RUN] $*"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [DRY-RUN] $*" >> "$LOGFILE"
  else
    "$@"
  fi
}

check_dependencies() {
  local required=(sudo apt-get dpkg-query journalctl logrotate snap)
  local optional=(docker npm pip3)

  for cmd in "${required[@]}"; do
    if ! command_exists "$cmd"; then
      log_message "Error: Required command '$cmd' not found. Please install it first."
      exit 1
    fi
  done

  for cmd in "${optional[@]}"; do
    if ! command_exists "$cmd"; then
      log_message "Warning: Optional command '$cmd' not found. Some cleanup tasks will be skipped."
    fi
  done
}

confirm_global() {
  if $DRY_RUN || ! $CONFIRM_GLOBAL; then
    return 0
  fi
  echo -n "This script will perform system cleanup tasks which may remove files and packages. Continue? (y/N): "
  read -r answer
  if [[ "${answer,,}" != "y" ]]; then
    log_message "Aborted by user."
    exit 1
  fi
}

clean_apt() {
  log_message "Cleaning apt cache..."
  run_cmd sudo apt-get clean

  log_message "Cleaning obsolete package files (autoclean)..."
  run_cmd sudo apt-get autoclean -y

  log_message "Removing unused dependencies (autoremove)..."
  run_cmd sudo apt-get autoremove -y
}

clean_history() {
  log_message "Clearing shell histories..."

  local files=("$HOME/.bash_history" "$HOME/.zsh_history" "$HOME/.local/share/fish/fish_history")
  for f in "${files[@]}"; do
    if [ -f "$f" ]; then
      run_cmd bash -c "> \"$f\""
      log_message "Cleared $f"
    fi
  done

  history -c || true
  history -r || true
}

remove_old_kernels() {
  log_message "Checking kernel versions to be removed..."

  local current_kernel
  current_kernel=$(uname -r)
  local current_kernel_base
  current_kernel_base=$(echo "$current_kernel" | sed -E 's/([^-]+-[0-9]+).*/\1/')

  # Ambil semua kernel image, header, modules-extra
  local all_kernels
  all_kernels=$(dpkg-query -W -f='${Package}\n' 'linux-image-[0-9]*' 2>/dev/null || true)
  all_kernels+=$'\n'$(dpkg-query -W -f='${Package}\n' 'linux-headers-[0-9]*' 2>/dev/null || true)
  all_kernels+=$'\n'$(dpkg-query -W -f='${Package}\n' 'linux-modules-extra-[0-9]*' 2>/dev/null || true)
  all_kernels=$(echo "$all_kernels" | grep -v '^$' | sort -u)

  # Dapatkan list kernel base versi yang terinstall (tanpa subversi)
  local kernel_bases=()
  while read -r pkg; do
    # Extract version base (ex: 5.15.0-78)
    if [[ $pkg =~ linux-(image|headers|modules-extra)-([0-9]+\.[0-9]+\.[0-9]+-[0-9]+) ]]; then
      kernel_bases+=("${BASH_REMATCH[2]}")
    fi
  done <<< "$all_kernels"

  # Ambil 2 kernel base terbaru selain yang sekarang
  IFS=$'\n' sorted_unique=($(printf "%s\n" "${kernel_bases[@]}" | sort -V | uniq))
  unset IFS

  local keep_versions=("$current_kernel_base")
  # Cari indeks current kernel base di sorted_unique
  local idx
  for i in "${!sorted_unique[@]}"; do
    if [[ "${sorted_unique[i]}" == "$current_kernel_base" ]]; then
      idx=$i
      break
    fi
  done

  # Keep 2 versi sebelumnya (jika ada)
  for offset in 1 2; do
    local prev_idx=$((idx - offset))
    if (( prev_idx >= 0 )); then
      keep_versions+=("${sorted_unique[prev_idx]}")
    fi
  done

  # Kernel yang akan dihapus: semua kecuali keep_versions
  local kernels_to_remove=()
  while read -r pkg; do
    for v in "${keep_versions[@]}"; do
      if [[ "$pkg" =~ $v ]]; then
        continue 2
      fi
    done
    kernels_to_remove+=("$pkg")
  done <<< "$all_kernels"

  if (( ${#kernels_to_remove[@]} > 0 )); then
    log_message "Kernels to be removed (keeping current + 2 previous):"
    for k in "${kernels_to_remove[@]}"; do
      echo "  $k"
    done

    # Backup list
    local backup_file="$HOME/kernel_packages_to_remove_$(date +%Y%m%d_%H%M%S).txt"
    printf "%s\n" "${kernels_to_remove[@]}" > "$backup_file"
    log_message "Backup kernel package list saved to $backup_file"

    read -r -p "Remove these kernel packages? (y/N): " confirm
    if [[ "${confirm,,}" == "y" ]]; then
      log_message "Removing old kernels..."
      run_cmd sudo apt-get remove --purge -y "${kernels_to_remove[@]}"
    else
      log_message "Kernel removal aborted."
    fi
  else
    log_message "No old kernels found to remove."
  fi
}

clean_journal_logs() {
  log_message "Vacuuming journal logs to 10MB..."
  run_cmd sudo journalctl --vacuum-size=10M
}

force_logrotate() {
  log_message "Forcing log rotation..."
  run_cmd sudo logrotate --force /etc/logrotate.conf
}

remove_snap_disabled_revisions() {
  if ! command_exists snap; then
    log_message "Snap not found; skipping snap revisions cleanup."
    return
  fi
  log_message "Removing disabled local snap package revisions..."
  snap list --all | awk '/disabled/{print $1, $3}' | while IFS= read -r line; do
      snapname=$(echo "$line" | awk '{print $1}')
      revision=$(echo "$line" | awk '{print $2}')
      if [ -n "$snapname" ] && [ -n "$revision" ]; then
          log_message "Removing $snapname revision $revision"
          run_cmd sudo snap remove "$snapname" --revision="$revision"
      fi
  done
}

clear_thumbnails_cache() {
  if [ -d "$THUMBNAIL_CACHE_DIR" ]; then
    log_message "Clearing thumbnails cache..."
    run_cmd find "$THUMBNAIL_CACHE_DIR" -mindepth 1 -delete
    log_message "Thumbnails cache cleared."
  else
    log_message "Thumbnails cache directory not found."
  fi
}

clean_firefox_cache() {
  if [ ! -d "$FIREFOX_CACHE_DIR" ]; then
    log_message "Firefox cache directory not found."
    return
  fi

  log_message "Cleaning Firefox disk cache for all profiles..."

  # Cari semua direktori cache2 dalam profil
  mapfile -t cache_dirs < <(find "$FIREFOX_CACHE_DIR" -type d -name cache2)

  if (( ${#cache_dirs[@]} == 0 )); then
    log_message "No Firefox cache2 directories found."
    return
  fi

  for dir in "${cache_dirs[@]}"; do
    log_message "Removing Firefox cache2 directory: $dir"
    run_cmd rm -rf "$dir"
  done
  log_message "Firefox disk cache cleared."
}

clean_user_trash() {
  if [ -d "$TRASH_DIR" ]; then
    log_message "Emptying user's trash can..."
    run_cmd rm -rf "$TRASH_DIR"/*
    # Info files
    if [ -d "$HOME/.local/share/Trash/info" ]; then
      run_cmd rm -rf "$HOME/.local/share/Trash/info"/*
    fi
    log_message "User's trash can emptied."
  else
    log_message "User's trash can not found or already empty."
  fi
}

clean_logs_var() {
  log_message "Truncating large and old log files in /var/log (>10MB and older than 7 days)..."
  local files
  mapfile -t files < <(sudo find /var/log -type f -name "*.log" -size +10M -mtime +7 2>/dev/null || true)
  if (( ${#files[@]} == 0 )); then
    log_message "No large old log files found to truncate."
    return
  fi
  for f in "${files[@]}"; do
    log_message "Truncating $f"
    run_cmd sudo truncate -s 0 "$f"
  done
  log_message "Log truncation done."
}

clean_docker() {
  if ! command_exists docker; then
    log_message "Docker not found; skipping Docker cleanup."
    return
  fi
  log_message "Cleaning up dangling Docker images and stopped containers..."
  run_cmd docker system prune -af
}

clean_npm_cache() {
  if ! command_exists npm; then
    log_message "npm not found; skipping npm cache cleanup."
    return
  fi
  log_message "Cleaning npm cache..."
  run_cmd npm cache clean --force
}

clean_pip_cache() {
  if ! command_exists pip3; then
    log_message "pip3 not found; skipping pip cache cleanup."
    return
  fi
  log_message "Cleaning pip cache..."
  run_cmd pip3 cache purge
}

reset_swap() {
  log_message "Resetting swap..."
  run_cmd sudo swapoff -a && sudo swapon -a
  log_message "Swap reset completed."
}

clean_chrome_cache() {
  local chrome_dirs=()
  [ -d "$CHROME_CACHE_DIR" ] && chrome_dirs+=("$CHROME_CACHE_DIR")
  [ -d "$CHROMIUM_CACHE_DIR" ] && chrome_dirs+=("$CHROMIUM_CACHE_DIR")

  for dir in "${chrome_dirs[@]}"; do
    log_message "Clearing Chrome/Chromium cache: $dir"
    run_cmd find "$dir" -mindepth 1 -delete
  done
}

clean_tmp() {
  log_message "Cleaning /tmp and /var/tmp of files older than 1 day..."
  run_cmd sudo find /tmp -mindepth 1 -mtime +1 -exec rm -rf {} + || true
  run_cmd sudo find /var/tmp -mindepth 1 -mtime +1 -exec rm -rf {} + || true
  log_message "Temporary directories cleaned."
}

show_summary() {
  log_message "Cleanup completed."
  log_message "Disk usage summary (root partition):"
  df -h / | tee -a "$LOGFILE"
  log_message "You may want to reboot if kernels were removed."
}

main() {
  if [[ $# -eq 0 ]]; then
    TASKS=("all")
  else
    TASKS=("$@")
  fi

  check_dependencies
  confirm_global

  for task in "${TASKS[@]}"; do
    case "$task" in
      -h|--help)
        usage
        ;;
      all)
        clean_apt
        clean_history
        remove_old_kernels
        clean_journal_logs
        force_logrotate
        remove_snap_disabled_revisions
        clear_thumbnails_cache
        clean_firefox_cache
        clean_user_trash
        clean_logs_var
        clean_docker
        clean_npm_cache
        clean_pip_cache
        reset_swap
        clean_chrome_cache
        clean_tmp
        ;;
      apt) clean_apt ;;
      history) clean_history ;;
      kernels) remove_old_kernels ;;
      journal) clean_journal_logs ;;
      logrotate) force_logrotate ;;
      snap) remove_snap_disabled_revisions ;;
      thumbnails) clear_thumbnails_cache ;;
      firefox) clean_firefox_cache ;;
      trash) clean_user_trash ;;
      logs) clean_logs_var ;;
      docker) clean_docker ;;
      npm) clean_npm_cache ;;
      pip) clean_pip_cache ;;
      swap) reset_swap ;;
      chrome) clean_chrome_cache ;;
      tmp) clean_tmp ;;
      *)
        log_message "Unknown task: $task"
        usage
        ;;
    esac
  done

  show_summary
}

# Parse flags before positional args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --no-confirm)
      CONFIRM_GLOBAL=false
      shift
      ;;
    -h|--help)
      usage
      ;;
    *)
      break
      ;;
  esac
done

main "$@"

