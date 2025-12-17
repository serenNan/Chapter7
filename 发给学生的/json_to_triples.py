import json
import os
import glob


def make_literal(value):
    """生成 RDF 字面量"""
    # 转义双引号和反斜杠
    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'


def convert_relationship_json(data):
    """
    转换 relationship.json 格式 (含RECORDS数组，RA/RB/relationship字段)
    gCloud格式: <主体> <谓词> <客体>.
    """
    triples = []
    records = data.get('RECORDS', [])
    for record in records:
        ra = record.get('RA', '')
        rb = record.get('RB', '')
        relationship = record.get('relationship', '')
        if ra and rb and relationship:
            triples.append(f"<{ra}> <{relationship}> <{rb}>.")
    return triples


def convert_allRelationship_json(data):
    """
    转换 allRelationship.json 格式 (含RECORDS数组，只有relationship字段)
    gCloud格式: <关系名> <类型> <关系>.
    """
    triples = []
    records = data.get('RECORDS', [])
    for record in records:
        relationship = record.get('relationship', '')
        if relationship:
            triples.append(f"<{relationship}> <类型> <关系>.")
    return triples


def convert_allRelationship2_json(data):
    """
    转换 allRelationship2.json 格式 (数组，sourceType/targetType/relation字段)
    gCloud格式: <sourceType> <relation> <targetType>.
    """
    triples = []
    for record in data:
        source_type = record.get('sourceType', '')
        target_type = record.get('targetType', '')
        relation = record.get('relation', '')
        if source_type and target_type and relation:
            triples.append(f"<{source_type}> <{relation}> <{target_type}>.")
    return triples


def convert_allType_json(data):
    """
    转换 allType.json 格式 (数组，typeName/url字段)
    gCloud格式: <类型名> <类型> <实体类型>. 及 icon属性
    """
    triples = []
    for record in data:
        type_name = record.get('typeName', '')
        url = record.get('url', '')
        if type_name:
            triples.append(f"<{type_name}> <类型> <实体类型>.")
            if url:
                triples.append(f"<{type_name}> <icon> {make_literal(url)}.")
    return triples


def json_to_triples(input_file, output_file):
    """
    读取JSON文件，根据文件名选择合适的转换方法
    输出格式: <主体> <关系> <客体>
    """
    filename = os.path.basename(input_file)

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # * 核心逻辑: 根据文件名选择对应的转换方法
    if filename == 'relationship.json':
        triples = convert_relationship_json(data)
    elif filename == 'allRelationship.json':
        triples = convert_allRelationship_json(data)
    elif filename == 'allRelationship2.json':
        triples = convert_allRelationship2_json(data)
    elif filename == 'allType.json':
        triples = convert_allType_json(data)
    else:
        print(f"跳过未知格式文件: {filename}")
        return 0

    with open(output_file, 'w', encoding='utf-8') as f:
        for triple in triples:
            f.write(triple + '\n')

    print(f"[{filename}] 转换完成! 共生成 {len(triples)} 条三元组 -> {os.path.basename(output_file)}")
    return len(triples)


def process_all_json_files(data_dir, output_dir):
    """
    处理data目录下所有JSON文件
    """
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    total_triples = 0

    print(f"找到 {len(json_files)} 个JSON文件\n")

    for json_file in json_files:
        filename = os.path.basename(json_file)
        # 跳过 allItem.json (内容不是有效JSON)
        if filename == 'allItem.json':
            print(f"[{filename}] 跳过 (非标准JSON格式)")
            continue

        output_name = filename.replace('.json', '.nt')
        output_file = os.path.join(output_dir, output_name)
        count = json_to_triples(json_file, output_file)
        total_triples += count

    print(f"\n全部完成! 总计生成 {total_triples} 条三元组")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    output_dir = script_dir

    process_all_json_files(data_dir, output_dir)
