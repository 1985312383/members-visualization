# 合并仓库详情
import json
from pathlib import Path


# 获取十大知识分享组织信息
def get_top10_knowledge_sharing_organization_info(previous_data_path, current_data_path):
    """
    对比前后两个时期的十大知识分享组织信息

    Args:
        previous_data_path: 历史数据文件路径
        current_data_path: 当前数据文件路径

    Returns:
        包含对比信息的列表，如果历史数据不存在则返回当前数据
    """
    previous_data_path = Path(previous_data_path)
    current_data_path = Path(current_data_path)

    # 检查当前数据文件是否存在
    if not current_data_path.exists():
        print(f"❌ 当前数据文件不存在: {current_data_path}")
        return []

    try:
        with open(current_data_path, 'r', encoding='utf-8') as f:
            current_data_list = json.load(f)

        # 检查历史数据文件是否存在
        if not previous_data_path.exists():
            print(f"⚠️  历史数据文件不存在: {previous_data_path}")
            print("   首次运行或历史数据缺失，返回当前数据")
            # 为当前数据添加默认的对比字段
            for item in current_data_list:
                item['starAdd'] = 0
                item['rankAdd'] = 0
            print(f"✅ 成功获取 {len(current_data_list)} 个组织的数据")
            return current_data_list

        with open(previous_data_path, 'r', encoding='utf-8') as f:
            previous_data_list = json.load(f)

        diff_info = []
        for item in current_data_list:
            previous_item = next(
                (prev for prev in previous_data_list if prev['name'] == item['name']), None)
            if previous_item:
                diff_info.append({
                    **item,
                    'starAdd': item['star_count'] - previous_item['star_count'],
                    'rankAdd': item['rank'] - previous_item['rank'],
                })

        print(f"✅ 成功对比 {len(diff_info)} 个组织的数据")
        return diff_info
    except Exception as e:
        print(f"❌ 处理组织数据时出错: {e}")
        return []
