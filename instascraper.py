#!/usr/bin/env python3
import sys
import os
import argparse
import requests
import urllib
from bs4 import BeautifulSoup
from datetime import date
import csv
import ssl
import json
import webbrowser
from pprint import pprint
from tqdm import tqdm


class InstaPostScraper:

    def __init__(self, url):
        self.id = url.split('/')[4]
        self.url = "https://www.instagram.com/p/{}".format(self.id)
        self.author = ''
        self.caption = ''
        self.source = ''
        self.likes = ''
        self.date_scraped = ''
        self.location = ''
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def getData(self):
        html = urllib.request.urlopen(str(self.url), context=self.ctx).read()
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find('script', text=lambda t:
                           t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        base_data = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']
        self.src = str(base_data['display_resources'][2]['src'])
        self.author = str(base_data['owner']['username'])
        self.caption = str(
            base_data['edge_media_to_caption']['edges'][0]['node']['text'])
        self.likes = str(base_data['edge_media_preview_like']['count'])
        try:
            self.location = str(json.loads(
                base_data['location']['address_json'])['city_name'])
        except:
            self.location = "N/A"
        self.date_scraped = date.today().strftime("%B %d, %Y")
        self.preview = "<img src='./files/{0}.jpg' height='150px' />".format(
            self.id)
        self.source_link = "<a href='{}' target='_blank'>source</a>".format(
            self.src)
        self.author_link = "<a href='https://instagram.com/{}' target='_blank'>@{}</a>".format(
            self.author, self.author)
        self.post_link = "<a href='https://instagram.com/p/{}' target='_blank'>post</a>".format(
            self.id)

    def download_image(self):
        if not os.path.exists('files'):
            os.makedirs('files')
        urllib.request.urlretrieve(self.src, "files/{}.jpg".format(self.id))

    def scrape(self):
        self.getData()
        self.download_image()
        return [self.url, self.src, self.author, self.caption, self.likes, self.location, self.date_scraped]

    def get_html(self):
        return [self.post_link, self.source_link, self.author_link, self.caption, self.likes, self.location, self.preview, self.date_scraped]


def main(input_file, output_file='output'):
    lines = open(input_file).read().splitlines()
    output_csv = "{}.csv".format(output_file)
    output_html = "{}.html".format(output_file)
    output_html_file = open(output_html, "w")
    table = """
        <html>\n
        <head>\n
        <link rel="stylesheet" href="https://unpkg.com/purecss@1.0.1/build/pure-min.css" integrity="sha384-oAOxQR6DkCoMliIh8yFnu25d7Eq/PHS21PClpwjOTeU2jRSq11vu66rf90/cZr47" crossorigin="anonymous">\n
        <title>InstaScrape - Results </title>\n
        </head>\n
        <body>\n
        <table class="pure-table">\n
    """
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        header = ["Url", "Source", "Author", "Caption",
                         "Likes", "Location", "Date scraped"]
        html_header = ["Original", "Source", "Author", "Caption",
                       "Likes", "Location", "Preview", "Date scraped", "Scheduled"]
        writer.writerow(header)
        table += "<thead>\n"
        table += "  <tr>\n"
        for column in html_header:
            table += "<th>{0}</th>\n".format(column)
        table += "  </tr>\n"
        table += "</thead>\n"
        table += "<tbody>\n"
        for i in tqdm(range(len(lines))):
            link = lines[i]
            post = InstaPostScraper(link)
            post_data = post.scrape()
            writer.writerow(post_data)
            html_data = post.get_html()
            table += "  <tr>\n"
            for col in html_data:
                table += "    <td>{0}</td>\n".format(col)
            table += "<td > <input type = 'checkbox' /></td>\n"
            table += "  </tr>\n"
    table += "</tbody></body></table></html>"
    output_html_file.writelines(table)
    output_html_file.close()
    webbrowser.open('file://' + os.path.realpath(output_html))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="instascraper",
        description="Instascraper is a batch scraper for instagram"
    )
    parser.add_argument(
        "-i",
        "--input",
        nargs=1,
        required=True,
        metavar="input_file.txt",
        help="""The input file with the links for the Instagram. There should be\
                one link per line."""
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs=1,
        default="output",
        metavar="result",
        help="""The output file name. Two files will be generated with a CSV and\
                HTML extension"""
    )

    args = parser.parse_args()
    main(args.input[0], args.output)
