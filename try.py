import json

def parse_blocks(lines: list):
    blocks = []
    current = {}
    key_order = ["入院診斷", "出院診斷", "主訴", "病史"]
    current_key = None
    buffer = []
    key_idx = 0

    for line in lines + ["==="]:
        line = line.strip()
        if line in key_order:
            if current_key and buffer:
                current[current_key] = "\n".join(buffer)
                buffer = []
            current_key = line
            key_idx += 1

        elif line == "-":
            continue
        elif line == "===":
            if current_key and buffer:
                current[current_key] = "\n".join(buffer)
                buffer = []

            if len(current) == 4:
                blocks.append(current)
            current = {}
            current_key = None
            key_idx = 0
        else:
            content = line[2:] if line.startswith("- ") else line
            buffer.append(content)

    return blocks

def convert_txt_to_single_json(input_txt_path: str, output_json_path: str):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        lines = [line for line in f if line.strip()]

    blocks = parse_blocks(lines)

    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(blocks, f, ensure_ascii=False, indent=2)

    print(f"✅ 已轉換成單一 JSON 檔案：{output_json_path}")
    print(f"✔️ 共轉換 {len(blocks)} 筆資料")

if __name__ == "__main__":
    convert_txt_to_single_json(
        input_txt_path='generated_text/all_cases.txt',
        output_json_path='generated_text/all_cases.json'
    )
