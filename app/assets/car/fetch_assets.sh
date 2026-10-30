#!/bin/sh
# Download the licensed demo photo set (see CREDITS.md) next to this script
# for fully local runs. Without it, the app streams the same frames from
# their canonical Wikimedia Commons URLs (frames.json).
set -e
cd "$(dirname "$0")"
UA="ShowfrontBuild/1.0 (contact: abuz8studios@gmail.com)"
curl -s -A "$UA" -o 01.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/2018_Toyota_Camry_Hybrid_WAS_2017_1726.jpg/1280px-2018_Toyota_Camry_Hybrid_WAS_2017_1726.jpg"
curl -s -A "$UA" -o 02.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/2018_Toyota_Camry_Hybrid_WAS_2017_1728.jpg/1280px-2018_Toyota_Camry_Hybrid_WAS_2017_1728.jpg"
curl -s -A "$UA" -o 03.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/2018_Toyota_Camry_Hybrid_WAS_2017_1727.jpg/1280px-2018_Toyota_Camry_Hybrid_WAS_2017_1727.jpg"
curl -s -A "$UA" -o 04.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/2018_Toyota_Camry_Hybrid_WAS_2017_1729.jpg/1280px-2018_Toyota_Camry_Hybrid_WAS_2017_1729.jpg"
curl -s -A "$UA" -o 05.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/2018_Toyota_Camry_Hybrid_WAS_2017_1730.jpg/1280px-2018_Toyota_Camry_Hybrid_WAS_2017_1730.jpg"
echo "Fetched 5 frames (CC BY-SA 4.0, Mariordo via Wikimedia Commons)."
