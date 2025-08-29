#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
艾宾浩斯遗忘曲线复习系统 - 核心算法
支持单词学习和阅读练习的复习计划管理
"""

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import os
from pathlib import Path
from typing import Dict, List, Optional

class SimpleEbbinghausSystem:
    """简化版艾宾浩斯复习系统"""
    
    def __init__(self, excel_path: str = "vocabulary.xlsx"):
        self.excel_path = excel_path
        
        # 复习间隔配置（天数）
        self.new_word_intervals = [0, 1, 2, 4, 7, 15, 30]  # 单词复习间隔（0=当天晚上复习）
        
        # 阅读复习间隔
        self.reading_intervals = {
            '段落': [0, 1, 3, 7],      # 段落阅读间隔（0=当天复习）
            '文章': [0, 2, 5, 10],     # 文章阅读间隔  
            '长篇': [0, 3, 7, 14]      # 长篇阅读间隔
        }
        
        # 加载或创建数据
        self.learning_records = self._load_or_create_data()
    
    def _load_or_create_data(self) -> pd.DataFrame:
        """加载或创建Excel数据"""
        try:
            if os.path.exists(self.excel_path):
                df = pd.read_excel(self.excel_path)
                print(f"✅ 从 {self.excel_path} 加载了 {len(df)} 条记录")
                
                # 确保duration列存在
                if 'duration' not in df.columns:
                    df['duration'] = 0
                
                # 转换日期列
                df['date'] = pd.to_datetime(df['date']).dt.date
                df['next_review_date'] = pd.to_datetime(df['next_review_date']).dt.date
                
                return df
            else:
                print(f"📝 创建新的数据文件: {self.excel_path}")
                return self._create_empty_dataframe()
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return self._create_empty_dataframe()
    
    def _create_empty_dataframe(self) -> pd.DataFrame:
        """创建空的DataFrame"""
        columns = [
            'date',             # 学习日期
            'word_count',       # 单词数量或阅读数量
            'word_type',        # 单词类型: new/段落/文章/长篇
            'stage',            # 复习阶段
            'next_review_date', # 下次复习日期
            'status',           # 状态: pending/completed/mastered
            'duration'          # 阅读时长（仅阅读记录使用）
        ]
        
        return pd.DataFrame(columns=columns)
    
    def _save_data(self, df: pd.DataFrame):
        """保存数据到Excel"""
        try:
            # 创建目录
            Path(self.excel_path).parent.mkdir(parents=True, exist_ok=True)
            
            # 保存到Excel
            df.to_excel(self.excel_path, index=False)
            print(f"💾 数据已保存到 {self.excel_path}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")
    
    def add_learning_session(self, learn_date: str, new_word_count: int):
        """
        添加学习会话
        
        Args:
            learn_date: 学习日期 (YYYY-MM-DD)
            new_word_count: 新学单词数量
        """
        learn_date_obj = datetime.strptime(learn_date, '%Y-%m-%d').date()
        
        new_records = []
        
        # 添加新学单词记录
        if new_word_count > 0:
            new_records.append({
                'date': learn_date_obj,
                'word_count': new_word_count,
                'word_type': 'new',
                'stage': 0,
                'next_review_date': learn_date_obj + timedelta(days=self.new_word_intervals[0]),
                'status': 'pending',
                'duration': 0
            })

        if new_records:
            new_df = pd.DataFrame(new_records)
            self.learning_records = pd.concat([self.learning_records, new_df], ignore_index=True)
            self._save_data(self.learning_records)

        # 输出结果信息
        print(f"✅ 已记录 {learn_date} 的学习:")
        if new_word_count > 0:
            print(f"   📚 学习单词: {new_word_count} 个")
    
    
    def get_existing_learning_records(self, check_date: str) -> list:
        """
        获取指定日期的现有学习记录
        
        Args:
            check_date: 检查日期 (YYYY-MM-DD)
            
        Returns:
            list: 现有学习记录列表
        """
        check_date_obj = datetime.strptime(check_date, '%Y-%m-%d').date()
        
        # 查找该日期的学习记录
        existing_records = self.learning_records[
            (self.learning_records['date'] == check_date_obj) &
            (self.learning_records['word_type'] == 'new')
        ]
        
        records = []
        if not existing_records.empty:
            for _, record in existing_records.iterrows():
                records.append({
                    'word_type': '单词',
                    'word_count': int(record['word_count']),
                    'stage': int(record['stage']),
                    'status': record['status']
                })
        
        return records
    
    
    def add_word_learning_session(self, learn_date: str):
        """
        添加单词学习会话（简化版）
        
        Args:
            learn_date: 学习日期 (YYYY-MM-DD)
        """
        learn_date_obj = datetime.strptime(learn_date, '%Y-%m-%d').date()
        
        # 创建单词学习记录
        new_record = {
            'date': learn_date_obj,
            'word_count': 1,  # 简化为1个单位
            'word_type': 'new',  # 统一为单词类型
            'stage': 0,
            'next_review_date': learn_date_obj + timedelta(days=self.new_word_intervals[0]),
            'status': 'pending',
            'duration': 0
        }
        
        new_df = pd.DataFrame([new_record])
        self.learning_records = pd.concat([self.learning_records, new_df], ignore_index=True)
        self._save_data(self.learning_records)
        
        print(f"📚 已记录 {learn_date} 的单词学习")
    
    def add_reading_session(self, read_date: str, description: str):
        """
        添加阅读会话（简化版）
        
        Args:
            read_date: 阅读日期 (YYYY-MM-DD)
            description: 阅读内容描述（如"2001_text1_一二段"）
        """
        read_date_obj = datetime.strptime(read_date, '%Y-%m-%d').date()
        
        # 创建阅读记录，使用默认复习间隔
        default_intervals = [1, 3, 7]  # 默认阅读复习间隔
        
        new_record = {
            'date': read_date_obj,
            'word_count': 1,  # 简化为1个单位
            'word_type': 'reading',  # 统一类型
            'description': description,  # 存储描述信息
            'stage': 0,
            'next_review_date': read_date_obj + timedelta(days=default_intervals[0]),
            'status': 'pending',
            'duration': 0
        }
        
        new_df = pd.DataFrame([new_record])
        self.learning_records = pd.concat([self.learning_records, new_df], ignore_index=True)
        self._save_data(self.learning_records)
        
        message = f'已记录 {read_date} 的阅读: {description}'
        print(f"📖 {message}")
        
        return {'success': True, 'message': message}
    
    def get_existing_reading_records(self, check_date: str) -> list:
        """
        获取指定日期的现有阅读记录
        
        Args:
            check_date: 检查日期 (YYYY-MM-DD)
            
        Returns:
            list: 现有阅读记录列表
        """
        check_date_obj = datetime.strptime(check_date, '%Y-%m-%d').date()
        
        # 查找该日期的阅读记录
        existing_records = self.learning_records[
            (self.learning_records['date'] == check_date_obj) &
            (self.learning_records['word_type'].isin(['段落', '文章', '长篇']))
        ]
        
        records = []
        if not existing_records.empty:
            for _, record in existing_records.iterrows():
                unit = "段" if record['word_type'] == "段落" else "篇"
                records.append({
                    'reading_type': record['word_type'],
                    'count': int(record['word_count']),
                    'stage': int(record['stage']),
                    'status': record['status']
                })
        
        return records
        
    def add_reading_session_with_merge(self, read_date: str, reading_type: str, 
                                     count: int, merge_strategy: str = 'add') -> dict:
        """
        添加阅读会话，支持同日记录合并策略
        
        Args:
            read_date: 阅读日期 (YYYY-MM-DD)
            reading_type: 阅读类型 ('段落', '文章', '长篇')
            count: 阅读数量（段落数/文章数/长文数）
            merge_strategy: 合并策略 ('add'=累加, 'replace'=替换, 'cancel'=取消)
            
        Returns:
            dict: 操作结果 {'success': bool, 'message': str}
        """
        read_date_obj = datetime.strptime(read_date, '%Y-%m-%d').date()
        
        # 检查是否已有同日同类型记录
        existing_records = self.learning_records[
            (self.learning_records['date'] == read_date_obj) &
            (self.learning_records['word_type'] == reading_type)
        ]
        
        if merge_strategy == 'cancel':
            return {'success': False, 'message': '操作已取消'}
        
        # 如果选择替换，先删除现有记录
        if merge_strategy == 'replace' and not existing_records.empty:
            self.learning_records = self.learning_records[
                ~((self.learning_records['date'] == read_date_obj) &
                  (self.learning_records['word_type'] == reading_type))
            ]
            print(f"🗑️ 已删除 {read_date} 的现有{reading_type}记录")
        
        # 处理累加策略
        if merge_strategy == 'add' and not existing_records.empty:
            # 累加到现有记录
            idx = existing_records.index[0]
            old_count = int(self.learning_records.loc[idx, 'word_count'])
            self.learning_records.loc[idx, 'word_count'] = old_count + count
            unit = "段" if reading_type == "段落" else "篇"
            print(f"📖 {reading_type}阅读已累加: +{count} {unit} (总计{old_count + count}{unit})")
            
            # 保存数据
            self._save_data(self.learning_records)
            
            return {
                'success': True, 
                'message': f'已累加 {read_date} 的{reading_type}阅读: +{count}{unit} (总计{old_count + count}{unit})'
            }
        
        # 添加新的阅读记录
        new_record = {
            'date': read_date_obj,
            'word_count': count,  # 使用word_count存储阅读数量
            'word_type': reading_type,
            'stage': 0,
            'next_review_date': read_date_obj + timedelta(days=self.reading_intervals[reading_type][0]),
            'status': 'pending',
            'duration': 0  # 不再使用duration字段
        }
        
        new_df = pd.DataFrame([new_record])
        self.learning_records = pd.concat([self.learning_records, new_df], ignore_index=True)
        
        # 保存数据
        self._save_data(self.learning_records)
        
        # 生成结果消息
        strategy_text = {
            'add': '(新增模式)' if not existing_records.empty else '',
            'replace': '(替换模式)'
        }.get(merge_strategy, '')
        
        unit = "段" if reading_type == "段落" else "篇"
        message = f'已记录 {read_date} 的{reading_type}阅读{strategy_text}: {count}{unit}'
        
        return {'success': True, 'message': message}
    
    def get_today_plan(self, target_date: str = None) -> Dict:
        """获取指定日期的复习计划（简化版）"""
        if target_date is None:
            target_date = datetime.now().strftime('%Y-%m-%d')
        
        target_date_obj = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        # 查找需要复习的记录
        due_records = self.learning_records[
            (self.learning_records['next_review_date'] == target_date_obj) &
            (self.learning_records['status'] == 'pending')
        ]
        
        plan = {
            'date': target_date,
            'date_display': self._get_relative_date(target_date_obj),
            'reviews': []
        }
        
        # 使用字典来合并同类型的复习项目
        review_groups = {}
        
        for _, record in due_records.iterrows():
            if record['word_type'] == 'new':
                # 处理单词记录
                merge_key = '单词'
                
                if merge_key not in review_groups:
                    review_groups[merge_key] = {
                        'word_count': 0,
                        'word_type': '单词'
                    }
                
                # 累加单词数量
                review_groups[merge_key]['word_count'] += int(record['word_count'])
                
            else:
                # 处理阅读记录
                reading_type = record['word_type']
                unit = "段" if reading_type == "段落" else "篇"
                
                # 合并同类型阅读记录
                merge_key = f"{reading_type}阅读"
                
                if merge_key not in review_groups:
                    review_groups[merge_key] = {
                        'word_count': 0,
                        'reading_type': merge_key,
                        'unit': unit,
                        'item_type': 'reading'
                    }
                
                review_groups[merge_key]['word_count'] += int(record.get('word_count', 0))
        
        # 将合并后的复习项目添加到计划中
        for review_item in review_groups.values():
            plan['reviews'].append(review_item)
            
        return plan
    
    def _get_relative_date(self, target_date: date) -> str:
        """获取相对时间显示"""
        today = datetime.now().date()
        diff = (target_date - today).days
        
        if diff == 0:
            return "今天"
        elif diff == -1:
            return "昨天"
        elif diff == -2:
            return "前天"
        else:
            return target_date.strftime('%m月%d日')
    
    def get_weekly_overview(self) -> Dict:
        """获取一周概览"""
        today = datetime.now().date()
        
        # 查看未来7天的复习计划
        week_plan = {}
        for i in range(7):
            check_date = today + timedelta(days=i)
            date_str = check_date.strftime('%Y-%m-%d')
            
            due_records = self.learning_records[
                (self.learning_records['next_review_date'] == check_date) &
                (self.learning_records['status'] == 'pending')
            ]
            
            if not due_records.empty:
                new_word_reviews = len(due_records[due_records['word_type'] == 'new'])
                familiar_word_reviews = len(due_records[due_records['word_type'] == 'marked_familiar'])
                reading_reviews = len(due_records[due_records['word_type'].isin(['段落', '文章', '长篇'])])
                
                total_reviews = len(due_records)
                
                week_plan[date_str] = {
                    'display': self._get_relative_date(check_date),
                    'total_reviews': total_reviews,
                    'new_word_reviews': new_word_reviews,
                    'familiar_word_reviews': familiar_word_reviews,
                    'reading_reviews': reading_reviews
                }
        
        return week_plan
    
    def get_monthly_calendar(self, year: int, month: int) -> Dict:
        """获取月历复习计划"""
        import calendar
        
        # 生成月历结构
        cal = calendar.Calendar(firstweekday=0)  # 周一为第一天
        month_days = cal.monthdayscalendar(year, month)
        
        # 获取该月所有复习计划
        month_start = datetime(year, month, 1).date()
        if month == 12:
            month_end = datetime(year + 1, 1, 1).date() - timedelta(days=1)
        else:
            month_end = datetime(year, month + 1, 1).date() - timedelta(days=1)
            
        # 查找该月范围内的复习计划
        month_reviews = self.learning_records[
            (self.learning_records['next_review_date'] >= month_start) &
            (self.learning_records['next_review_date'] <= month_end) &
            (self.learning_records['status'] == 'pending')
        ]
        
        # 按日期分组复习任务
        daily_reviews = {}
        for _, record in month_reviews.iterrows():
            review_date = record['next_review_date']
            day = review_date.day
            
            if day not in daily_reviews:
                daily_reviews[day] = {
                    'total': 0,
                    'items': []
                }
            
            daily_reviews[day]['total'] += 1
            
            # 根据记录类型添加详细信息
            if record['word_type'] == 'word':
                # 单词学习：显示原始学习日期
                original_date = record['date'].strftime('%m.%d')
                daily_reviews[day]['items'].append(f"单词{original_date}")
            elif hasattr(record, 'description') and record.get('description'):
                # 阅读记录：显示具体内容描述
                daily_reviews[day]['items'].append(f"阅读{record['description']}")
            else:
                # 兼容旧数据格式
                if record['word_type'] == 'new':
                    original_date = record['date'].strftime('%m.%d')
                    daily_reviews[day]['items'].append(f"单词{original_date}")
                elif record['word_type'] == 'marked_familiar':
                    original_date = record['date'].strftime('%m.%d')
                    daily_reviews[day]['items'].append(f"单词{original_date}")
                elif record['word_type'] in ['段落', '文章', '长篇']:
                    daily_reviews[day]['items'].append(f"阅读{record['word_type']}")
        
        return {
            'year': year,
            'month': month,
            'month_name': f"{year}年{month}月",
            'weeks': month_days,
            'daily_reviews': daily_reviews,
            'weekday_names': ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        }
    
    def complete_review(self, review_date: str, original_date: str, word_type: str, success: bool):
        """完成复习并更新计划"""
        review_date_obj = datetime.strptime(review_date, '%Y-%m-%d').date()
        original_date_obj = datetime.strptime(original_date, '%Y-%m-%d').date()
        
        # 查找要更新的记录
        if word_type == '单词':
            # 处理单词记录
            mask = (
                (self.learning_records['date'] == original_date_obj) &
                (self.learning_records['word_type'] == 'new') &
                (self.learning_records['next_review_date'] == review_date_obj)
            )
        else:
            # 处理阅读记录
            reading_type = word_type.replace('阅读', '')
            mask = (
                (self.learning_records['date'] == original_date_obj) &
                (self.learning_records['word_type'] == reading_type) &
                (self.learning_records['next_review_date'] == review_date_obj)
            )
        
        matching_records = self.learning_records[mask]
        
        if matching_records.empty:
            print(f"⚠️ 未找到匹配的复习记录")
            return
        
        for idx in matching_records.index:
            current_stage = self.learning_records.loc[idx, 'stage']
            
            if success:
                # 复习成功，进入下一阶段
                new_stage = current_stage + 1
                
                # 获取适当的间隔数组
                if word_type == '单词':
                    intervals = self.new_word_intervals
                else:
                    reading_type = word_type.replace('阅读', '')
                    intervals = self.reading_intervals.get(reading_type, [1, 3, 7])
                
                if new_stage < len(intervals):
                    # 还有下一个复习阶段
                    next_review = review_date_obj + timedelta(days=intervals[new_stage])
                    self.learning_records.loc[idx, 'stage'] = new_stage
                    self.learning_records.loc[idx, 'next_review_date'] = next_review
                    self.learning_records.loc[idx, 'status'] = 'pending'
                else:
                    # 已完成所有复习阶段
                    self.learning_records.loc[idx, 'status'] = 'mastered'
                    print(f"🎉 {word_type} 已完全掌握！")
            else:
                # 复习失败，重新开始
                intervals = self.new_word_intervals if word_type == '单词' else self.reading_intervals.get(word_type.replace('阅读', ''), [1, 3, 7])
                
                self.learning_records.loc[idx, 'stage'] = 0
                self.learning_records.loc[idx, 'next_review_date'] = review_date_obj + timedelta(days=intervals[0])
                self.learning_records.loc[idx, 'status'] = 'pending'
                print(f"🔄 {word_type} 需要重新复习")
        
        self._save_data(self.learning_records)
        print(f"✅ 复习记录已更新")

def main():
    """命令行演示"""
    print("🌟 艾宾浩斯单词复习系统")
    print("📌 建议使用Web界面: python app.py")
    print("🌐 Web访问地址: http://127.0.0.1:5000")
    print()
    
    system = SimpleEbbinghausSystem()
    
    while True:
        print("\n" + "="*50)
        print("请选择操作:")
        print("1. 记录单词学习")
        print("2. 记录阅读练习")
        print("3. 查看今日复习计划")
        print("4. 查看一周概览")
        print("0. 退出")
        print("="*50)
        
        choice = input("请输入选择 (0-4): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            date_str = input("学习日期 (YYYY-MM-DD, 回车默认今天): ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            # 只需要确认是否学习了单词
            learn_words = input("今天学习了单词吗？(y/n): ").strip().lower()
            
            if learn_words in ['y', 'yes', '是', '1']:
                system.add_word_learning_session(date_str)
        elif choice == '2':
            date_str = input("阅读日期 (YYYY-MM-DD, 回车默认今天): ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            print("阅读类型: 1-段落 2-文章 3-长篇")
            type_choice = input("选择类型: ").strip()
            type_map = {'1': '段落', '2': '文章', '3': '长篇'}
            reading_type = type_map.get(type_choice, '段落')
            
            count = int(input(f"阅读数量({"段" if reading_type=="段落" else "篇"}): ").strip() or 0)
            
            if count > 0:
                result = system.add_reading_session(date_str, reading_type, count)
                print(result['message'])
        elif choice == '3':
            date_str = input("查看日期 (YYYY-MM-DD, 回车默认今天): ").strip()
            if not date_str:
                date_str = datetime.now().strftime('%Y-%m-%d')
            
            plan = system.get_today_plan(date_str)
            print(f"\n📅 {plan['date_display']} ({plan['date']}) 的复习计划:")
            
            if not plan['reviews']:
                print("🎉 今天没有复习任务！")
            else:
                for i, review in enumerate(plan['reviews'], 1):
                    if 'word_type' in review:
                        print(f"   {i}. {review['word_type']} {review['word_count']}个")
                        print(f"      来源: {review['original_date_display']} | 第{review['stage']}次复习")
                    else:
                        unit = review.get('unit', '个')
                        print(f"   {i}. {review['reading_type']} {review['word_count']}{unit}")
                        print(f"      来源: {review['original_date_display']} | 第{review['stage']}次复习")
        elif choice == '4':
            overview = system.get_weekly_overview()
            print("\n📊 未来一周复习概览:")
            
            if not overview:
                print("未来一周无复习任务")
            else:
                for date_str, info in overview.items():
                    print(f"   {info['display']} ({date_str}): {info['total_reviews']}项任务")
                    details = []
                    if info['new_word_reviews'] > 0:
                        details.append(f"新学{info['new_word_reviews']}")
                    if info['familiar_word_reviews'] > 0:
                        details.append(f"标熟{info['familiar_word_reviews']}")
                    if info['reading_reviews'] > 0:
                        details.append(f"阅读{info['reading_reviews']}")
                    if details:
                        print(f"      ({', '.join(details)})")

if __name__ == "__main__":
    main()
