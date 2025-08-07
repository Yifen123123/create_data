# txt_to_json_multi_cases.py
import json

def parse_txt_to_multi_json(txt_path: str, json_path: str):
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 依據 "===" 分隔多段病歷
    cases_raw = content.split("===")
    result = []

    for idx, block in enumerate(cases_raw):
        lines = [line.strip() for line in block.strip().splitlines() if line.strip()]
        if not lines:
            continue

        case = {}
        current_key = None
        for line in lines:
            # 辨認標題行
            if line in ["入院診斷", "出院診斷", "主訴", "病史"]:
                current_key = line
                case[current_key] = ""
            elif current_key:
                clean_line = line.lstrip("-").strip()
                if case[current_key]:
                    case[current_key] += "\n" + clean_line
                else:
                    case[current_key] = clean_line

        if len(case) == 4:  # 確保四個欄位都有才收錄
            result.append(case)
        else:
            print(f"⚠️ 第 {idx+1} 組病歷不完整，略過：{case.keys()}")

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✅ 轉換完成，共儲存 {len(result)} 組病歷至 {json_path}")

# 範例執行
if __name__ == "__main__":
    parse_txt_to_multi_json("data/all.txt", "data/all.json")
