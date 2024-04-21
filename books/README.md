# Books in Latin

## Background

The goal of this project is to find macronized Latin works that are in the public domain and adapt them into text formats suitable for e-readers or for any other purposes.

Ideally the texts would contain only Latin, but several still contain headers or passages in English (that ideally could be translated at some point). Any English should be marked in *italics* (surrounded by `*`) or as headers (lines starting with `#`).

Books were OCRed from original scan PDFs, errors were corrected, formatting was updated in markdown, and vowel lengths were adjusted to modern standards. When possible, footnotes and images were retained. Most prefaces, appendices, vocabularies, or other sections of the works primarily in English are omitted.

## Creating ebooks

Pandoc can be used to turn any of the markdown files present into an ebook suitable for reading on an e.g. Kindle or other device.

```bash
pandoc -o fabulae.epub appleton_fabulae.md
```

## List of Edited Books

 - [Appleton - Fabulae](appleton_fabulae.md)
 - [Appleton & Jones - Pons Tironum](appleton_pons_tironum.md)
 - [Bennett - Cicero's Selected Orations](bennett_cicero.md)
 - [Chickering - First Latin Reader](chickering_first_latin_reader.md)
 - [Clark - Eutropi Historia Romana](clark_eutropi.md)
 - [Collar - Gate to Caesar](collar_gate_to_caesar.md)
 - [Collar - Via Latina](collar_via_latina.md)
 - [Dale - Rēgēs Cōnsulēsque Rōmānī](dale_reges.md)
 - [Dix - A Third Latin Reader and Writer](dix_third_reader.md)
 - [Dobson - Caesar in Britain](dobson_caesar_britain.md)
 - [Drake - Selected Fables of Phaedrus](drake_phaedrus.md)[^1]
 - [Duff - Silva Latina](duff_silva_latina.md)
 - [Eutropius - Breviarium](eutropius_breviarium.md)[^2]
 - [Fairclough & Brown - Virgil's Aeneid](fairclough_brown_aeneid.md)
 - [Fay - Carolus et Maria](fay_carolus.md)
 - [Knapp - The Aeneid of Virgil and Metamorphoses of Ovid](knapp_aeneid.md)[^1]
 - [Maxey & Fay - A New Latin Primer](maxey_primer.md)
 - [Moore - Porta Latina](moore_porta.md)
 - [Newman - Easy Latin Plays](newman_plays.md)
 - [Nutting - A First Latin Reader](nutting_reader.md)
 - [Ritchie - Fabulae Faciles](ritchie_fabulae_faciles.md)
 - [Sonnenschein - Ora Maritima](sonnenschein_ora_maritima.md)

[^1]: Macrons weren't modified/updated for books consisting only of prose.
[^2]: Books are obtained from secondary sources such as Wikisource or Dickinson College Commentaries

## List of Unedited Books or In-Progress Books

 - [Appleton - Lūdī Persicī](appleton_ludi.md)
 - [Appleton & Jones - Puer Romanus](appleton_jones_puer_romanus.md)
 - [D'Ooge - Easy Latin](dooge_easy_latin.md)
 - [D'Ooge - Selections from Urbis Romae Viri Inlustres](dooge_urbis_romae.md)
 - [Fairclough & Richardson - Phormio of Terence](fairclough_richardson_phormio.md)
 - [Flagg - The Lives of Cornelius Nepos](flagg_nepos.md)
 - [Forbes - Eight Orations of Cicero](forbes_cicero.md)
 - [Gallup - A Latin Reader](gallup_reader.md)
 - [Gildersleeve - A Latin Reader](gildersleeve_reader.md)
 - [Greenough & Daniell - Conspiracy of Catilline](greenough_sallust.md)
 - [Greenough & D'Ooge & Daniell - Caesar's Gallic War](greenough_caesar.md)
 - [Greenough & Kittredge - Select Orations and Letters of Cicero](greenough_cicero.md)
 - [Gunnison & Harley - Marcus Tullius Cicero Seven Orations](gunnison_cicero.md)
 - [Harkness & Kirtland - Six Orations of Cicero](harkness_cicero.md)
 - [Harper & Gallup - Ten Orations of Cicero](harper_cicero.md)
 - [Hazzard - Eutropius](hazzard_eutropius.md)
 - [Herbermann - The Bellum Catilinae of C. Sallustius Crispus](herbermann_sallust.md)
 - [Humphreys - Selections from the History of Alexander the Great by Quintus Curtius Rufus](humphreys_alexander.md)
 - [Jones & Smith - Excerpta Brevia](jones_excerpta.md)
 - [Kelsey - Select Orations and Letters of Cicero](kelsey_cicero.md)
 - [Kirtland - Selections from the Correspondence of Cicero](kirtland_cicero.md)
 - [Lord - Cicero de Amicitia](lord_amicitia.md)
 - [Lord - Livy Book I](lord_livy.md)
 - [Maxey - Cornelia](maxey_cornelia.md)
 - [Miller & Beeson - Second Latin Book](miller_reader.md)
 - [Nutting - Ad Alpes](nutting_ad_alpes.md)
 - [Paine & Mainwaring - Primus Annus](paine_primus.md)
 - [Paine & Mainwaring - Secundus Annus](paine_secundus.md)
 - [Roberts & Rolfe - Cicero Selected Orations and Letters](rolfe_cicero.md)
 - [Roberts & Rolfe - Ovid's Metamorphoses](rolfe_ovid.md)
 - [Roberts & Rolfe - Vergil's Aeneid Books I-VI](rolfe_vergil.md)
 - [Rolfe - The Lives of Cornelius Nepos](rolfe_nepos.md)
 - [Rolfe - Livy Book 1](rolfe_livy.md)
 - [Rolfe - Selections from Viri Romae](rolfe_viri_romae.md)
 - [Rolfe & Roberts - Caesar's Gallic War](rolfe_caesar.md)
 - [Sanford & Scott - A Junior Latin Reader](sanford_reader.md)
 - [Schlicher - Latin Plays](schlicher_plays.md)
 - [Scudder - Easy Latin](scudder_easy.md)
 - [Scudder - Sallust's Catiline](scudder_sallust.md)
 - [Strangeways - P. Ovidī Nāsōnis Elegīaca](strangeways_ovid.md)
 - [Stuart & Lee - Caesar's Gallic War](stuart_caesar.md)
 - [Towle & Jenks - Caesar's Gallic War](towle_caesar.md)
 - [Tunstall - Six Orations of Cicero](tunstall_cicero.md)
 - [von Minckwitz - Cicero Ten Orations](von_minckwitz_cicero.md)
 - [White - Cicero's Oration for Quintus Ligarius](white_cicero.md)

## Other resources

[WikiSource](https://la.wikisource.org/wiki/Categoria:Textus_ad_discendam_linguam_latinam) has a collection of Latin e-books in several formats.
