import urllib
import urllib.request
import json
from datetime import datetime
import re

def get_rule_stage(hour):
    req = urllib.request.Request("https://spla2.yuu26.com/{rule}/schedule".format(rule='league'))
    req.add_header("user-agent", "@penguinone2580")
    with urllib.request.urlopen(req) as res:
        response_body = res.read().decode("utf-8")
        response_json = json.loads(response_body.split("\n")[0])
        data = response_json["result"]
        for d in data:
            start_time = datetime.strptime(d["start"], '%Y-%m-%dT%H:%M:%S')
            end_time = datetime.strptime(d["end"], '%Y-%m-%dT%H:%M:%S')
            start_hour = start_time.strftime("%H")
            if hour == int(start_hour):
                text = "{start} ~ {end}\n{rule}\n{stage1}\t{stage2}".format(
                    start=start_time.strftime("%m/%d %H:%M"),
                    end=end_time.strftime("%m/%d %H:%M"),
                    rule=d["rule_ex"]["name"],
                    stage1=d["maps_ex"][0]["name"],
                    stage2=d["maps_ex"][1]["name"])

                return text

def check_hour(hour):
    if hour==0:
        hour = 23
    elif hour%2==0:
        hour = hour - 1
    return hour

receive_txt = "リグマ21募集"
if ("リグマ" in receive_txt or "リーグマッチ" in receive_txt or "4タグ" in receive_txt) and "募集" in receive_txt:
    league = True

if league:
    hour = int(re.sub("\\D", "", receive_txt))%24
    txt = get_rule_stage(check_hour(hour))
    print(txt)
