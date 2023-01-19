#!/usr/bin/env bash
# Downloads the intended PDFs and metadata into volumes/*.
# To be called from the top-level directory (with an alias or activated venv etc. such that
# the retrievelit command is available under that name).
# Each call must include all existing corpus directories so that retrievlit can
# avoid name collisions.
# It is almost certainly better to call these commands one-by-one, not as a batch.

cd volumes

retrievelit --mapper Elsevier IST-2022
retrievelit --mapper Acm --maxwait=30 TOSEM-2022 IST-2022
retrievelit --mapper Acm --maxwait=30 --grouping=volume ICSE-2022 TOSEM-2022 IST-2022
retrievelit --mapper ComputerOrgJournal TSE-2022 ICSE-2022 TOSEM-2022 IST-2022
retrievelit --mapper Springer EMSE-2022 TSE-2022 ICSE-2022 TOSEM-2022 IST-2022

cd ..
