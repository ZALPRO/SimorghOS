#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  SimorghOS 0.0.1 — ISO build script / اسکریپت ساخت ISO
#  SimorghOS — the self-governing operating system
#
#  Usage:  sudo ./build.sh          (full ISO build)
#          sudo ./build.sh clean    (cleanup)
#  Requires: live-build xorriso squashfs-tools dosfstools (and sudo)
# ─────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "clean" ]]; then
    ./auto/clean
    exit 0
fi

if [[ $EUID -ne 0 ]]; then
    echo "simorgh: ISO build needs root →  sudo ./build.sh" >&2
    exit 1
fi

umask 022
export LC_ALL=C
# CA bundle inside the bootstrap so HTTPS archives (Brave) verify on the
# very first apt update
export DEBOOTSTRAP_OPTIONS="--include=ca-certificates"

echo "── simorgh: lb config ──"
./auto/config

echo "── lb build ──"
lb build 2>&1 | tee build.log

if [[ -f live-image-amd64.hybrid.iso ]]; then
    mkdir -p dist
    mv live-image-amd64.hybrid.iso "dist/simorgh-os-0.0.1-amd64.iso"
    sha256sum "dist/simorgh-os-0.0.1-amd64.iso" > "dist/simorgh-os-0.0.1-amd64.iso.sha256"
    echo
    echo "✔ ISO ready: $(readlink -f dist/simorgh-os-0.0.1-amd64.iso)"
    cat "dist/simorgh-os-0.0.1-amd64.iso.sha256"
else
    echo "✘ ISO build failed; see build.log" >&2
    exit 1
fi
