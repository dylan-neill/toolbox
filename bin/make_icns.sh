#!/usr/bin/env bash
#
# Regenerate the macOS app icon (app_icon.icns) from the 512px master PNG.
#
# Briefcase consumes src/toolbox/resources/icons/app_icon.icns when packaging the
# macOS .app; this script is how that .icns is produced, so the icon is a
# reproducible derivative of app_icon512.png rather than a hand-made binary.
#
# Requires macOS (uses the built-in `sips` and `iconutil`).
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
src="$here/src/toolbox/resources/icons/app_icon512.png"
out="$here/src/toolbox/resources/icons/app_icon.icns"

iconset="$(mktemp -d)/app.iconset"
mkdir -p "$iconset"
for size in 16 32 128 256 512; do
    sips -z "$size" "$size" "$src" --out "$iconset/icon_${size}x${size}.png" >/dev/null
    retina=$((size * 2))
    sips -z "$retina" "$retina" "$src" --out "$iconset/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$iconset" -o "$out"
echo "Wrote $out"
