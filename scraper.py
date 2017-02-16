import json
import csv
import html
import re
import unicodedata


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    unescape_clean_text = html.unescape(cleantext)
    return unescape_clean_text.encode("utf-8")


def main():
    with open('all_users.json') as data_file:
        users = json.load(data_file)

    # Remove the TA from the list
    users = list(filter(lambda n: n.get('role') != 'ta', users))

    with open('result.json') as data_file:
        results = json.load(data_file)

    # All the posts start with children
    results = results.get('children')

    with open('results.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for user in users:
            student = filter(lambda n: n.get('uid') == user['id'], results)
            try:
                subject = cleanhtml(student.__next__().get('subject'))
            except StopIteration:
                subject = ''

            student_reply = filter(lambda n: n.get('children') == user['id'], results)
            spamwriter.writerow([user['name'], user['email'], subject])


if __name__ == '__main__':
    main()
