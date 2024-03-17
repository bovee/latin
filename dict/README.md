# Starter Latin Dictionary

This is an attempt to OCR and cleanup public domain, Latin-Latin dictionaries/vocabularies for beginners.
Vowel quantities were updated to modern standards and editing was performed to allow entries to be parsed programmatically (e.g. `-īvī (-iī)` was rewritten to `-īvī | -iī`, extraneous information was removed from the entry heads, etc).
Pictures are not included yet.

Each file has a slightly different format and the script `process_dicts.py` was written to process and harmonize entries across files for comparison; it is still a work in progress.

## Sources 

See files in the `books` folder for more details about each source.

 - `dict_app_fab.txt`: Appleton - Fābulae
 - `dict_app_pons.txt`: Appleton & Jones - Pōns Tīrōnum
 - `dict_dale.txt`: Dale - Rēgēs Cōnsulēsque Rōmānī
 - `dict_paine_sec.txt`: Mainwaring & Paine - Secundus Annus
 - `dict_strange_ovid.txt`: Strangeways - P. Ovidī Nāsōnis Elegīaca
