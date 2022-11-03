#!/usr/bin/env bash
# Downloads the intended PDFs and metadata into volumes/*.
# To be called from the top-level directory (with activated venv if needed).
# Each call must include all existing corpus directories so that retrievlit can
# avoid name collisions.

retrievelit() {
  # highly provisional calling style:
  python /c/ws/rq/retrievelit/main.py --ieeecs $*
}

cd volumes

retrievelit --mapper ComputerOrgJournal --ieeecs TSE-2021
retrievelit --mapper Springer EMSE-2021 TSE-2021

cd ..
