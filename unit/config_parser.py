# coding:utf-8
import configparser


class _ConfigParser():
    """瀵归厤缃枃浠舵搷浣滅被"""

    def get_value_from_config(self, file_name, section_value, key_value):
        """浠庨厤缃枃浠惰鍙栦俊鎭�"""
        cp = configparser.ConfigParser()
        cp.read(file_name)
        v = cp.get(section_value, key_value)
        return v
    False