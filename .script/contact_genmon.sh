#!/bin/bash

# Path to your translated Python script
PYTHON_SCRIPT="$HOME/.script/contacts.py"

# Modern SEARCH icon for that cockpit look
ICON="/usr/share/icons/Papirus/24x24/apps/system-search.svg"

# Blue-colored label for your XFCE panel
LABEL="<txt><span color='#00d7ff' weight='bold'> Contacts</span></txt>"

# Optimized command for English localization
CLICK_CMD="bash -c '
    TERM=\$(zenity --entry --title=\"CONTACT SEARCH\" --text=\"Who or what number are you looking for?\");
    if [ \$? -eq 0 ]; then
        RESULT=\$(python3 $PYTHON_SCRIPT \"\$TERM\" | zenity --list \
            --title=\"SEARCH RESULTS\" \
            --column=\"CONTACT | PHONE\" \
            --width=500 --height=600 \
            --text=\"Results for: \$TERM\");
        if [ ! -z \"\$RESULT\" ]; then
            NUMBER=\$(echo \"\$RESULT\" | awk -F\"|\" \"{print \$2}\" | xargs);
            echo -n \"\$NUMBER\" | xclip -selection clipboard;
            notify-send \"Cockpit\" \"Number \$NUMBER copied to clipboard!\" --icon=edit-copy;
        fi
    fi
'"

# Output for Genmon Plugin
echo "<img>${ICON}</img>"
echo "${LABEL}"
echo "<click>${CLICK_CMD}</click>"
echo "<tool>Google Contacts Search (Evolution)</tool>"
