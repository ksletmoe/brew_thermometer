#!/usr/bin/env bash

PI_USER="pi"
CONF_DIR="/etc/brew_thermometer"
DEFAULT_CONF_FILE="default_configuration.json"
CONF_FILE_NAME="config.json"

mkdir -p "$CONF_DIR"
chown -R "$PI_USER":"$PI_USER" "$CONF_DIR"
chmod -R 700 "$CONF_DIR"
cp "$DEFAULT_CONF_FILE" "$CONF_DIR/$CONF_FILE_NAME"


