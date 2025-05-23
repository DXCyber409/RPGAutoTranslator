import json
import logging
import re
import os
import sys
import traceback
import re
import api

# 对指定文本进行日语抽取翻译
def translate(text):
    if len(text) == 0:
        return ""
    # text = "ーーーーーー基礎ヤラレモーションーーーーーー"
    # text = "～どうでもいいイベント用"
    if (text.startswith("ー") or text.startswith("～")):
        return text
    trans_text = text
    # 抽取日语词组短语句子进行翻译，避免破坏原文格式
    found = re.findall("([㐀-䶵一-龥ぁ-ㄩ９-～、-〗]{2,})", text, re.M)
    if (found):
        for part in found:
            trans_part = api.translate(part)
            trans_text = trans_text.replace(part, trans_part, 1)
        print("原文:%s, 抽取:%s, 译文:%s" % (text.replace("\n", "\\n"), found, trans_text.replace("\n", "\\n")))
    return trans_text

input_file = r"D:\機械の少女が夢見た世界\ManualTransFile.json"
with open(input_file, mode="r", encoding="utf-8") as fp:
    res = json.load(fp)

start_count = 1  # 中断后继续翻译用
counter = 1
try:
    for key, value in res.items():
        if counter < start_count:
            counter = counter + 1
            continue
        value2 = translate(value)
        print("当前翻译进度:", counter, value, value2)
        res[key] = value2
        counter = counter + 1
        if counter > 0 and counter % 500 == 0:
            with open(input_file, mode="w", encoding="utf-8") as fp:
                json.dump(res, fp, indent=4, ensure_ascii=False)
            print("存档完成")
except:
    with open(input_file, mode="w", encoding="utf-8") as fp:
        json.dump(res, fp, indent=4, ensure_ascii=False)
    print("存档完成")

    traceback.print_exc()

print("Done.")
