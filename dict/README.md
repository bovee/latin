# Learning Dictionaries

The `dict.txt` file here is a compilation of various public domain beginner Latin dictionaries.

## Format

Each line is a semicolon-delimited list of the following: `headwords; part-of-speech; entry`.

The first entry is a comma-delimited list of headwords. Verbs have four parts, adjectives three, nouns two, and all other forms one. The verb forms are the first person singular, the infinitive, the perfect infinitive, and the supine. If a form is missing, a `—` is used as a placeholder. The adjective forms are the male, female, and neuter for most adjectives (or) the nominative, the genitive, and a `—` for adjectives of one termination. Nouns have the nominative form and the genitive and all other entries have only one headword. Each headword is fully expanded for ease of parsing (e.g. no `-ōrum` forms are present) with a `|` used to separate the stem from the ending and if multiple forms are present (e.g. `abiī | abīvī`), they are separated by ` | `s.

The second entry is the part-of-speech; these are as follows:

 - `adi`: adjective
 - `adv`: adverb
 - `con`: conjunction
 - `gra`: grammatical points
 - `ind`: indeclinable (not further classified)
 - `int`: interjection
 - `nom`: noun
 - `ver`: verb

Lastly comes the dictionary entry. Each is tagged with a source code as follows in a `[..]` block followed by the text entry. See the `dict/sources` folder for the original OCR dictionary files.

 - `F`: Appleton - F\u0101bulae
 - `PT`: Appleton & Jones - P\u014dns T\u012br\u014dnum
 - `RCR`: Dale - R\u0113g\u0113s C\u014dnsul\u0113sque R\u014dm\u0101n\u012b
 - `SA`: Mainwaring & Paine - Secundus Annus
 - `ONE`: Strangeways - P. Ovid\u012b N\u0101s\u014dnis Eleg\u012baca

## Pictures

Pictures sourced from Fabulae are indicated with a `_f` suffix and from Pons Tironum with a `_pt` suffix. Macrons in titles are indicated with a dash (`-`) after each long vowel.

Pictures were also sourced from the following Public Domain books:
`FP` - https://archive.org/details/firstprimerbeing00meikuoft/page/8/mode/2up
`GLS` - https://archive.org/details/ERIC_ED623145/page/8/mode/2up
`IC` - https://archive.org/details/illustratedcompa00richuoft/page/n29/mode/2up

Sources for each word/illustration are as follows:
F: apis,bracchium,calamus,cithara,concha,delphinus,formi-ca,halce-do-,hedera,mi-les,musca,muste-la,pho-ca,regio-ne-s,ste-llio-,thyrsus,tuba
PT: ara-trum,balneum,convi-va,cru-s,fro-ns,fu-nis,lectica,lu-dus,ma-lum,ovis,pecten,pila,pirum,porcus,pullus,raeda,saccus,salto-,ta-li-,tesserae,u-vae,va-s
IC: agita-tor,alveus,arcus,armilla,as,a-trium,augur,auri-ga,bacchae,baculum,balteus,bra-cae,bu-cina-tor,calathus,calceus,calix,carcer,cardo-,carpentum,casa,castellum,cate-na,cavea,centurio-,cinctus_gabi-nus,circus,cista,cla-va,cla-viger,cla-vis,clipeus,cloa-ca,columna,corrigia,cothurnus,crepida,cri-brum,cubiculum,culi-na,culter,cu-na-bula,currus,cuspis,de-na-rius,draco-,eques,fabricor,falx,fascis,fax,fenestra,follis,foris,forum,fossor,frenum,funda,galea,gladia-tor,gla-ns,gradus,guberna-tor,habe-na,hasta,hostia,ia-nua,impluvium,i-nfula,iugum,lampas,lare-s,larva,lectulus,lectus,li-bra,li-ctor,linter,lituus,lo-ri-ca,lo-rum,lucerna,luctor,macellum,ma-lus,mendi-cus,mitra,mola,monumentum,mu-rex,nu-dus,nu-pta,ocrea,o-stium,pa-la,palla,pa-nis,parie-s,parma,pecten,Pena-te-s,pergula,perso-na,pessulus,petasus,pictor,pictu-ra,pi-leus,plaustrum,pondus,po-ns,postis,Pyrrhicha,quadri-ga,ratis,re-te,rota,rutrum,sa-ga,sagitta,sagitta-rius,salta-tio-,sarcina,sce-ptrum,sculptor,scu-tum,secu-ris,sella,sepulcrum,signum,silex,si-strum,soccus,solea,solium,spi-culum,sta-men,stilus,sti-va,subsellium,supplex,tabella,taberna-culum,taeda,te-gula,te-la,thea-trum,ti-bia,toga,torque-s,torus,tri-cli-nium,tubicen,tugurium,tumulus,tunica,turris,tu-s,typanum,umbo-,u-rna,uter,va-gi-na,ve-na-bulum,ve-na-tor,vesta-lis,virga,vitta
FP: anas,a-nulus,arbor,arca,caper,cervus,cochlea,coro-na,liber,mu-s,na-vis,ovu-m,penna,piscis,puteus,rex,taurus
GLS: a-nser,avis,bo-s,canis,equus,folium,fru-ctus,lu-na,oculus,pa-vo-,pe-s,rosa,serpe-ns,ste-lla
