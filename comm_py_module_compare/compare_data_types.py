import re
from collections import defaultdict
from itertools import product


def compare_data_types(dict_source,dict_target,db_type_source,db_type_target):
    # 1. 统一键名大小写
    normalized_dict1 = {k.upper(): {ik.upper(): iv.upper() for ik, iv in v.items()}
                        for k, v in dict_source.items()}
    normalized_dict2 = {k.upper(): {ik.upper(): iv.upper() for ik, iv in v.items()}
                        for k, v in dict_target.items()}

    # 2. 定义类型映射规则（Oracle → MySQL）
    type_mapping = {
        #类型映射
        'NUMBER': ['INT', 'BIGINT', 'DECIMAL'],
        'VARCHAR2': ['VARCHAR'],
        'DATE': ['DATETIME'],
        'CLOB': ['TEXT']

    }
    # 3. 结构差异检测
    diff_report = []
    all_tables = set(normalized_dict1) | set(normalized_dict2)

    for table in all_tables:
        # 表存在性检查
        if table not in normalized_dict1:
            diff_report.append({  # 使用字典结构记录差异
                'table': table,
                'field': None,  # 表级差异无需字段
                'diff_type': '表缺少',
                'source_db': db_type_source,
                'target_db': db_type_target,
                'description': f"表:{table}仅存在于 {db_type_target}"
            })
            continue
        if table not in normalized_dict2:
            #diff_report[table].append(f"表仅存在于: {db_type_source}")
            diff_report.append({  # 使用字典结构记录差异
                'table': table,
                'field': None,  # 表级差异无需字段
                'diff_type': '表缺少',
                'source_db': db_type_source,
                'target_db': db_type_target,
                'description': f"表:{table}仅存在于 {db_type_source}"
            })
            continue

            # 字段对比
        fields1 = normalized_dict1[table]
        fields2 = normalized_dict2[table]
        all_fields = set(fields1) | set(fields2)

        for field in all_fields:
            # 字段存在性检查
            if field not in fields1:
                #diff_report[table].append(f"字段缺失: {field} 字段仅存在于{db_type_target}数据库 {table}表")
                diff_report.append({  # 使用字典结构记录差异
                    'table': table,
                    'field': field,  # 表级差异无需字段
                    'diff_type': '字段缺失',
                    'source_db': db_type_source,
                    'target_db': db_type_target,
                    'description': f"字段:{field}仅存在于 {db_type_target}数据库的{table} "
                })
                continue
            if field not in fields2:
                #diff_report[table].append(f"字段缺失: {field} 字段仅存在于{db_type_source}数据库 {table}表")
                diff_report.append({  # 使用字典结构记录差异
                    'table': table,
                    'field': field,  # 表级差异无需字段
                    'diff_type': '字段缺失',
                    'source_db': db_type_source,
                    'target_db': db_type_target,
                    'description': f"字段:{field} 仅存在于 {db_type_source}数据库的{table} "
                })

                continue

            # 类型转换与对比
            orig_type = fields1[field]
            target_type = fields2[field]
            # 根据映射表判断类型是否兼容
            if orig_type in type_mapping:
                allowed_types = [t.upper() for t in type_mapping[orig_type]]
                if target_type  in allowed_types:
                    diff_report.append({  # 使用字典结构记录差异
                        'table': table,
                        'field': field,  # 表级差异无需字段
                        'diff_type': '类型兼容',
                        'source_db': db_type_source,
                        'target_db': db_type_target,
                        'description': f"数据库:{db_type_source} 字段:{field}({orig_type}) 兼容 数据库:{db_type_target} 字段:{field}({target_type})"
                    })
                else:
                    # 若未在映射表中定义,则严格比较类型
                    #if orig_type != target_type:
                    # if target_type not in allowed_types:
                       #diff_report[table].append(f"字段 {field} 类型不一致 Oracle {orig_type} vs MySQL({target_type})")
                       diff_report.append({  # 使用字典结构记录差异
                           'table': table,
                           'field': field,
                           'diff_type': '类型不兼容',
                           'source_db': db_type_source,
                           'target_db': db_type_target,
                           'description': f" 数据库:{db_type_source} 字段:{field}({orig_type}) 不兼容 数据库:{db_type_target} 字段:{field}({target_type})"
                       })

    data_to_insert = []
    #遍历列表结果
    for item in diff_report:
        field_name = item['field'] if item['field'] else None
        data_tuple = (
            item['table'],
            field_name,
            item['diff_type'],
            item['source_db'],
            item['target_db'],
            item['description'],
        )
        data_to_insert.append(data_tuple)
    return data_to_insert
