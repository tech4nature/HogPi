System events are logged to `hedge.log` via a logging configuration in
`hedge.py`.

To collate these events (plus system metrics such as memory usage)
across all boxes, we use the Stackdriver component of Google Cloud
Services.

This requires installation and configuration of the `fluent-bit`
collector on each box.

## Installation

    # Trust the fluentbit package signing key
    wget -qO - http://packages.fluentbit.io/fluentbit.key | sudo apt-key add -

    # Add their repo as a package source
    echo "deb https://packages.fluentbit.io/raspbian/stretch stretch main" | sudo tee -a  /etc/apt/sources.list > /dev/null

    # Install the collector
    sudo apt-get update
    sudo apt-get install td-agent-bit

    # Replace default config with our own
    sudo cp deploy/logging/td-agent-bit.conf /etc/td-agent-bit/td-agent-bit.conf

You should change every instance of the line `Tag mem.box1` within `/etc/td-agent-bit/td-agent-bit.conf`, to match the box that you're installing on, so we know the origin of each log entry. For example, you might change `Tag mem.box1` to `Tag mem.box-7943438380890` throughout.

Then get a copy of the Google Cloud credentials file `hedgehogrepublic-249416-03aed70fa4e3.json` and place it in `/etc/td-agent-bit/`, and restart the service:

    sudo service td-agent-bit restart

Check it is running ok:

    sudo service td-agent-bit status

Logs should now be visible at https://console.cloud.google.com/logs/viewer?project=hedgehogrepublic-249416 (for users with permissions to do so)
