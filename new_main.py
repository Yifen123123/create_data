import json
from create_image_data_en import apply_fake_text

image_path = 'sample/data_001_whiteout.png'
position_path = 'sample/data_001_positions.txt'
json_path = 'data/all_cases.json'

# 讀取 JSON，格式為 list of dicts，每個 dict 代表一組資料
with open(json_path, 'r', encoding='utf-8') as f:
    all_cases = json.load(f)

# 依序處理每一組資料
for idx, case in enumerate(all_cases):
    # 每一組 fake_text_list 依照指定欄位順序組合
    fake_text_list = [
        case.get("入院診斷", ""),
        case.get("出院診斷", ""),
        case.get("主訴", ""),
        case.get("病史", ""),
    ]

    try:
        apply_fake_text(
            image_path=image_path,
            position_path=position_path,
            fake_text_list=fake_text_list,
            output_path=f'sample/output_{idx+1}.png'  # 依照 index 命名
        )
    except Exception as e:
        print(f"❌ 第 {idx+1} 筆資料處理失敗：{e}")
