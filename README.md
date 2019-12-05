# Instascraper

Instascraper is a Python script to scrape batches of instagram posts.

## Usage

Your input file should be a text file with one link to a post on each line (e.g. `https://instagram/p/{post_id}`)

```bash
$ python3 instascraper.py --help
usage: instascraper [-h] -i input_file.txt [-o result]

Instascraper is a batch scraper for instagram

optional arguments:
  -h, --help            show this help message and exit
  -i input_file.txt, --input input_file.txt
                        The input file with the links for the Instagram. There
                        should be one link per line.
  -o result, --output result
                        The output file name. Two files will be generated with
                        a CSV and HTML extension
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
