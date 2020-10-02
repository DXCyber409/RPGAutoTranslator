import json
import logging
import re
import os
import api

cur_count = 0

# 对指定文本进行日语抽取翻译
def translate(text):
    global cur_count
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
        print("进度:%s, 原文:%s, 抽取:%s, 译文:%s" % (cur_count, text.replace("\n", "\\n"), found, trans_text.replace("\n", "\\n")))
        cur_count = cur_count + 1
    return trans_text

# 对json内容进行翻译
def value_handler(obj):
    if isinstance(obj, str):
        newval = translate(obj)
        return newval
    if isinstance(obj, list):
        newval = []
        for val in obj:
            if isinstance(val, str):
                newval.append(translate(val))
            elif isinstance(val, list):
                for i in range(0, len(val)):
                    val[i] = translate(val[i])
                newval.append(val)
            else:
                newval.append(val)
        return newval
    return obj

print("Translating System.json 系统菜单...")
with open("orig/System.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
jobj["terms"]["commands"] = value_handler(jobj["terms"]["commands"])
for command in jobj["terms"]["messages"].keys():
    jobj["terms"]["messages"][command] = value_handler(jobj["terms"]["messages"][command])
jobj["weaponTypes"] = value_handler(jobj["weaponTypes"])
jobj["equipTypes"] = value_handler(jobj["equipTypes"])
jobj["elements"] = value_handler(jobj["elements"])
jobj["armorTypes"] = value_handler(jobj["armorTypes"])
with open("trans/System.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Actors.json 人物文本...")
with open("orig/Actors.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["name"] = value_handler(item["name"])
with open("trans/Actors.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Armors.json 装备文本...")
with open("orig/Armors.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["description"] = value_handler(item["description"])
    item["name"] = value_handler(item["name"])
with open("trans/Armors.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Items.json 物品文本...")
with open("orig/Items.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["name"] = value_handler(item["name"])
    item["description"] = value_handler(item["description"])
with open("trans/Items.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Skills.json 技能文本...")
with open("orig/Skills.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["name"] = value_handler(item["name"])
    item["message1"] = value_handler(item["message1"])
    item["message2"] = value_handler(item["message2"])
with open("trans/Skills.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating States.json 状态文本...")
with open("orig/States.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["name"] = value_handler(item["name"])
    item["message1"] = value_handler(item["message1"])
    item["message2"] = value_handler(item["message2"])
    item["message3"] = value_handler(item["message3"])
    item["message4"] = value_handler(item["message4"])
with open("trans/States.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Weapons.json 武器文本...")
with open("orig/Weapons.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    item["name"] = value_handler(item["name"])
    item["description"] = value_handler(item["description"])
with open("trans/Weapons.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating Troops.json 战斗文本...")
with open("orig/Troops.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    # item["name"] = value_handler(item["name"])
    for item2 in item["pages"]:
        for item3 in item2["list"]:
            # 只翻译显示文本、选项，其他不处理 401普通文本 402选项文本 408战斗选项文本 102分支选项
            if item3["code"] == 401 or item3["code"] == 402 or item3["code"] == 408 or item3["code"] == 102:
                item3["parameters"] = value_handler(item3["parameters"])
with open("trans/Troops.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

print("Translating CommonEvents.json 事件文本...")
with open("orig/CommonEvents.json", mode="r", encoding="utf-8", buffering=4096) as f:
    jobj = json.loads(f.read())
    cur_count = 1
for item in jobj:
    if item is None:
        continue
    for item2 in item["list"]:
        # 只翻译显示文本、选项，其他不处理 401普通文本 402选项文本 408战斗选项文本 102分支选项
        if item2["code"] == 401 or item2["code"] == 402 or item2["code"] == 408 or item2["code"] == 102:
            item2["parameters"] = value_handler(item2["parameters"])
with open("trans/CommonEvents.json", mode="w", encoding="utf-8", buffering=4096) as f:
    f.write(json.dumps(jobj, ensure_ascii=False))
    f.flush()

for mfile in os.listdir("orig"):
    if not re.match(r"Map\d{3}.json", mfile):
        continue

    print("Translating %s 地图对话文本..." % mfile)
    map_file = open("orig/" + mfile, mode="r", encoding="utf-8", buffering=4096)
    jobj = json.loads(map_file.read())
    cur_count = 1
    map_file.close()

    for item in jobj["events"]:
        if item is None:
            continue
        item["name"] = value_handler(item["name"])
        for page in item["pages"]:
            for item2 in page["list"]:
                # 只翻译显示文本、选项，其他不处理 401普通文本 402选项文本 408战斗选项文本 102分支选项
                if item2["code"] == 401 or item2["code"] == 402 or item2["code"] == 408 or item2["code"] == 102:
                    item2["parameters"] = value_handler(item2["parameters"])

    map_file = open("trans/" + mfile, mode="w", encoding="utf-8", buffering=4096)
    map_file.write(json.dumps(jobj, ensure_ascii=False))
    map_file.flush()
    map_file.close()

print("Done.")
