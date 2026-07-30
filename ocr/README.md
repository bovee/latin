# Tips and Tricks for OCRing macronized books in Latin

## Training an OCR model

I had to install `hocr-tools` and `ocrmypdf` and `git clone`d [Tesstrain](https://github.com/tesseract-ocr/tesstrain) for the following. Here's a `Makefile` that simplifies the process of building the training data.

```make
FILE=./Craigie-Specimens_of_Anglo_Saxon_Poetry_1
START=012
END=094

ocr:
    # For old english books, use `-l Latin_macron`.
	ocrmypdf "${FILE}.pdf" - --output-type=none -l ang --pages ${START}-${END} --force-ocr --sidecar ./${FILE}.txt --oversample 400 -k &> ./temp.out
    # dump out the PNG/matching TXT for building the training data
	for i in $$(seq -w $(START) $(END)); do \
		hocr-extract-images $$(tail -n 1 ./temp.out)/000$${i}_ocr_hocr.hocr -p ./junk/$$(basename $(FILE))-$${i}-line-%04d.gt.png; \
	done
	rename '.gt' '' ./junk/*.png
```

For some books, I found adding `-e ocr_par` to the `hocr-extract-images` command gave more lines.
I then manually edited the `.txt` files (see Vim section below) to make sure the text was correct.
Once I had a folder of `.gt.txt` and `.png` files from the above, I ran `make training` to generate the final `.traineddata` file.
I then ran this model against a book again to generate more `.gt.txt` and `.png` files and then re-ran it again on those, etc.

The current `Latin_macron` model (v3) was trained with ~1000 new samples from public domain books (on top of `START_MODEL=lat`) and has a minimal training error rate (BCER) of 0.345%.

The current `ang` (Old English) model (v1) was trained with 1360 new samples from public domain books (on top of `START_MODEL=`) and has a BCER of 3.8% and BWER of 10.3%.

## OCRing a Book

I used ocrmypdf (which uses tesseract under the hood) on Arch Linux for the following.

1. Put `Latin_macron.traineddata` in /usr/share/tessdata (or `ang.traineddata` for Old English).
2. Run, e.g.:
```sh
ocrmypdf "Appleton - Fabulae.pdf" - --output-type=none -l Latin_macron --pages 17-146 --force-ocr --sidecar ./test.txt --oversample 400 > ./test.out 
```
3. Clean up the resulting PDF.

## Generating a dictionary file

The `process_kaiki.py` script here will generate a `latin_words_full.txt` file that can be used for various purposes.

The `latin_words_full.txt.bz2` is a compressed version of its output generated from a dump downloaded on February 7th, 2024.

It will also generate `.dic` and `.aff` files that can be used as a Latin dictionary in common word processing applications. These differ slightly from the `txt` version in that they will not flag words with enclictics like `-que`, etc.

A similar `ang_words_full.txt` was generated via `process_kaiki_ang.py` from a ddump downloaded on July 9th, 2026.

## Vim

Run the following to import the word list and generate a Vim dictionary from it:
```
mkspell ~/.vim/spell/la ./latin_words
```
To highlight misspellings, I added the following to my .vimrc before my colorscheme:
```vim
autocmd ColorScheme gruvbox hi SpellBad cterm=underline
```
I could then type `set lang spelllang=la` when I opened a file to see which words were correct.

Vim supports most macron letters with digraphs (e.g. press `^K`, then `a`, then `-` to get ā) and other medieval characters, but not macronized 'y's or insular 'g's; I added the following to my vimrc to type those easily:
```vim
dig y- 563
dig Y- 562
dig g9 7545
dig G9 42877
```

Frequently a single letter only needs to be macronized or unmacronized; here is a short script to do that quickly in addition to handling other common Old English variants (this can be bound to something besides `zz`):
```
function! Macronize()
  let l:char = matchstr(getline('.'), '\%' . col('.') . 'c.')
  let l:char = get({ 'a': 'ā', 'e': 'ē', 'i': 'ī', 'o': 'ō', 'u': 'ū', 'y': 'ȳ', 'æ': 'ǣ', 'c': 'ċ', 'g': 'ġ', 'þ': 'ꝥ', 'l': 'ł', 'd': 'ð', 'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u', 'ȳ': 'y', 'ǣ': 'æ', 'ċ': 'c', 'ġ': 'g', 'ꝥ': 'þ', 'ł': 'l', 'ð': 'd', 'A': 'Ā', 'E': 'Ē', 'I': 'Ī', 'O': 'Ō', 'U': 'Ū', 'Y': 'Ȳ', 'Æ': 'Ǣ', 'C': 'Ċ', 'G': 'Ġ', 'Þ': 'Ꝥ', 'L': 'Ł', 'D': 'Ð', 'Ā': 'A', 'Ē': 'E', 'Ī': 'I', 'Ō': 'O', 'Ū': 'U', 'Ȳ': 'Y', 'Ǣ': 'Æ', 'Ċ': 'C', 'Ġ': 'G', 'Ꝥ': 'Þ', 'Ł': 'L', 'Ð': 'D', '&': '⁊', '⁊': '&', }, l:char, l:char)
  call setline(line('.'), substitute(getline('.'), '\%' . col('.') . 'c.', l:char, ''))
endfunction
map zz :call Macronize()<CR>
```
