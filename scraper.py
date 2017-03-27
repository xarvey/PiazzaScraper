import json
import csv
import re
import html
from piazza_api import Piazza

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    unescape_clean_text = html.unescape(cleantext)
    return unescape_clean_text.encode("utf8")


def generate_csv(users, results):
    # Remove the TA from the list
    users = list(filter(lambda n: n.get('role') != 'ta', users))

    # All the posts start with children
    print(list(results))
    results = results.get('children')

    all_replies = sum([child.get('children') for child in results], [])

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


def main():
    p = Piazza()
    p.user_login()
    classId = input("Enter your class id")
    classObj = p.network(classId)
    postId = input("Enter post number")
    posts = classObj.get_post(postId)
    all_users = classObj.get_all_users()

    generate_csv(all_users, posts)


if __name__ == '__main__':
    main()
