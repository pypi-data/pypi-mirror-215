from collections import OrderedDict

import suricataparser
from django.http.response import HttpResponse, JsonResponse
from snort.models import SnortRule, SnortRuleViewArray
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .parser import Parser, SerializeRule
from settings.models import keyword
from settings.models import Setting
from django.core.serializers import serialize
# Create your views here.

def get_rule_keys(request, rule_id=None):
    rule_keywordss = SnortRuleViewArray.objects.filter(**{"snortId": rule_id})
    results = {"data": []}
    for rule_key in rule_keywordss:
        results["data"].append({"htmlId": rule_key.htmlId, "value": rule_key.value, "typeOfItem": rule_key.typeOfItem,
                        "locationX": rule_key.locationX, "locationY": rule_key.locationY})
    return JsonResponse(results)


def get_rule(request, rule_id=None, cloned=None):
    if (request.session.get("instance")):
        r_value = HttpResponse(json.loads(request.session.pop("instance"))[0]["fields"]["content"])
        return r_value
    full_rule = SnortRule.objects.get(**{"id": rule_id}).content
    return HttpResponse(full_rule)

@csrf_exempt
def build_rule_keyword_to_rule(request, full_rule=""):
    if not full_rule and request.method == "POST":
        try:
            full_rule = json.loads(request.body.decode()).get("fule_rule")
        except:
            pass
    resppnse = {"data": []}
    if not full_rule:
        return JsonResponse(resppnse)
    rule_parsed = Parser(full_rule.replace("sid:-;", ""))
    build_keyword_dict(resppnse, rule_parsed)
    return JsonResponse(resppnse)

@csrf_exempt
def build_rule_parse(request, full_rule=""):
    if not full_rule and request.method == "POST":
        try:
            full_rule = request.body.decode()
        except:
            pass
    resppnse = {}
    if not full_rule:
        return JsonResponse(resppnse)
    try:
        rule_parsed = Parser(full_rule.replace("sid:-;", ""))
    except:
        print(full_rule.replace("sid:-;", ""))
        raise
    rule_kw = {"options": {}}
    rule_kw["action"] = rule_parsed.all["header"].get("action", "alert")
    rule_kw["protocol"] = rule_parsed.all["header"].get("proto")
    rule_kw["not_src_ip"] = not rule_parsed.all["header"].get("source", (False, "any"))
    rule_kw["src_ip"] = rule_parsed.all["header"].get("source", (False, "any"))[1]
    rule_kw["not_src_port"] = not rule_parsed.all["header"].get("src_port", (False, "any"))[0]
    rule_kw["src_port"] = rule_parsed.all["header"].get("src_port", (False, "any"))[1]
    rule_kw["direction"] = rule_parsed.all["header"].get("arrow", "->")
    rule_kw["not_dst_ip"] = not rule_parsed.all["header"].get("destination", (False, "any"))[0]
    rule_kw["dst_ip"] = rule_parsed.all["header"].get("destination", (False, "any"))[1]
    rule_kw["not_dst_port"] = not rule_parsed.all["header"].get("dst_port", (False, "any"))[0]
    rule_kw["dst_port"] = rule_parsed.all["header"].get("dst_port", (False, "any"))[1]
    # build_keyword_dict(resppnse, rule_parsed)
    rule_kw["options"] = []
    unparsed = ""
    unparsed_count = 0
    for index, option in rule_parsed.options.items():
        if option[0] in ["sid", "msg", "metadata", "description"]:
            unparsed_count += 1
            continue
        try:
            format = keyword.objects.filter(name=option[0], stage="options", available=True)[0].options.split(",")
        except:
            unparsed += option[0] + ":" + ",".join(option[1]) + ";"
            unparsed_count += 1
            continue
        parsed_index = index - unparsed_count
        format_index = 0
        first_int_connected = False
        splited = False
        rule_kw["options"].append({"option": option[0]})
        if format[format_index] == "[!]":
            if option[1][0].strip('"').startswith("!"):
                rule_kw["options"][parsed_index][option[0]] = True
                option[1][0] = option[1][0].lstrip("!")
            format_index += 1
        elif format[format_index] == "int":
            # check if first object is int
            if option[1][0].strip('"').isnumeric():
                splited = True
                first_int_connected = True
                option_name = option[0] + str(format_index) if format_index else option[0]
                rule_kw["options"][parsed_index][option_name] = int(option[1].pop(0).strip('"'))
            format_index += 1
        if format[format_index].startswith("{") and format[format_index].endswith("}"):
            format_options = format[format_index][1:-1].split("|")
            format_options = sorted(format_options, key=lambda  x: -1*len(x))
            for format_option in format_options:
                if not first_int_connected and format_index > 0 and format[format_index - 1] == "int" and format_option in option[1][0]:
                    if option[1][format_index - 1].strip('"').split(format_option)[0].isnumeric():
                        first_int_connected = True
                        splited = False
                        option_name = option[0] + str(format_index - 1) if format_index - 1 else option[0]
                        rule_kw["options"][parsed_index][option_name] = int(option[1][format_index - 1].strip('"').split(format_option)[0])
                        option[1][format_index - 1] = option[1][format_index - 1].strip('"')[len(option[1][format_index - 1].strip('"').split(format_option)[0]):]
                if option[1][format_index - (not splited)].startswith(format_option):
                    if len(option[1][format_index - (not splited)]) > len(format_option):
                        option[1][format_index - (not splited)] = option[1][format_index - (not splited)][len(format_option):]
                        option_name = option[0] + str(format_index) if format_index else option[0]
                        rule_kw["options"][parsed_index][option_name] = format_option
                        format_index += 1
                        break

        option_name = option[0] + str(format_index) if format_index else option[0]
        if format[format_index] == "int":
            rule_kw["options"][parsed_index][option_name] = int(option[1][0].strip('"'))
        else:
            rule_kw["options"][parsed_index][option_name] = option[1][0].strip().strip('"')

        if len(option[1]) > 1:
            if isinstance(option[1], list):
                rule_kw["options"][parsed_index][option[0] + "_modifer"] = {}
                for kw_index, pair in enumerate(option[1][1:]):
                    if len(pair.split(" ")) > 1:
                        try:
                            modifier_format = keyword.objects.filter(
                                name=pair.split(" ")[0],
                                stage=option[0] + "_modifer", available=True)[0].options.split(",")[0]
                        except:
                            modifier_format = "int"

                        if " ".join(pair.split(" ")[1:]).isnumeric() and modifier_format == "int":
                            rule_kw["options"][parsed_index][option[0] + "_modifer"][pair.strip().split(" ")[0]] = int(" ".join(
                                pair.strip().split(" ")[1:]))
                        else:
                            rule_kw["options"][parsed_index][option[0] + "_modifer"][pair.strip().split(" ")[0]] = " ".join(pair.strip().split(" ")[1:])
                    else:
                        rule_kw["options"][parsed_index][option[0] + "_modifer"][pair.strip().split(" ")[0]] = True
            elif isinstance(option[1], str):
                rule_kw["options"][parsed_index][option_name] = option[1].strip().strip('"')
    if unparsed:
        rule_kw["unparsed_data"] = unparsed
    return JsonResponse(rule_kw)
@csrf_exempt
def build_rule_serialize(request):
    DO_NOT_QOUTE = Setting.objects.get(name="DO_NOT_QUOTE").value.split(",")
    full_rule = json.loads(request.body.decode())
    rule_kw = {"header": OrderedDict(), "options": OrderedDict()}
    # get headers
    rule_kw["header"]["action"] = full_rule.get("action")
    rule_kw["header"]["proto"] = full_rule.get("protocol")
    rule_kw["header"]["source"] = (not full_rule.get("not_src_ip", False), full_rule.get("src_ip", "any"))
    rule_kw["header"]["src_port"] = (not full_rule.get("not_src_port", False), full_rule.get("src_port", "any"))
    rule_kw["header"]["arrow"] = full_rule.get("direction", "->")
    rule_kw["header"]["destination"] = (not full_rule.get("not_dst_ip", False), full_rule.get("dst_ip", "any"))
    rule_kw["header"]["dst_port"] = (not full_rule.get("not_dst_port", False), full_rule.get("dst_port", "any"))

    # get options
    for index, option in enumerate(full_rule["options"]):
        modifer = {}
        rule_kw["options"][index] = option.pop("option"),list()
        for key in list(option.keys()):
            if f"{rule_kw['options'][index][0]}_modifer" in key:
                modifer = option.pop(key)
        for op_key, op_value in sorted(option.items()):
            if op_key.startswith(rule_kw["options"][index][0]):
                append_value = ""
                if isinstance(op_value, str):
                    append_value = f'"{op_value}"' if rule_kw['options'][index][0] not in DO_NOT_QOUTE else f'{op_value}'
                elif isinstance(op_value, bool):
                    if op_value:
                        append_value = "!"
                elif isinstance(op_value, int):
                    append_value = str(op_value)
                if len(rule_kw["options"][index][1]) > 0:
                    rule_kw["options"][index][1][0] += append_value
                else:
                    rule_kw["options"][index][1].append(append_value)
        for item_key, item_value in modifer.items():
            if isinstance(item_value, bool):
                if item_value:
                    rule_kw["options"][index][1].append(item_key)
            else:
                rule_kw["options"][index][1].append(item_key + " " + str(item_value))

    data = SerializeRule(rule_kw).serialize_rule()
    if full_rule.get("unparsed_data"):
        data = data[:-1] +full_rule.get("unparsed_data") + ")"
    return JsonResponse({"content": data})
@csrf_exempt
def get(request, stage=""):
    if not stage:
        data = keyword.objects.filter(available=True)
    else:
        data = keyword.objects.filter(stage=stage, available=True)
    data = serialize("json", data)
    return JsonResponse(json.loads(data), safe=False)


def get_current_user_name(request):
    return JsonResponse({"user": getattr(request.user, request.user.USERNAME_FIELD)})


def build_keyword_dict(resppnse, rule_parsed):
    if not rule_parsed:
        return
    rule_keywordss = [build_keyword_item("action", rule_parsed.header["action"]),
                      build_keyword_item("protocol", rule_parsed.header["proto"]),
                      build_keyword_item("srcipallow", "!" if not rule_parsed.header["source"][0] else "-----"),
                      build_keyword_item("srcip", rule_parsed.header["source"][1], item_type="input"),
                      build_keyword_item("srcportallow", "!" if not rule_parsed.header["src_port"][0] else "-----"),
                      build_keyword_item("srcport", rule_parsed.header["src_port"][1], item_type="input"),
                      build_keyword_item("direction", rule_parsed.header["arrow"]),
                      build_keyword_item("dstipallow", "!" if not rule_parsed.header["destination"][0] else "-----"),
                      build_keyword_item("dstip", rule_parsed.header["destination"][1], item_type="input"),
                      build_keyword_item("dstportallow","!" if not rule_parsed.header["dst_port"][0] else "-----"),
                      build_keyword_item("dstport",rule_parsed.header["dst_port"][1], item_type="input"),
                      ]
    i = 0
    op_num = 0
    for index, op in rule_parsed.options.items():
        if op[0] == "tag":
            if op[1] == ["session", "packets 10"]:
                continue
            if op[1] == ["session","10", "packets"]:
                continue
        if op[0] in ["msg", "sid"]:
            if isinstance(op[1], list):
                resppnse[op[0]] = "".join(op[1]).strip('"').strip('"').strip()
            else:
                resppnse[op[0]] = op[1].strip('"').strip()
            i += 1
            continue
        if op[0] == "metadata":
            for item in op[1]:
                for meta_value in ["group ", "name ", "treatment ", "document ", "description "]:
                    if item.strip("'").strip().startswith(meta_value):
                        resppnse["metadata_" + meta_value.strip()] = item.replace(meta_value, "").strip().strip('"')
                        break
            continue
        rule_keywordss.append(build_keyword_item("keyword_selection" + str(op_num), op[0], x=op_num, y=0))

        if len(op) > 1:
            i=0
            if isinstance(op[1], str):
                op = (op[0], [op[1]])
            for value in op[1]:
                name = f"keyword_selection{str(op_num)}"
                if i > 0:
                    name = f"keyword{op_num}-{i-1}"
                    if ":" in value:
                        rule_keywordss.append(build_keyword_item(name, value.split(":")[0].strip().strip('"').strip("'"), x=op_num, y=i-1))
                        value = value.split(":")[1]
                    else:
                        rule_keywordss.append(
                            build_keyword_item(name, value.strip().split(" ")[0].strip().strip('"').strip("'"), x=op_num,
                                               y=i - 1))
                        value = value.split(" ")[-1]
                    i += 1
                if value.strip().startswith("!"):
                    rule_keywordss.append(
                        build_keyword_item(f"keyword{str(op_num)}" + "-not", "!", x=op_num, y=0,
                                           item_type="input"))
                    value = value.strip()[1:]

                rule_keywordss.append(
                    build_keyword_item(name + "-data", value.strip().strip('"').strip("'"), x=op_num, y=i,
                                       item_type="input"))
                i += 1
        op_num += 1

    for rule_key in rule_keywordss:
        resppnse["data"].append(
            {"htmlId": rule_key["htmlId"], "value": rule_key["value"], "typeOfItem": rule_key["typeOfItem"],
             "locationX": rule_key["locationX"], "locationY": rule_key["locationY"]})


def build_keyword_item(my_id, value, item_type="select", x=0, y=0):
    return {"htmlId": my_id, "value": value, "typeOfItem": item_type,
            "locationX": x, "locationY": y}


# build_rule_keyword_to_rule(None, SnortRule.objects.get(**{"id": 5}).content)
def build_rule_rule_to_keywords(request, rule_keywords=None):
    resppnse = {"fule_rule": ""}
    if not rule_keywords:
        rule_keywords = {}
    return JsonResponse(resppnse)

def favico(request):
    image_data = open(os.path.join(settings.BASE_DIR, "favicon.ico"), "rb").read()
    return HttpResponse(image_data, content_type="image/png")
