# Generate reachy_mobile_base.service
# Put this service file in ~/.config/systemd/user

mkdir -p $HOME/.config/systemd/user

tee $HOME/.config/systemd/user/reachy_mobile_base.service <<EOF
[Unit]
Description=Mobile base SDK server service

[Service]
SyslogIdentifier=reachy_mobile_base
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/bash $PWD/launch_mobile_base.bash


[Install]
WantedBy=default.target
EOF
