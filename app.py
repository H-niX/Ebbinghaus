#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版艾宾浩斯系统 - Web界面
"""

from flask import Flask, render_template, request, jsonify, send_file
from ebbinghaus import SimpleEbbinghausSystem
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'simple_ebbinghaus_2025'

# 全局系统实例
system = None
current_file = "vocabulary.xlsx"

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/guide')
def guide():
    """使用指南页面"""
    return render_template('guide.html')

@app.route('/api/init', methods=['POST'])
def api_init():
    """初始化系统"""
    global system, current_file
    try:
        data = request.get_json()
        filename = data.get('filename', 'vocabulary.xlsx')
        
        system = SimpleEbbinghausSystem(filename)
        current_file = filename
        
        return jsonify({'success': True, 'filename': filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/check_existing_learning', methods=['POST'])
def api_check_existing_learning():
    """检查指定日期是否已有学习记录"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        data = request.get_json()
        check_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        existing_records = system.get_existing_learning_records(check_date)
        
        return jsonify({
            'success': True, 
            'has_existing': len(existing_records) > 0,
            'existing_records': existing_records
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add_learning', methods=['POST'])
def api_add_learning():
    """添加学习记录"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        data = request.get_json()
        learn_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        learn_type = data.get('type', 'word')
        
        if learn_type != 'word':
            return jsonify({'success': False, 'error': '不支持的学习类型'})
        
        # 添加单词学习记录
        system.add_word_learning_session(learn_date)
        
        return jsonify({
            'success': True, 
            'message': f'已记录 {learn_date} 的单词学习'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/check_existing_reading', methods=['POST'])
def api_check_existing_reading():
    """检查指定日期是否已有阅读记录"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        data = request.get_json()
        check_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        existing_records = system.get_existing_reading_records(check_date)
        
        return jsonify({
            'success': True, 
            'has_existing': len(existing_records) > 0,
            'existing_records': existing_records
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/add_reading', methods=['POST'])
def api_add_reading():
    """添加阅读记录"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        data = request.get_json()
        read_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({'success': False, 'error': '阅读内容描述不能为空'})
        
        # 添加阅读记录
        result = system.add_reading_session(read_date, description)
        
        if result['success']:
            return jsonify({
                'success': True, 
                'message': result['message']
            })
        else:
            return jsonify({'success': False, 'error': result['message']})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/today_plan')
def api_today_plan():
    """获取今日复习计划"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        target_date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
        plan = system.get_today_plan(target_date)
        
        return jsonify({'success': True, 'plan': plan})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/monthly_calendar')
def api_monthly_calendar():
    """获取月历复习计划"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        # 获取年月参数，默认为当前月
        year = int(request.args.get('year', datetime.now().year))
        month = int(request.args.get('month', datetime.now().month))
        
        calendar_data = system.get_monthly_calendar(year, month)
        
        return jsonify({'success': True, 'calendar': calendar_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/weekly_overview')
def api_weekly_overview():
    """获取一周概览"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        overview = system.get_weekly_overview()
        
        return jsonify({'success': True, 'overview': overview})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/complete_review', methods=['POST'])
def api_complete_review():
    """完成复习"""
    global system
    try:
        if not system:
            system = SimpleEbbinghausSystem(current_file)
        
        data = request.get_json()
        review_date = data.get('review_date')
        original_date = data.get('original_date') 
        word_type = data.get('word_type')
        success = data.get('success', True)
        
        # 转换前端的中文类型到后端英文类型，但complete_review方法需要中文类型
        # 保持中文类型传递给complete_review方法
        backend_word_type = word_type
        if word_type == '新学单词':
            backend_word_type = '新学单词'  # 保持中文
        elif word_type == '标熟单词':
            backend_word_type = '标熟单词'  # 保持中文
        # 阅读类型已经是中文，直接传递
        
        system.complete_review(review_date, original_date, backend_word_type, success)
        
        return jsonify({
            'success': True, 
            'message': '复习记录已更新'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🌟 艾宾浩斯单词复习系统 - Web版本")
    print("🌐 访问地址: http://localhost:5000")
    print("💡 专为大量单词学习优化！")
    app.run(debug=True, host='127.0.0.1', port=5000)
