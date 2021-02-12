# ocr-data
This repository consists of 

* a ground truth OCR data set for historical prints from around 1830. 
* a framework to create and share your own ground truth OCR data sets if you don't own the copyright for the images used. 

## How to get the ground truth OCR data set?
The data set can be found in the `data` directory and consists of a *.mets file for each of the pdfs that were used for transcription and a directory `data/page_transcriptions` that contains the transcriptions of the ground truth in PAGEXML format.
The PDFs are not hosted here, but have to be retrieved from the respective institutions and can then be combined with the transcriptions found here. To compile the data set, please

* download all PDFs listed in the `*.mets` files into the `data/pdf_renamed/` directory and rename them ${identifier}.pdf
* change to the `pipelines` directory and run the `make` command

## How to create your own ground truth OCR data set?

* Collect a set of PDFs from Google Books or the Internet Archive and select a set of Pages that you would like to transcribe
* transcribe the text on the images for each pdf individually with the `ketos transcribe` framework found here http://kraken.re/ketos.html (Kiessling 2019) and store the resulting `*.html` a directory named after the pdfs identifier within the `data/transcriptions` directory.
* Now, you can run the `python create_xml_files.py` for each of the pdfs which will output a data set similar to the one from our case study in this repository and other scholars who would like  to use your data set can reproduce it without you having to publish the Google Books PDF yourself. 

___

Kiessling, Benjamin. “Kraken - an Universal Text Recognizer for the Humanities.” DH Conference Proceedings, vol. 30, 2019.
