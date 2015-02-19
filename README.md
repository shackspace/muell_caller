# Call Gelber Sack

Scope of this project is to glue two projects in the shackspace:

 - Tell via Gobbelz (Lounge TTS Interface) that today is Gelber Sack (Info by openHAB installation)

# Installation

use the systemd files provided to install a timer, then run

    systemctl enable gelber_sack.timer
    systemctl start gelber_sack.timer
    # test via:
    ## systemctl start gelber_sack.service
