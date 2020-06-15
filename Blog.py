import random
import string


class BlogPost:
    def __init__(self, author_id,  author_name, header, content):
        all_characters = string.digits + string.ascii_letters
        blog_id = ''.join((random.choice(all_characters) for i in range(8)))
        self.__id = blog_id
        self.__author_id = author_id
        self.__author_name = author_name
        self.__header = header
        self.__content = content
        self.__upvotes = 0

    def set_author_id(self, author_id):
        self.__author_id = author_id

    def set_author_name(self, author_name):
        self.__author_name = author_name

    def set_header(self, header):
        self.__header = header

    def set_content(self, content):
        self.__content = content

    def get_id(self):
        return self.__id

    def get_author_id(self):
        return self.__author_id

    def get_author_name(self):
        return self.__author_name

    def get_header(self):
        return self.__header

    def get_content(self):
        return self.__content

    def upvote(self):
        self.__upvotes += 1
