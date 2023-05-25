import json

# read json file
from_json_file = "alpaca_data-0-3252-中文-已完成.json"
to_vicuna_format_json_file = "vicuna_finetuning_data.json"
with open(from_json_file, 'r') as json_file:
    json_list = json.load(json_file)


id_prefix = "identity_"
to_json_list = []
for index, json_obj in enumerate(json_list):
    id = f"{id_prefix}{index}"
    to_json = {
        "id": id,
        "conversations": [
            {
                "from": "human",
                "value": json_obj["instruction"]
            },
            {
                "from": "gpt",
                "value": json_obj["output"]
            }
        ]
    }
    to_json_list.append(to_json)


# write json list to file
print(f"json list len={len(to_json_list)}")
with open(to_vicuna_format_json_file, "w") as to_json_file:
    json.dump(to_json_list, to_json_file, ensure_ascii=False)
