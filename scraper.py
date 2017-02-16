import json
import csv
import html
import re
import unicodedata


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    unescape_clean_text = html.unescape(cleantext)
    return unescape_clean_text.encode("utf8")


def main():
    with open('all_users.json') as data_file:
        users = json.load(data_file)

    # Remove the TA from the list
    users = list(filter(lambda n: n.get('role') != 'ta', users))

    with open('result.json') as data_file:
        results = json.load(data_file)

    # All the posts start with children
    results = results.get('children')

    all_replies = sum([child.get('children') for child in results],[])
    print(all_replies)

    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["Name", "Email", "Post Content", "Reply Content"])

        for user in users:
            student_posts = filter(lambda n: n.get('uid') == user['id'], results)
            try:
                subject = cleanhtml(student_posts.__next__().get('subject'))
            except StopIteration:
                subject = ''

            student_reply = filter(lambda n: n.get('uid') == user['id'], all_replies)
            reply_subject = []
            try:
                while 1:
                    reply_subject.append(cleanhtml(student_reply.__next__().get('subject')))
            except StopIteration:
                pass

            writer.writerow([user['name'], user['email'], subject, [reply_single for reply_single in reply_subject]])


if __name__ == '__main__':
    main()
