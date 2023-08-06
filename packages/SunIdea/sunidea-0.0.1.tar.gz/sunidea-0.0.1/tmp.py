# -*- coding: utf-8 -*-
# @Time : 2023/5/11 11:34
# @Author : sunshuanglong
# @File : tmp.py

from tqdm import tqdm
import time
from SunIdea.sun_module.multi_task import MultiTask
from SunIdea.sun_utils import sun_idea_utils


def fun_job(data_list):
    for item in tqdm(data_list, desc="processing..."):
        for i in range(1000):
            item[f"add_{i}"] = "made by sunxiaowu"
    return data_list


if __name__ == "__main__":

    task_obj = MultiTask(process_num=32)  # 创建多进程任务对象
    t1 = time.time()
    data_list = task_obj.load_jsonl("test.jsonl")  # 数据加载
    # res_list = task_obj.multi_task_processing(data_list, fun_job)  # 多任务切分调用
    t2 = time.time()
    print(t2 - t1)
    data_list2 = sun_idea_utils.parse_jsonls_to_str_list_from_file("test.jsonl")
    print(time.time() - t2)
    # print(len(res_list))  # 得到结果
    # print(res_list[0])
