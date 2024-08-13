
function get_battery_level() {
  local output
  output=$(dbus-send --session --dest=tn.aziz.soundpeats.BLEService --print-reply /tn/aziz/soundpeats/BLEService tn.aziz.soundpeats.BLEService.GetBatteryLevel 2>&1)

  if [[ $output == *"Not connected"* ]]; then
    echo "disconnected"
    return
  fi

  local left
  local right
  left=$(echo "$output" | awk '/string "left"/ {getline; print $3}')
  right=$(echo "$output" | awk '/string "right"/ {getline; print $3}')

  echo "L: $left, R: $right"
}


function get_cached_battery_level() {
  local cache_file="/tmp/headset_battery_level"
  local cache_duration=60  # Cache duration in seconds (1 minute)
  local current_time
  current_time=$(date +%s)

  if [[ -f $cache_file ]]; then
    local cache_time
    cache_time=$(stat -c %Y "$cache_file")
    local time_diff=$((current_time - cache_time))

    if (( time_diff < cache_duration )); then
      cat "$cache_file"
      return
    fi
  fi

  local battery_level
  battery_level=$(get_battery_level)
  echo "$battery_level" > "$cache_file"
  echo "$battery_level"
}

alias bat=get_battery_level

# p10k.zsh

function prompt_soundpeats() {
    local battery_level
    battery_level=$(get_cached_battery_level)
    p10k segment -f 208 -i '🎧' -t "${battery_level}"
}
