# gutenberg_downloader

Downloader used to create the dataset for deeplearning on book genre detection


## Description
The purpose of these scripts is to be used as a tool to download publicly available txt books for academic purposes on creating datasets for training neuronal network. It uses https://pypi.org/project/Gutenberg/


## Usage
Use bookDownloader to get the source txt books. Then use dataSetCreator for a basic dataset with the books

Curretnly the book genre "selection" is hardcoded and depends from the metadata available:
```
	genreKeys = collections.OrderedDict({
		"SciFi": ["cience Fiction", "cience fiction"],
		"Fantasy": ["Fantasy", "fantasy"],
		"Horror": [" horror", "Horror", " Scary", " scary", " terror", "Terror"],
		"Mistery": [" mistery", "Mistery", " detective", " Detective"],
		"Thriller": ["Thriller", " thriller", "Suspense", " suspense"],
		"Adventure": [" adventure", "Adventure"],
		"Romance": ["omance", "omantic"],
		"GenFiction": ["-- Fiction"],
		"Poetry": [" poetry", "Poetry", " poem", "Poem", "Song", " song", " rhyme", "Rhyme", " verses", "Verses"]
		})
```



