# -*- coding: utf-8 -*-
# @Time : 2023/6/26 11:21
# @Author : sunshuanglong
# @File : sun_idea_utils.py
import tqdm
import json


def parse_jsonls_to_str_list(data_list):
    res_list = list()
    for item in tqdm(data_list, desc="to_json..."):
        res_list.append(json.loads(item))
    return res_list


def parse_jsonls_to_str_list_from_file(file_path):
    res_list = list()
    data_list = open(file_path, "r", encoding="utf-8").read().strip().split("\n")
    for item in data_list:
        res_list.append(json.loads(item))
    return res_list
