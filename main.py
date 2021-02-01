from bs4 import BeautifulSoup
import argparse
import csv
import os
import requests

def extract_section(soup, _id, android_version, out_dir):
    result = soup.find('h3', id=_id)
    if result is None:
        return
    table = result.find_next('table')
    output_rows = []
    x = 0
    aosp_ver_idx = -1
    for table_row in table.findAll('tr'):
        if x == 0:
            columns = table_row.findAll('th')
        else:
            columns = table_row.findAll('td')
        output_row = []
        y = 0
        urls = []
        ignore_row = False
        for column in columns:
            if x == 0:
                if y == 1 or column.text == 'References':
                    output_row.append('Reference ID(s)')
                else:
                    output_row.append(column.text.strip())
                if android_version is not None and column.text == 'Updated AOSP versions':
                        aosp_ver_idx = y
            else:
                if android_version is not None and aosp_ver_idx == y:
                    ignore_row = android_version not in column.text.strip().replace(" ", "").split(',')
                    if ignore_row:
                        break
                for url in column.findAll('a'):
                    href = url.get('href')
                    if href is not None:
                        urls.append(href)
                text = column.text.strip().split('\n')[0] if '\n' in column.text else column.text
                output_row.append(text.strip())
            y += 1
        if x == 0:
            output_row.append('Reference URLs')
            x = 1
        else:
            output_row.append(';'.join(urls))
        if not ignore_row:
            output_rows.append(output_row)
        
    fname = _id + '.csv'
    if out_dir is not None:
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        fname = out_dir + '/' + _id + '.csv' 
    with open(fname, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch-level", type=str, required=True,
            help="Specify the patch you want to scrape (Example: 2021-01-01, 2020-10-05, 2020-09, etc)")
    parser.add_argument("--android-version", type=str,
            help="Android version you want to filter by")
    parser.add_argument("--out-dir", type=str,
            help="Directory in which files must be placed")
    args = parser.parse_args()
    level_parts = args.patch_level.split('-')
    url = 'https://source.android.com/security/bulletin/{}-{}-01'.format(level_parts[0], level_parts[1])
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    extract_section(soup, 'android-runtime', args.android_version, args.out_dir)
    extract_section(soup, 'framework', args.android_version, args.out_dir)
    extract_section(soup, 'media-framework', args.android_version, args.out_dir)
    extract_section(soup, 'system', args.android_version, args.out_dir)
    extract_section(soup, '01android-runtime', args.android_version, args.out_dir)
    extract_section(soup, '01framework', args.android_version, args.out_dir)
    extract_section(soup, '01media-framework', args.android_version, args.out_dir)
    extract_section(soup, '01system', args.android_version, args.out_dir)
    extract_section(soup, 'kernel-compoents', args.android_version, args.out_dir) # Yes, "compoents". Thank you Google, very cool.
    extract_section(soup, 'kernel-components', args.android_version, args.out_dir)
    extract_section(soup, 'kernel', args.android_version, args.out_dir)
    extract_section(soup, '01kernel', args.android_version, args.out_dir)
    extract_section(soup, '05kernel', args.android_version, args.out_dir)


if __name__ == '__main__':
    main()
