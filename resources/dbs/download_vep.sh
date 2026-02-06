#!/usr/bin/env bash
set -euo pipefail

# CONFIG
VEP_VERSION=110
ASSEMBLY=GRCh38
CACHE_DIR=$(pwd)/vep_cache
PLUGIN_DIR=$(pwd)/vep_plugins

mkdir -p "$CACHE_DIR" "$PLUGIN_DIR"

echo "Downloading VEP cache..."
vep_install \
  -a cf \
  -s homo_sapiens \
  -y "$ASSEMBLY" \
  -c "$CACHE_DIR" \
  --version "$VEP_VERSION" \
  --CONVERT

echo "Downloading VEP plugins..."

cd "$PLUGIN_DIR"

# Common clinical plugins
git clone https://github.com/Ensembl/VEP_plugins.git

echo "VEP cache and plugins installed successfully."
