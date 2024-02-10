# Tips and Tricks for OCRing macronized books in Latin

## Training an OCR model

I had to install `hocr-tools` and `ocrmypdf` and `git clone`d [Tesstrain](https://github.com/tesseract-ocr/tesstrain) for the below.

```sh
ocrmypdf "HC Nutting - A First Latin Readder.pdf" - --output-type=none -l Latin_macron --pages 21-30 --force-ocr --sidecar ./test.txt --oversample 400 > ./test.out -k --pdf-renderer hocr
# note the location in /tmp that the hocrs outputted for the below
for i in {017..025}
do
	hocr-extract-images /tmp/ocrmypdf.io.s4hxwvnw/000${i}_ocr_hocr.hocr -p roliv-${i}-line-%04d.gt.png 
done
rename '.gt' '' *.png
```

For some books, I found adding `-e ocr_par` to the `hocr-extract-images` command gave more lines.
I then manually edited the `.txt` files (see Vim section below) to make sure the text was correct.
Once I had a folder of `.gt.txt` and `.png` files from the above, I made a few edits to the Makefile (e.g. `START_MODEL = lat`) and then ran `make training` to generate the final `.traineddata` file.
I then ran this model against a book again to generate more `.gt.txt` and `.png` files and then re-ran it again on those, etc.

## OCRing a Book

I used ocrmypdf (which uses tesseract under the hood) on Arch Linux for the following.

1. Put `Latin_macron.traineddata` in /usr/share/tessdata.
2. Run, e.g.:
```sh
ocrmypdf "Appleton - Fabulae.pdf" - --output-type=none -l Latin_macron --pages 17-146 --force-ocr --sidecar ./test.txt --oversample 400 > ./test.out 
```
3. Clean up the resulting PDF.

## Generating a dictionary file

The `process_kaiki.py` script here will generate a `latin_words.txt` file that can be used for various purposes.

The `latin_words.txt.bz2` is a compressed version of its output generated from a dump downloaded on February 7th, 2024.
 
## Vim

Run the following to import the word list and generate a Vim dictionary from it:
```
mkspell ~/.vim/spell/la ./latin_words.txt
```
To highlight misspellings, I added the following to my .vimrc before my colorscheme:
```vim
autocmd ColorScheme gruvbox hi SpellBad cterm=underline
```
I could then type `set lang spelllang=la` when I opened a file to see which words were correct.

Vim supports most macron letters with digraphs (e.g. press `^K`, then `a`, then `-` to get ā), but not macronized 'y's; I added the following to my vimrc to get those too:
```vim
dig y- 563
dig Y- 562
```
