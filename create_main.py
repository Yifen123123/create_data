from create_image_data_en import apply_fake_text

fake_text_list = [
    "Patient, male, 42 years old, admitted for psychological and behavioral abnormalities due to long-term cocaine addiction. The patient has an 8-year history of cocaine use, with significant increase in frequency and dosage over the past six months. One week prior to admission, he experienced severe hallucinations, delusions, and paranoia, accompanied by cacosmia (reporting smelling putrid odors despite no unusual smells in the environment). The patient also presented with significant visual impairment, including blurred vision, photosensitivity, and reduced visual field, confirmed by ophthalmological examination.",
    "精神狀態：煩躁不安，注意力不集中，思維紊亂",
    "精神行為干預：認知行為療法，每週3次",
    "患者因古柯鹼癖引起的嚴重精神症狀及惡嗅覺，經評估後實施經顱磁刺激治療（TMS），針對前額葉及嗅覺相關腦區進行調節，共計8次療程。治療後惡嗅覺症狀明顯改善，幻覺及妄想症狀亦有所減輕。",
]


apply_fake_text(
    image_path='sample/data_004_whiteout.png',
    position_path='sample/data_004_positions.txt',
    fake_text_list=fake_text_list
)
