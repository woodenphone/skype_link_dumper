#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     17/02/2016
# Copyright:   (c) User 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sqlite3
import re


def find_url_links(html):
    """Find URLS in a string of text"""
    # Should return list of strings
    # Copied from:
    # http://stackoverflow.com/questions/520031/whats-the-cleanest-way-to-extract-urls-from-a-string-using-python
    # old regex http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+
    url_regex = """http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
    links = re.findall(url_regex,html, re.DOTALL)
    #logging.debug("find_url_links() links: "+repr(links))
    assert(type(links) is type([]))# Should be list
    return links

def find_links_href(html):
    """Given string containing '<a href="https://gyazo.com/2273ec1b9754a59b99a02beda539aa1b"'
    return ['https://gyazo.com/2273ec1b9754a59b99a02beda539aa1b']
    """
    embed_regex = """href=["']([^'"]+)["']>"""
    links = re.findall(embed_regex,html, re.DOTALL)
    #logging.debug("find_links_src() links: "+repr(links))
    return links


def list_convos(cursor):
    # List convos
    table_name = 'Conversations'
    columns = 'id, displayname'
    q = 'SELECT %s FROM %s LIMIT 100' % (columns, table_name)

    cursor.execute(q)
    results = cursor.fetchall()

    convos = []
    for result in results:
        print(result)
        convo = {
            'id':result[0],
            'displayname':result[1],
            }
        convos.append(convo)
    return convos


def list_covo_messages(cursor, conversation_id):
    # Grab messages
    table_name = 'Messages'
    columns = 'id, convo_id, author, body_xml'
    q = 'SELECT %s FROM %s WHERE convo_id IS %s' % (columns, table_name, conversation_id)

    c.execute(q)
    results = c.fetchall()

    messages = []
    for result in results:
        #print(result)
        message = {
            'id':result[0],
            'convo_id':result[1],
            'author':result[2],
            'body_xml':result[3],
            }
        messages.append(message)
    return messages


def parse_convo_links(cursor, conversation_id, coversation_name, output_filepath):
    print('parse_convo_links() output_filepath: '+repr(output_filepath))
    with open(output_filepath, 'wb') as of:
        # Write header
        header = '%s<br>\r\n' % (coversation_name)
        header = header.encode('ascii', 'ignore')# Coerce to ascii
        of.write(header)
        # Grab messages
        message_dicts_list = list_covo_messages(cursor, conversation_id)
        # Parse each message
        for message in message_dicts_list:
            #print('message: '+repr(message))
            if not message['body_xml']:
                continue
            message_links = find_links_href(message['body_xml'])
            for message_link in message_links:
                output_line = '<a href="%s">%s</a><br>\r\n' % (message_link, message_link)
                output_line = output_line.encode('ascii', 'ignore')# Coerce to ascii
                print('output_line: '+repr(output_line))
                of.write(output_line)
    return


print( find_links_href(html=u'<a href="https://www.youtube.com/watch?v=b0dH4P0jHJA">https://www.youtube.com/watch?v=b0dH4P0jHJA</a>') )
# Connect
db_path = os.path.join('main.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()


# Setup output location
output_dir = os.path.join('output')
if len(output_dir) != 0:
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except WindowsError, err:
            pass

# Get conversation info
convo_dict_list = list_convos(cursor=c)
# Process for each conversation
for convo_dict in convo_dict_list:
    filename = '%s.html' % (convo_dict['id'])
    parse_convo_links(
        cursor=c,
        conversation_id=convo_dict['id'],
        coversation_name=convo_dict['displayname'],
        output_filepath=os.path.join(output_dir, filename)
        )

#list_covo_messages(cursor=c, conversation_id=238086)
##parse_convo_links(
##    cursor=c,
##    conversation_id=238086,
##    output_filepath=os.path.join('out.txt')
##    )


def main():
    pass

if __name__ == '__main__':
    main()
