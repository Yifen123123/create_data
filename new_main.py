import json
import os
from create_image_data_en import apply_fake_text

def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_positions(position_path):
    with open(position_path, 'r', encoding='utf-8') as f:
        return eval(f.read())

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    # 固定樣板圖與座標
    image_template = "sample/data_001_whiteout.png"
    position_template = "sample/data_001_positions.txt"
    output_dir = "output"
    ensure_dir(output_dir)

    # 載入全部資料
    records = load_json("data/all.json")
    positions = load_positions(position_template)

    for idx, record in enumerate(records):
        try:
            fake_text_list = [
                record["入院診斷"],
                record["出院診斷"],
                record["主訴"],
                record["病史"]
            ]
        except KeyError as e:
            print(f"❌ 第 {idx+1} 筆資料缺欄位：{e}")
            continue

        output_path = os.path.join(output_dir, f"data_001_result_{idx+1:03d}.png")

        # 執行填寫
        try:
            apply_fake_text(
                image_path=image_template,
                position_path=position_template,
                fake_text_list=fake_text_list,
                output_path=output_path  # 修改 apply_fake_text 讓你可以指定輸出路徑
            )
            print(f"✅ 已輸出：{output_path}")
        except Exception as e:
            print(f"❌ 第 {idx+1} 筆處理失敗：{e}")

if __name__ == '__main__':
    main()





def apply_fake_text(image_path: str, position_path: str, fake_text_list: list, default_size: int = 24, output_path: str = None):
    from os.path import splitext

    image = read_image_pil(image_path)

    with open(position_path, 'r') as f:
        positions = eval(f.read())

    if len(fake_text_list) != len(positions):
        raise ValueError("❌ 假資料筆數與位置數量不符！")

    filled_image, used_size = first_auto_fill(positions, image, default_size, fake_text_list)

    if output_path is None:
        path_and_name, suffix = splitext(image_path)
        output_path = path_and_name + '_filled' + suffix

    save_image_pil(filled_image, output_path)
    print(f"✅ 已儲存填入假資料後圖片：{output_path}")
    print(f"✏️ 使用字體大小：{used_size}")

