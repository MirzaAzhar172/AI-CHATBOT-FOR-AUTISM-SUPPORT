import streamlit as st
import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
import re
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# LANGUAGE TRANSLATIONS - COMPLETE
TRANSLATIONS = {
    'en': {
        'app_title': 'PrismCHAT',
        'app_subtitle': 'Virtual Counsellor Intelligent v1.0',
        'new_chat': 'New Chat',
        'chat_history': 'Chat History',
        'no_history': 'No chat history yet',
        'quick_help': 'Quick Help',
        'early_signs': 'Early Signs of Autism',
        'managing_meltdowns': 'Managing Meltdowns',
        'support_parents': 'Support for Parents',
        'behavior_tracker': 'Behavior Tracker',
        'settings': 'Settings',
        'session_insight': 'Session Insight',
        'emotional_state': 'Emotional State:',
        'calm': 'Calm',
        'neutral': 'Neutral',
        'distressed': 'Distressed',
        'overall': 'Overall',
        'messages': 'messages',
        'dark_mode': 'Dark Mode',
        'light_mode': 'Light Mode',
        'copyright': '© 2025 PrismCHAT',
        'developed_by': 'Developed by',
        'main_heading': 'How can we support you?',
        'main_subheading': 'Your expert companion for autism support.',
        'chat_title': 'PrismChat Support',
        'input_placeholder': 'Ask me anything...',
        'thinking': 'Thinking...',
        'api_error': 'API Error.',
        'connection_failed': 'Connection failed.',
        'language': 'Language',
        'system_prompt': 'You are PrismChat, a professional, empathetic, and clear-speaking autism counsellor. Give structured and sensory-friendly advice.',
        'early_signs_q': 'What are the common early signs of autism?',
        'meltdowns_q': 'How do I handle an autistic meltdown effectively?',
        'parents_q': 'What emotional support is available for parents?',
        # Additional UI elements
        'add_event': 'Add Event',
        'view_analytics': 'View Analytics',
        'event_logged': 'Event logged',
        'please_add_notes': 'Please add notes',
        'no_history_yet': 'No history yet',
        'back': 'Back',
        'appearance': 'Appearance',
        'user_profile': 'User Profile',
        'emergency': 'Emergency',
        'family': 'Family',
        'theme': 'Theme',
        'current_theme': 'Current Theme',
        'switch_to_light': 'Switch to Light Mode',
        'switch_to_dark': 'Switch to Dark Mode',
        'dark_reduces_strain': 'Dark mode reduces eye strain in low-light environments.',
        'light_better_visibility': 'Light mode provides better visibility in bright conditions.',
        'select_language': 'Select Language:',
        'language_updated': 'Language updated',
        'child_information': 'Child Information',
        'child_name': "Child's Name",
        'age': 'Age',
        'diagnosis': 'Diagnosis',
        'profile_benefits': 'Profile Benefits',
        'personalized_advice': 'Personalized advice',
        'age_appropriate': 'Age-appropriate tips',
        'context_aware': 'Context-aware support',
        'better_recommendations': 'Better recommendations',
        'additional_details': 'Additional Details',
        'known_triggers': 'Known Triggers',
        'communication_style': 'Communication Style',
        'interests_strengths': 'Interests & Strengths',
        'sensory_needs': 'Sensory Needs',
        'additional_notes': 'Additional Notes',
        'save_profile': 'Save Profile',
        'profile_saved': 'Profile saved for',
        'enter_child_name': 'Please enter child\'s name',
        'emergency_contacts': 'Emergency Contacts',
        'crisis_hotlines_my': 'Crisis Hotlines (Malaysia)',
        'emotional_support_247': '24/7 Emotional support',
        'professional_counseling': 'Professional counseling',
        'women_children_protection': 'Women & children protection',
        'autism_support_centers': 'Autism Support Centers',
        'nasom': 'National Autism Society of Malaysia',
        'early_intervention': 'Early intervention & therapy',
        'emergency_guidelines': 'Emergency Response Guidelines',
        'during_crisis': 'During a Crisis:',
        'stay_calm': 'Stay calm, speak softly',
        'remove_triggers': 'Remove triggers if possible',
        'give_space': 'Give space and time',
        'use_visual_supports': 'Use visual supports',
        'avoid_restraint': 'Avoid physical restraint',
        'when_seek_help': 'When to Seek Help:',
        'risk_of_harm': 'Risk of harm',
        'prolonged_distress': 'Prolonged distress (30+ min)',
        'medical_emergency': 'Medical emergency',
        'caregiver_overwhelmed': 'Caregiver overwhelmed',
        'add_personal_contact': 'Add Personal Contact',
        'name': 'Name',
        'phone': 'Phone',
        'notes': 'Notes',
        'save_contact': 'Save Contact',
        'contact_saved': 'Contact saved:',
        'fill_name_number': 'Please fill in name and number',
        'family_members': 'Family Members',
        'active': 'Active',
        'switch': 'Switch',
        'delete': 'Delete',
        'switched_to': 'Switched to',
        'member_removed': 'Member removed',
        'add_family_member': 'Add Family Member',
        'role': 'Role',
        'add_member': 'Add Member',
        'added': 'Added',
        'enter_name': 'Please enter a name',
        'event': 'Event:',
        'intensity': 'Intensity:',
        'one_per_line': 'One per line, e.g.:\nLoud noises\nCrowds',
        'placeholder_interests': 'e.g., Loves trains, Good at puzzles',
        'placeholder_sensory': 'e.g., Needs quiet space, Prefers dim lighting',
        'placeholder_notes': 'Any other important information...',
        'placeholder_contact_name': 'e.g., Dr. Sarah',
        'placeholder_contact_phone': 'e.g., 012-3456789',
        'placeholder_contact_notes': 'e.g., Family therapist, available weekdays',
        'placeholder_member_name': 'e.g., Sarah',
        'placeholder_child_name': 'e.g., Ahmad',
        'placeholder_age': 'e.g., 5 years old',
        'placeholder_diagnosis': 'e.g., ASD Level 2, ADHD',
        'placeholder_event_notes': 'What happened?',
        'english': 'English',
        'bahasa_melayu': 'Bahasa Melayu',
        'chinese': '中文'
    },
    'ms': {
        'app_title': 'PrismCHAT',
        'app_subtitle': 'Kaunselor Virtual Pintar v1.0',
        'new_chat': 'Sembang Baru',
        'chat_history': 'Sejarah Sembang',
        'no_history': 'Tiada sejarah sembang lagi',
        'quick_help': 'Bantuan Pantas',
        'early_signs': 'Tanda Awal Autisme',
        'managing_meltdowns': 'Menguruskan Kemarahan',
        'support_parents': 'Sokongan Ibu Bapa',
        'behavior_tracker': 'Penjejak Tingkah Laku',
        'settings': 'Tetapan',
        'session_insight': 'Ringkasan Sesi',
        'emotional_state': 'Keadaan Emosi:',
        'calm': 'Tenang',
        'neutral': 'Neutral',
        'distressed': 'Tertekan',
        'overall': 'Keseluruhan',
        'messages': 'mesej',
        'dark_mode': 'Mod Gelap',
        'light_mode': 'Mod Terang',
        'copyright': '© 2025 PrismCHAT',
        'developed_by': 'Dibangunkan oleh',
        'main_heading': 'Bagaimana kami boleh bantu anda?',
        'main_subheading': 'Rakan pakar anda untuk sokongan autisme.',
        'chat_title': 'Sokongan PrismChat',
        'input_placeholder': 'Tanya apa sahaja...',
        'thinking': 'Berfikir...',
        'api_error': 'Ralat API.',
        'connection_failed': 'Sambungan gagal.',
        'language': 'Bahasa',
        'system_prompt': 'Anda adalah PrismChat, kaunselor autisme yang profesional, empati, dan jelas. Berikan nasihat berstruktur dan mesra deria.',
        'early_signs_q': 'Apakah tanda-tanda awal autisme yang biasa?',
        'meltdowns_q': 'Bagaimana saya menangani kemarahan autistik dengan berkesan?',
        'parents_q': 'Apakah sokongan emosi yang ada untuk ibu bapa?',
        # Additional UI elements
        'add_event': 'Tambah Peristiwa',
        'view_analytics': 'Lihat Analisis',
        'event_logged': 'Peristiwa direkod',
        'please_add_notes': 'Sila tambah nota',
        'no_history_yet': 'Tiada sejarah lagi',
        'back': 'Kembali',
        'appearance': 'Penampilan',
        'user_profile': 'Profil Pengguna',
        'emergency': 'Kecemasan',
        'family': 'Keluarga',
        'theme': 'Tema',
        'current_theme': 'Tema Semasa',
        'switch_to_light': 'Tukar ke Mod Terang',
        'switch_to_dark': 'Tukar ke Mod Gelap',
        'dark_reduces_strain': 'Mod gelap mengurangkan tekanan mata dalam persekitaran cahaya rendah.',
        'light_better_visibility': 'Mod terang memberikan keterlihatan lebih baik dalam keadaan terang.',
        'select_language': 'Pilih Bahasa:',
        'language_updated': 'Bahasa dikemaskini',
        'child_information': 'Maklumat Kanak-kanak',
        'child_name': 'Nama Kanak-kanak',
        'age': 'Umur',
        'diagnosis': 'Diagnosis',
        'profile_benefits': 'Faedah Profil',
        'personalized_advice': 'Nasihat diperibadikan',
        'age_appropriate': 'Petua sesuai umur',
        'context_aware': 'Sokongan sedar konteks',
        'better_recommendations': 'Cadangan lebih baik',
        'additional_details': 'Butiran Tambahan',
        'known_triggers': 'Pencetus Diketahui',
        'communication_style': 'Gaya Komunikasi',
        'interests_strengths': 'Minat & Kekuatan',
        'sensory_needs': 'Keperluan Deria',
        'additional_notes': 'Nota Tambahan',
        'save_profile': 'Simpan Profil',
        'profile_saved': 'Profil disimpan untuk',
        'enter_child_name': 'Sila masukkan nama kanak-kanak',
        'emergency_contacts': 'Hubungan Kecemasan',
        'crisis_hotlines_my': 'Talian Krisis (Malaysia)',
        'emotional_support_247': 'Sokongan emosi 24/7',
        'professional_counseling': 'Kaunseling profesional',
        'women_children_protection': 'Perlindungan wanita & kanak-kanak',
        'autism_support_centers': 'Pusat Sokongan Autisme',
        'nasom': 'Persatuan Autisme Kebangsaan Malaysia',
        'early_intervention': 'Intervensi awal & terapi',
        'emergency_guidelines': 'Garis Panduan Tindakan Kecemasan',
        'during_crisis': 'Semasa Krisis:',
        'stay_calm': 'Kekal tenang, bercakap perlahan',
        'remove_triggers': 'Buang pencetus jika boleh',
        'give_space': 'Beri ruang dan masa',
        'use_visual_supports': 'Guna sokongan visual',
        'avoid_restraint': 'Elak kekangan fizikal',
        'when_seek_help': 'Bila Perlu Bantuan:',
        'risk_of_harm': 'Risiko bahaya',
        'prolonged_distress': 'Kesusahan berpanjangan (30+ min)',
        'medical_emergency': 'Kecemasan perubatan',
        'caregiver_overwhelmed': 'Penjaga terharu',
        'add_personal_contact': 'Tambah Hubungan Peribadi',
        'name': 'Nama',
        'phone': 'Telefon',
        'notes': 'Nota',
        'save_contact': 'Simpan Hubungan',
        'contact_saved': 'Hubungan disimpan:',
        'fill_name_number': 'Sila isi nama dan nombor',
        'family_members': 'Ahli Keluarga',
        'active': 'Aktif',
        'switch': 'Tukar',
        'delete': 'Padam',
        'switched_to': 'Ditukar kepada',
        'member_removed': 'Ahli dikeluarkan',
        'add_family_member': 'Tambah Ahli Keluarga',
        'role': 'Peranan',
        'add_member': 'Tambah Ahli',
        'added': 'Ditambah',
        'enter_name': 'Sila masukkan nama',
        'event': 'Peristiwa:',
        'intensity': 'Intensiti:',
        'one_per_line': 'Satu setiap baris, cth:\nBunyi kuat\nOrang ramai',
        'placeholder_interests': 'cth: Suka kereta api, Pandai puzzle',
        'placeholder_sensory': 'cth: Perlukan ruang senyap, Suka cahaya malap',
        'placeholder_notes': 'Maklumat penting lain...',
        'placeholder_contact_name': 'cth: Dr. Sarah',
        'placeholder_contact_phone': 'cth: 012-3456789',
        'placeholder_contact_notes': 'cth: Ahli terapi keluarga, ada pada hari kerja',
        'placeholder_member_name': 'cth: Sarah',
        'placeholder_child_name': 'cth: Ahmad',
        'placeholder_age': 'cth: 5 tahun',
        'placeholder_diagnosis': 'cth: ASD Tahap 2, ADHD',
        'placeholder_event_notes': 'Apa yang berlaku?',
        'english': 'English',
        'bahasa_melayu': 'Bahasa Melayu',
        'chinese': '中文'
    },
    'zh': {
        'app_title': 'PrismCHAT',
        'app_subtitle': '虚拟智能顾问 v1.0',
        'new_chat': '新对话',
        'chat_history': '对话历史',
        'no_history': '暂无对话历史',
        'quick_help': '快速帮助',
        'early_signs': '自闭症早期迹象',
        'managing_meltdowns': '应对情绪崩溃',
        'support_parents': '家长支持',
        'behavior_tracker': '行为追踪',
        'settings': '设置',
        'session_insight': '会话分析',
        'emotional_state': '情绪状态：',
        'calm': '平静',
        'neutral': '中性',
        'distressed': '焦虑',
        'overall': '总体',
        'messages': '条消息',
        'dark_mode': '深色模式',
        'light_mode': '浅色模式',
        'copyright': '© 2025 PrismCHAT',
        'developed_by': '开发者',
        'main_heading': '我们如何帮助您？',
        'main_subheading': '您的自闭症支持专家伙伴。',
        'chat_title': 'PrismChat 支持',
        'input_placeholder': '问我任何问题...',
        'thinking': '思考中...',
        'api_error': 'API 错误。',
        'connection_failed': '连接失败。',
        'language': '语言',
        'system_prompt': '你是PrismChat，一位专业、富有同理心且表达清晰的自闭症辅导员。请提供结构化且感官友好的建议。',
        'early_signs_q': '自闭症的常见早期迹象是什么？',
        'meltdowns_q': '如何有效应对自闭症情绪崩溃？',
        'parents_q': '有哪些情感支持可供家长使用？',
        # Additional UI elements
        'add_event': '添加事件',
        'view_analytics': '查看分析',
        'event_logged': '事件已记录',
        'please_add_notes': '请添加备注',
        'no_history_yet': '暂无历史',
        'back': '返回',
        'appearance': '外观',
        'user_profile': '用户资料',
        'emergency': '紧急情况',
        'family': '家庭',
        'theme': '主题',
        'current_theme': '当前主题',
        'switch_to_light': '切换到浅色模式',
        'switch_to_dark': '切换到深色模式',
        'dark_reduces_strain': '深色模式在低光环境下减少眼睛疲劳。',
        'light_better_visibility': '浅色模式在明亮条件下提供更好的可见性。',
        'select_language': '选择语言：',
        'language_updated': '语言已更新',
        'child_information': '儿童信息',
        'child_name': '儿童姓名',
        'age': '年龄',
        'diagnosis': '诊断',
        'profile_benefits': '资料优势',
        'personalized_advice': '个性化建议',
        'age_appropriate': '适龄提示',
        'context_aware': '情境感知支持',
        'better_recommendations': '更好的建议',
        'additional_details': '附加详情',
        'known_triggers': '已知触发因素',
        'communication_style': '沟通方式',
        'interests_strengths': '兴趣与优势',
        'sensory_needs': '感官需求',
        'additional_notes': '附加备注',
        'save_profile': '保存资料',
        'profile_saved': '资料已保存：',
        'enter_child_name': '请输入儿童姓名',
        'emergency_contacts': '紧急联系',
        'crisis_hotlines_my': '危机热线（马来西亚）',
        'emotional_support_247': '24/7情感支持',
        'professional_counseling': '专业咨询',
        'women_children_protection': '妇女儿童保护',
        'autism_support_centers': '自闭症支持中心',
        'nasom': '马来西亚国家自闭症协会',
        'early_intervention': '早期干预与治疗',
        'emergency_guidelines': '紧急应对指南',
        'during_crisis': '危机期间：',
        'stay_calm': '保持冷静，轻声说话',
        'remove_triggers': '如可能，移除触发因素',
        'give_space': '给予空间和时间',
        'use_visual_supports': '使用视觉支持',
        'avoid_restraint': '避免身体约束',
        'when_seek_help': '何时寻求帮助：',
        'risk_of_harm': '有伤害风险',
        'prolonged_distress': '持续痛苦（30分钟以上）',
        'medical_emergency': '医疗紧急情况',
        'caregiver_overwhelmed': '护理者不堪重负',
        'add_personal_contact': '添加个人联系人',
        'name': '姓名',
        'phone': '电话',
        'notes': '备注',
        'save_contact': '保存联系人',
        'contact_saved': '联系人已保存：',
        'fill_name_number': '请填写姓名和号码',
        'family_members': '家庭成员',
        'active': '活跃',
        'switch': '切换',
        'delete': '删除',
        'switched_to': '已切换到',
        'member_removed': '成员已移除',
        'add_family_member': '添加家庭成员',
        'role': '角色',
        'add_member': '添加成员',
        'added': '已添加',
        'enter_name': '请输入姓名',
        'event': '事件：',
        'intensity': '强度：',
        'one_per_line': '每行一个，例如：\n大声噪音\n人群',
        'placeholder_interests': '例如：喜欢火车，擅长拼图',
        'placeholder_sensory': '例如：需要安静空间，偏好昏暗灯光',
        'placeholder_notes': '任何其他重要信息...',
        'placeholder_contact_name': '例如：李医生',
        'placeholder_contact_phone': '例如：012-3456789',
        'placeholder_contact_notes': '例如：家庭治疗师，工作日可用',
        'placeholder_member_name': '例如：莎拉',
        'placeholder_child_name': '例如：小明',
        'placeholder_age': '例如：5岁',
        'placeholder_diagnosis': '例如：ASD 2级，ADHD',
        'placeholder_event_notes': '发生了什么？',
        'english': 'English',
        'bahasa_melayu': 'Bahasa Melayu',
        'chinese': '中文'
    }
}

def get_text(key):
    """Get translated text based on current language"""
    lang = st.session_state.get('language', 'en')
    return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)

def get_language_display():
    """Get current language display name"""
    lang_map = {
        'en': 'EN',
        'ms': 'BM',
        'zh': '中文'
    }
    return lang_map.get(st.session_state.language, 'EN')

# 1. SETUP & STYLING
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = ""
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Load favicon
try:
    favicon = Image.open("prismchat_logo.png")
    PAGE_ICON = favicon
except:
    PAGE_ICON = "🧩"

st.set_page_config(
    page_title="PrismCHAT", 
    page_icon=PAGE_ICON,
    layout="centered", 
    initial_sidebar_state="expanded" 
)

# 2. USER PROFILE & MULTI-USER FUNCTIONS
USERS_FILE = "users.json"
BEHAVIOR_FILE = "behavior_logs.json"

def load_users():
    """Load all user profiles"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save user profiles"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving users: {e}")

def create_default_user():
    """Create default user profile"""
    return {
        'name': 'Default User',
        'role': 'Parent',
        'child_name': '',
        'child_age': '',
        'diagnosis': '',
        'triggers': [],
        'interests': '',
        'sensory_needs': '',
        'communication_style': 'Verbal',
        'notes': '',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def get_current_user():
    """Get current active user"""
    users = load_users()
    current_user_id = st.session_state.get('current_user_id', 'default')
    
    if current_user_id not in users:
        users['default'] = create_default_user()
        save_users(users)
    
    return users.get(current_user_id, create_default_user())

def load_behavior_logs():
    """Load behavior tracking logs"""
    if os.path.exists(BEHAVIOR_FILE):
        try:
            with open(BEHAVIOR_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_behavior_logs(logs):
    """Save behavior logs"""
    try:
        with open(BEHAVIOR_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving logs: {e}")

def add_behavior_event(event_type, description, intensity, triggers):
    """Add new behavior event"""
    logs = load_behavior_logs()
    user_id = st.session_state.get('current_user_id', 'default')
    
    if user_id not in logs:
        logs[user_id] = []
    
    event = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'type': event_type,
        'description': description,
        'intensity': intensity,
        'triggers': triggers,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M')
    }
    
    logs[user_id].append(event)
    save_behavior_logs(logs)
    return True

# 3. SENTIMENT ANALYSIS FUNCTIONS
def analyze_sentiment(text):
    """
    Simple rule-based sentiment analysis for autism support context
    Returns: sentiment (calm/neutral/distressed) and confidence score
    """
    text_lower = text.lower()
    
    distressed_keywords = [
        'help', 'scared', 'anxious', 'worried', 'stress', 'overwhelmed', 
        'meltdown', 'panic', 'can\'t', 'difficult', 'hard', 'struggle',
        'frustrated', 'upset', 'angry', 'sad', 'cry', 'alone', 'afraid',
        'emergency', 'crisis', 'hurt', 'pain'
    ]
    
    calm_keywords = [
        'thank', 'good', 'better', 'help', 'understand', 'calm', 'peaceful',
        'relax', 'happy', 'progress', 'improving', 'manageable', 'cope',
        'comfortable', 'safe', 'ok', 'fine', 'glad'
    ]
    
    distressed_count = sum(1 for word in distressed_keywords if word in text_lower)
    calm_count = sum(1 for word in calm_keywords if word in text_lower)
    
    urgent_patterns = ['emergency', 'crisis', 'immediate help', 'right now', 'can\'t handle']
    is_urgent = any(pattern in text_lower for pattern in urgent_patterns)
    
    question_count = text.count('?')
    
    if is_urgent or distressed_count >= 3:
        return "distressed", "high"
    elif distressed_count > calm_count:
        return "distressed", "medium"
    elif calm_count > distressed_count:
        return "calm", "medium"
    elif question_count >= 2:
        return "neutral", "medium"
    else:
        return "neutral", "low"

def get_sentiment_emoji(sentiment):
    """Return emoji for sentiment"""
    emoji_map = {
        "calm": "😊",
        "neutral": "😐",
        "distressed": "😟"
    }
    return emoji_map.get(sentiment, "😐")

def get_sentiment_color(sentiment):
    """Return color for sentiment indicator"""
    color_map = {
        "calm": "#4CAF50",
        "neutral": "#FFC107",
        "distressed": "#F44336"
    }
    return color_map.get(sentiment, "#FFC107")

def calculate_session_summary():
    """Calculate emotion breakdown for current session"""
    if not st.session_state.messages:
        return None
    
    user_messages = [msg for msg in st.session_state.messages if msg['role'] == 'user']
    
    if not user_messages:
        return None
    
    sentiments = []
    for msg in user_messages:
        sentiment, _ = analyze_sentiment(msg['content'])
        sentiments.append(sentiment)
    
    sentiment_counts = Counter(sentiments)
    total = len(sentiments)
    
    summary = {
        'calm': (sentiment_counts.get('calm', 0) / total) * 100,
        'neutral': (sentiment_counts.get('neutral', 0) / total) * 100,
        'distressed': (sentiment_counts.get('distressed', 0) / total) * 100,
        'total_messages': total,
        'dominant_emotion': max(sentiment_counts, key=sentiment_counts.get) if sentiment_counts else 'neutral'
    }
    
    return summary

# 4. CHAT HISTORY FUNCTIONS
HISTORY_FILE = "chat_history.json"

def load_chat_history():
    """Load chat history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(history):
    """Save chat history to JSON file"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving history: {e}")

def save_current_chat():
    """Save current conversation to history with sentiment data"""
    if st.session_state.messages and len(st.session_state.messages) > 0:
        history = load_chat_history()
        
        current_chat_id = st.session_state.get('current_chat_id', None)
        
        if not current_chat_id:
            current_chat_id = datetime.now().strftime('%Y%m%d_%H%M%S')
            st.session_state.current_chat_id = current_chat_id
        
        existing_index = next((i for i, chat in enumerate(history) if chat['id'] == current_chat_id), None)
        
        first_msg = next((msg['content'][:50] for msg in st.session_state.messages if msg['role'] == 'user'), 'New Chat')
        
        sentiment_summary = calculate_session_summary()
        
        chat_data = {
            'id': current_chat_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'title': first_msg,
            'messages': st.session_state.messages.copy(),
            'sentiment_summary': sentiment_summary,
            'user_id': st.session_state.get('current_user_id', 'default')
        }
        
        if existing_index is not None:
            history[existing_index] = chat_data
        else:
            history.insert(0, chat_data)
        
        history = history[:50]
        
        save_chat_history(history)
        return True
    return False

def load_chat_by_id(chat_id):
    """Load a specific chat from history"""
    history = load_chat_history()
    for chat in history:
        if chat['id'] == chat_id:
            st.session_state.messages = chat['messages'].copy()
            st.session_state.current_chat_id = chat_id
            st.rerun()

def delete_chat_by_id(chat_id):
    """Delete a specific chat from history"""
    history = load_chat_history()
    history = [chat for chat in history if chat['id'] != chat_id]
    save_chat_history(history)
    st.rerun()

# 5. SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "show_sentiment" not in st.session_state:
    st.session_state.show_sentiment = True
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "language" not in st.session_state:
    st.session_state.language = 'en'
if "current_user_id" not in st.session_state:
    st.session_state.current_user_id = 'default'
if "show_analytics" not in st.session_state:
    st.session_state.show_analytics = False
if "show_profile_page" not in st.session_state:
    st.session_state.show_profile_page = False

# 6. DYNAMIC THEME & CSS
if st.session_state.dark_mode:
    # DARK MODE - Refined colors
    text_color = "#E8E8E8"
    bg_color = "#0A0A0A"
    sidebar_bg = "#121212"
    input_bg = "#1A1A1A"
    border_color = "#2A2A2A" 
    placeholder_color = "#8A8A8A"
    code_bg = "#1E1E1E"
    code_text = "#E8E8E8"
    accent_color = "#7C3AED"
    hover_bg = "#252525"
else:
    # LIGHT MODE - Refined colors
    text_color = "#1A1A1A"
    bg_color = "#FAFAFA"
    sidebar_bg = "#FFFFFF"
    input_bg = "#F5F5F5"
    border_color = "#E0E0E0"
    placeholder_color = "#6B6B6B"
    code_bg = "#F0F0F0"
    code_text = "#1A1A1A"
    accent_color = "#7C3AED"
    hover_bg = "#F0F0F0"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* ============= ROOT & GLOBAL ============= */
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
    }}
    
    html, body, #root, .stApp, 
    [data-testid="stAppViewContainer"], 
    [data-testid="stHeader"], 
    [data-testid="stMainViewContainer"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* BLOCKS & CONTAINERS */
    div, section, article, main,
    [data-testid="stVerticalBlock"],
    [data-testid="stHorizontalBlock"],
    [data-testid="column"],
    .element-container,
    .row-widget {{
        background-color: transparent !important;
    }}

    /* ============= CUSTOM HAMBURGER MENU (TOP RIGHT) ============= */
    #hamburger-menu-button {{
        position: fixed;
        top: 0.75rem;
        right: 5.5rem;
        z-index: 9999;
        background-color: {sidebar_bg};
        border: 1.5px solid {border_color};
        border-radius: 8px;
        padding: 8px 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    #hamburger-menu-button:hover {{
        border-color: {accent_color};
        background-color: {hover_bg};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15);
    }}
    
    #hamburger-menu-button:active {{
        transform: translateY(0px);
    }}
    
    .hamburger-icon {{
        font-size: 1.3rem;
        color: {text_color};
        line-height: 1;
        user-select: none;
    }}
    
    .hamburger-label {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {text_color};
        letter-spacing: 0.02em;
    }}
    
    /* Hide hamburger when in settings page */
    .hide-hamburger {{
        display: none !important;
    }}

    /* ============= SETTINGS BUTTON (TOP RIGHT) ============= */
    .settings-button {{
        position: fixed;
        top: 0.75rem;
        right: 5.5rem;
        z-index: 9999;
    }}

    /* ============= CHAT INPUT ============= */
    [data-testid="stChatInput"] textarea {{
        background-color: {input_bg} !important;
        color: {text_color} !important; 
        border: 1.5px solid {border_color} !important;
        border-radius: 16px !important;
        padding: 14px 16px !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        transition: all 0.2s ease !important;
    }}
    
    [data-testid="stChatInput"] textarea:focus {{
        border-color: {accent_color} !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
    }}
    
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {placeholder_color} !important;
        opacity: 0.8 !important;
    }}

    /* ============= SIDEBAR ============= */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border_color} !important;
    }}

    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown *,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] li {{
        color: {text_color} !important;
    }}

    /* ============= BUTTONS ============= */
    div.stButton > button {{
        width: 100%;
        border-radius: 12px;
        border: 1.5px solid {border_color} !important;
        background-color: {input_bg} !important;
        color: {text_color} !important;
        padding: 0.65rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
    }}
    
    div.stButton > button:hover {{
        border-color: {accent_color} !important;
        background-color: {hover_bg} !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1);
    }}
    
    div.stButton > button:active {{
        transform: translateY(0px);
    }}
    
    /* Remove red focus outline */
    div.stButton > button:focus {{
        outline: none !important;
        box-shadow: 0 0 0 2px {accent_color}40 !important;
    }}
    
    div.stButton > button:focus:not(:focus-visible) {{
        box-shadow: none !important;
    }}
    
    div.stButton > button p,
    div.stButton > button span {{
        color: {text_color} !important;
    }}
    
    /* Primary Button Style */
    div.stButton > button[kind="primary"] {{
        background-color: {accent_color} !important;
        color: white !important;
        border-color: {accent_color} !important;
    }}
    
    div.stButton > button[kind="primary"]:hover {{
        background-color: #6D28D9 !important;
        border-color: #6D28D9 !important;
    }}
    
    /* Ensure primary button text is always white */
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span {{
        color: white !important;
    }}
    
    /* ============= TEXT ELEMENTS ============= */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
    .stMarkdown p, .stMarkdown span, .stMarkdown li,
    .stMarkdown strong, .stMarkdown em {{
        color: {text_color} !important;
    }}
    
    .stMarkdown h1 {{
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}
    
    .stMarkdown h2 {{
        font-weight: 600 !important;
    }}
    
    /* ============= CODE BLOCKS ============= */
    .stMarkdown code,
    code {{
        background-color: {code_bg} !important;
        color: {code_text} !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        border: 1px solid {border_color} !important;
        font-family: 'Fira Code', 'Monaco', monospace !important;
        font-size: 0.875rem !important;
    }}
    
    /* ============= METRICS ============= */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {{
        color: {text_color} !important;
    }}

    /* ============= INPUT FIELDS ============= */
    input[type="text"],
    input[type="number"],
    textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1.5px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 0.6rem 0.8rem !important;
        transition: all 0.2s ease !important;
    }}
    
    input[type="text"]:focus,
    input[type="number"]:focus,
    textarea:focus,
    [data-testid="stTextInput"] input:focus,
    [data-testid="stTextArea"] textarea:focus {{
        border-color: {accent_color} !important;
        box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1) !important;
        outline: none !important;
    }}
    
    input::placeholder,
    textarea::placeholder {{
        color: {placeholder_color} !important;
        opacity: 0.7 !important;
    }}
    
    /* ============= SELECTBOX ============= */
    [data-baseweb="select"],
    [data-baseweb="select"] *,
    [role="listbox"],
    [role="option"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border-radius: 10px !important;
    }}
    
    [role="option"]:hover {{
        background-color: {hover_bg} !important;
    }}
    
    /* ============= EXPANDERS ============= */
    .streamlit-expanderHeader,
    details summary,
    summary,
    [data-testid="stExpander"] summary,
    div[data-testid="stExpander"] > details > summary {{
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        padding: 10px 14px !important;
        background-color: {input_bg} !important;
        border: 1.5px solid {border_color} !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
    }}
    
    .streamlit-expanderHeader:hover,
    details summary:hover,
    [data-testid="stExpander"] summary:hover {{
        border-color: {accent_color} !important;
        background-color: {hover_bg} !important;
    }}
    
    .streamlit-expanderHeader,
    .streamlit-expanderHeader *,
    .streamlit-expanderHeader p,
    .streamlit-expanderHeader span,
    details summary,
    details summary *,
    summary,
    summary *,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary * {{
        color: {text_color} !important;
    }}
    
    .streamlit-expanderHeader svg,
    details summary svg,
    summary svg,
    [data-testid="stExpander"] svg {{
        fill: {text_color} !important;
        stroke: {text_color} !important;
    }}
    
    .streamlit-expanderContent,
    details > div,
    [data-testid="stExpander"] > div:not(summary) {{
        padding: 12px 8px !important;
        background-color: transparent !important;
        margin-top: 8px !important;
    }}
    
    .streamlit-expanderContent,
    .streamlit-expanderContent *,
    details > div,
    details > div * {{
        color: {text_color} !important;
    }}
    
    .streamlit-expanderContent code,
    details code {{
        background-color: {code_bg} !important;
        color: {code_text} !important;
    }}
    
    /* ============= INFO/SUCCESS/WARNING BOXES ============= */
    [data-testid="stInfo"],
    [data-testid="stSuccess"],
    [data-testid="stWarning"] {{
        background-color: {input_bg} !important;
        color: {text_color} !important;
        border: 1.5px solid {border_color} !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
    }}
    
    [data-testid="stInfo"] *,
    [data-testid="stSuccess"] *,
    [data-testid="stWarning"] * {{
        color: {text_color} !important;
    }}
    
    /* ============= SLIDER ============= */
    [data-testid="stSlider"] {{
        padding: 0.5rem 0 !important;
    }}
    
    /* ============= TABS ============= */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        border-bottom: 2px solid {border_color};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: {placeholder_color} !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {hover_bg} !important;
        color: {text_color} !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {input_bg} !important;
        color: {accent_color} !important;
        border-bottom: 2px solid {accent_color} !important;
    }}
    
    /* ============= DIVIDER ============= */
    hr {{
        border-color: {border_color} !important;
        margin: 1.5rem 0 !important;
    }}
    
    /* ============= SCROLLBAR ============= */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {bg_color};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {border_color};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {placeholder_color};
    }}
    
    /* ============= HIDE IMAGE ZOOM ============= */
    button[title="View fullscreen"] {{
        display: none !important;
    }}
    
    /* ============= CHAT MESSAGES ============= */
    [data-testid="stChatMessage"] {{
        padding: 1rem !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
    }}
    
    /* ============= ANIMATIONS ============= */
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .element-container {{
        animation: slideIn 0.3s ease-out;
    }}
    </style>
    """, unsafe_allow_html=True)

# Session state for settings page
if "show_settings_page" not in st.session_state:
    st.session_state.show_settings_page = False

# 7. SIDEBAR (Only show when NOT in settings page)
if not st.session_state.show_settings_page:
    with st.sidebar:
        # Logo
        try:
            st.markdown("""
                <div style='padding: 0 10px; margin-bottom: -20px;'>
                    <img src='data:image/png;base64,{}' style='width: 100%; max-width: 280px; margin: 0 auto; display: block;'>
                </div>
            """.format(__import__('base64').b64encode(open('prismchat_logo.png', 'rb').read()).decode()), unsafe_allow_html=True)
            st.markdown("<div style='margin-top: -20px; margin-bottom: -10px;'></div>", unsafe_allow_html=True)
        except:
            st.markdown(f"<h1 style='color:{text_color}; text-align: center;'>🧩 {get_text('app_title')}</h1>", unsafe_allow_html=True)
        
        # Current User Display - MINIMALIST
        current_user = get_current_user()
        st.markdown(f"""
            <p style='text-align: center; 
                      color: {text_color}; 
                      font-size: 0.85rem; 
                      font-weight: 500;
                      margin: 8px 0 12px 0;
                      padding: 8px 14px;
                      background-color: {input_bg};
                      border-radius: 8px;
                      border: 1px solid {border_color};'>
                {current_user['name']}
            </p>
        """, unsafe_allow_html=True)
        
        # Main Action Button - NEW CHAT ONLY (Full Width)
        if st.button(f"+ {get_text('new_chat')}", use_container_width=True, key="new_chat_btn"):
            save_current_chat()
            st.session_state.messages = []
            st.session_state.current_chat_id = None
            st.rerun()
        
        st.divider()
        
        # COLLAPSIBLE SECTIONS - MINIMAL ICONS
        
        # 1. Quick Help
        with st.expander(get_text('quick_help')):
            if st.button(f"› {get_text('early_signs')}", key="q1"):
                st.session_state.messages.append({"role": "user", "content": get_text('early_signs_q')})
                st.rerun()
            
            if st.button(f"› {get_text('managing_meltdowns')}", key="q2"):
                st.session_state.messages.append({"role": "user", "content": get_text('meltdowns_q')})
                st.rerun()
            
            if st.button(f"› {get_text('support_parents')}", key="q3"):
                st.session_state.messages.append({"role": "user", "content": get_text('parents_q')})
                st.rerun()
        
        # 2. Behavior Tracker
        with st.expander(get_text('behavior_tracker')):
            event_type = st.selectbox(get_text('event'), ["Meltdown", "Success", "Other"], label_visibility="collapsed")
            intensity = st.slider(get_text('intensity'), 1, 10, 5, label_visibility="collapsed")
            description = st.text_area(get_text('notes'), placeholder=get_text('placeholder_event_notes'), label_visibility="collapsed", height=80)
            
            if st.button(f"+ {get_text('add_event')}", use_container_width=True):
                if description:
                    add_behavior_event(event_type, description, intensity, [])
                    st.success(get_text('event_logged'))
                else:
                    st.warning(get_text('please_add_notes'))
            
            st.divider()
            
            if st.button(get_text('view_analytics'), use_container_width=True):
                st.session_state.show_analytics = True
                st.rerun()
        
        # 3. Chat History - CLEAN SENTIMENT DISPLAY
        with st.expander(get_text('chat_history')):
            history = load_chat_history()
            current_user_id = st.session_state.get('current_user_id', 'default')
            user_chats = [chat for chat in history if chat.get('user_id', 'default') == current_user_id]
            
            if user_chats:
                for chat in user_chats[:5]:
                    # Get sentiment data - MINIMAL INDICATOR
                    sentiment_indicator = ""
                    
                    if 'sentiment_summary' in chat and chat['sentiment_summary']:
                        summary = chat['sentiment_summary']
                        dominant = summary.get('dominant_emotion', 'neutral')
                        # Minimal color indicator instead of emoji
                        color_map = {
                            'calm': '#4CAF50',
                            'neutral': '#FFC107', 
                            'distressed': '#F44336'
                        }
                        sentiment_color = color_map.get(dominant, '#FFC107')
                        sentiment_indicator = f"<span style='display:inline-block; width:6px; height:6px; border-radius:50%; background:{sentiment_color}; margin-right:6px;'></span>"
                    
                    # Chat title button
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        # Display with HTML for color indicator
                        st.markdown(f"""
                            <div style='margin-bottom: 4px;'>
                        """, unsafe_allow_html=True)
                        
                        if st.button(
                            f"{chat['title'][:28]}...",
                            key=f"load_{chat['id']}",
                            use_container_width=True
                        ):
                            current_chat_id = st.session_state.get('current_chat_id', None)
                            if current_chat_id != chat['id']:
                                save_current_chat()
                            load_chat_by_id(chat['id'])
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col2:
                        if st.button("×", key=f"del_{chat['id']}"):
                            delete_chat_by_id(chat['id'])
                    
                    # Sentiment breakdown - MINIMALIST BARS WITH LABELS
                    if 'sentiment_summary' in chat and chat['sentiment_summary']:
                        summary = chat['sentiment_summary']
                        calm_pct = summary.get('calm', 0)
                        neutral_pct = summary.get('neutral', 0)
                        distressed_pct = summary.get('distressed', 0)
                        
                        st.markdown(f"""
                            <div style='margin: -8px 0 10px 0;'>
                                <!-- Progress Bar -->
                                <div style='display: flex; 
                                            gap: 4px; 
                                            height: 4px;
                                            border-radius: 2px;
                                            overflow: hidden;
                                            margin-bottom: 4px;'>
                                    <div style='flex: {calm_pct}; 
                                                background: #4CAF50;'></div>
                                    <div style='flex: {neutral_pct}; 
                                                background: #FFC107;'></div>
                                    <div style='flex: {distressed_pct}; 
                                                background: #F44336;'></div>
                                </div>
                                <!-- Labels -->
                                <div style='display: flex; 
                                            justify-content: space-between; 
                                            font-size: 0.65rem; 
                                            color: {placeholder_color};
                                            font-weight: 500;
                                            letter-spacing: 0.02em;'>
                                    <span>C: {calm_pct:.0f}%</span>
                                    <span>N: {neutral_pct:.0f}%</span>
                                    <span>D: {distressed_pct:.0f}%</span>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info(get_text('no_history_yet'))
        
        # Spacer before Settings & Footer
        st.markdown(f"""
            <div style='margin: 24px 0; 
                        border-top: 2px solid {border_color};'>
            </div>
        """, unsafe_allow_html=True)
        
        # Settings Button - MINIMAL
        if st.button(get_text('settings'), use_container_width=True, key="settings_btn"):
            st.session_state.show_settings_page = True
            st.rerun()

        # Footer - CLEAN
        st.markdown(f"""
            <div style='text-align: center; 
                        padding: 16px 0 8px 0;
                        margin-top: 16px;
                        border-top: 1px solid {border_color};
                        color: {placeholder_color};
                        font-size: 0.7rem;'>
                <p style='margin: 0; line-height: 1.6;'>
                    © 2025 PrismCHAT<br>
                    <span style='color: {accent_color}; font-weight: 500;'>Mirza Azhar</span>
                </p>
            </div>
        """, unsafe_allow_html=True)





# 8. SETTINGS PAGE - MINIMALIST DESIGN
if st.session_state.show_settings_page:
    st.title(get_text('settings'))
    
    # Back button - CLEAN
    if st.button(f"← {get_text('back')}"):
        st.session_state.show_settings_page = False
        st.rerun()
    
    st.divider()
    
    # Settings Tabs - NO EMOJIS
    tab1, tab2, tab3, tab4 = st.tabs([
        get_text('appearance'), 
        get_text('user_profile'), 
        get_text('emergency'), 
        get_text('family')
    ])
    
    # ========== TAB 1: APPEARANCE ==========
    with tab1:
        st.subheader(get_text('theme'))
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            theme_display = get_text('dark_mode') if st.session_state.dark_mode else get_text('light_mode')
            
            st.markdown(f"""
                <div style='text-align: center; 
                            padding: 40px 20px;
                            background-color: {input_bg};
                            border-radius: 12px;
                            border: 1px solid {border_color};'>
                    <div style='width: 60px; 
                                height: 60px; 
                                margin: 0 auto 16px; 
                                border-radius: 50%; 
                                background: {"linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)" if st.session_state.dark_mode else "linear-gradient(135deg, #ffffff 0%, #f5f5f5 100%)"}; 
                                border: 2px solid {border_color};'></div>
                    <h4 style='color: {text_color}; margin: 0; font-size: 1.1rem;'>{theme_display}</h4>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            theme_desc = get_text('dark_reduces_strain') if st.session_state.dark_mode else get_text('light_better_visibility')
            
            st.markdown(f"""
                <div style='padding: 20px 0;'>
                    <h4 style='color: {text_color}; margin-bottom: 12px; font-size: 1rem;'>{get_text('current_theme')}</h4>
                    <p style='color: {placeholder_color}; line-height: 1.6; font-size: 0.9rem;'>
                        {theme_desc}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            switch_text = get_text('switch_to_light') if st.session_state.dark_mode else get_text('switch_to_dark')
            
            if st.button(switch_text, use_container_width=True, type="primary"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        st.divider()
        
        st.subheader(get_text('language'))
        
        col3, col4 = st.columns([1, 2])
        
        with col3:
            lang_names = {
                'en': get_text('english'), 
                'ms': get_text('bahasa_melayu'), 
                'zh': get_text('chinese')
            }
            current_lang = st.session_state.language
            
            st.markdown(f"""
                <div style='text-align: center; 
                            padding: 40px 20px;
                            background-color: {input_bg};
                            border-radius: 12px;
                            border: 1px solid {border_color};'>
                    <div style='width: 60px; 
                                height: 60px; 
                                margin: 0 auto 16px; 
                                border-radius: 50%; 
                                background: linear-gradient(135deg, {accent_color} 0%, #9333EA 100%); 
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                color: white;
                                font-weight: 600;
                                font-size: 1.2rem;'>{current_lang.upper()}</div>
                    <h4 style='color: {text_color}; margin: 0; font-size: 1.1rem;'>{lang_names[current_lang]}</h4>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            
            selected_lang = st.selectbox(
                get_text('select_language'),
                options=['en', 'ms', 'zh'],
                format_func=lambda x: lang_names[x],
                index=['en', 'ms', 'zh'].index(current_lang)
            )
            
            if selected_lang != current_lang:
                st.session_state.language = selected_lang
                st.success(get_text('language_updated'))
                st.rerun()

    # ========== TAB 2: USER PROFILE ==========
    with tab2:
        current_user = get_current_user()
        users = load_users()
        
        st.subheader("Child Information")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            child_name = st.text_input(
                "Child's Name",
                value=current_user.get('child_name', ''),
                placeholder="e.g., Ahmad"
            )
            
            child_age = st.text_input(
                "Age",
                value=current_user.get('child_age', ''),
                placeholder="e.g., 5 years old"
            )
            
            diagnosis = st.text_area(
                "Diagnosis",
                value=current_user.get('diagnosis', ''),
                placeholder="e.g., ASD Level 2, ADHD",
                height=100
            )
        
        with col2:
            st.info("""
            **Profile Benefits**
            
            • Personalized advice
            • Age-appropriate tips
            • Context-aware support
            • Better recommendations
            """)
        
        st.divider()
        
        st.subheader("Additional Details")
        
        col3, col4 = st.columns(2)
        
        with col3:
            triggers_input = st.text_area(
                "Known Triggers",
                value='\n'.join(current_user.get('triggers', [])),
                placeholder="One per line, e.g.:\nLoud noises\nCrowds",
                height=120
            )
            
            communication_style = st.selectbox(
                "Communication Style",
                ["Verbal", "Non-verbal", "Limited verbal", "Uses AAC device"],
                index=["Verbal", "Non-verbal", "Limited verbal", "Uses AAC device"].index(
                    current_user.get('communication_style', 'Verbal')
                )
            )
        
        with col4:
            interests = st.text_area(
                "Interests & Strengths",
                value=current_user.get('interests', ''),
                placeholder="e.g., Loves trains, Good at puzzles",
                height=120
            )
            
            sensory_needs = st.text_area(
                "Sensory Needs",
                value=current_user.get('sensory_needs', ''),
                placeholder="e.g., Needs quiet space, Prefers dim lighting",
                height=120
            )
        
        notes = st.text_area(
            "Additional Notes",
            value=current_user.get('notes', ''),
            placeholder="Any other important information...",
            height=100
        )
        
        # Save button
        col_save1, col_save2, col_save3 = st.columns([1, 1, 1])
        
        with col_save2:
            if st.button("Save Profile", use_container_width=True, type="primary"):
                if child_name:
                    user_id = st.session_state.current_user_id
                    users[user_id]['child_name'] = child_name
                    users[user_id]['child_age'] = child_age
                    users[user_id]['diagnosis'] = diagnosis
                    users[user_id]['triggers'] = [t.strip() for t in triggers_input.split('\n') if t.strip()]
                    users[user_id]['communication_style'] = communication_style
                    users[user_id]['interests'] = interests
                    users[user_id]['sensory_needs'] = sensory_needs
                    users[user_id]['notes'] = notes
                    
                    save_users(users)
                    st.success(f"Profile saved for {child_name}")
                    st.balloons()
                else:
                    st.error("Please enter child's name")
    
    # ========== TAB 3: EMERGENCY RESOURCES ==========
    with tab3:
        st.subheader("Emergency Contacts")
        
        # Malaysia Crisis Hotlines - MINIMAL DESIGN
        st.markdown(f"""
            <div style='background-color: {input_bg}; 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 3px solid #F44336;
                        margin-bottom: 16px;'>
                <h4 style='color: {text_color}; margin-top: 0; font-size: 1rem;'>Crisis Hotlines (Malaysia)</h4>
                <div style='color: {text_color}; line-height: 1.8;'>
                    <p style='margin: 8px 0;'>
                        <strong>Befrienders KL</strong><br>
                        <code style='background: {code_bg}; padding: 2px 8px; border-radius: 4px;'>03-7956 8145</code><br>
                        <span style='color: {placeholder_color}; font-size: 0.85rem;'>24/7 Emotional support</span>
                    </p>
                    <p style='margin: 8px 0;'>
                        <strong>Mental Health Helpline</strong><br>
                        <code style='background: {code_bg}; padding: 2px 8px; border-radius: 4px;'>03-2935 9935</code><br>
                        <span style='color: {placeholder_color}; font-size: 0.85rem;'>Professional counseling</span>
                    </p>
                    <p style='margin: 8px 0;'>
                        <strong>Talian Kasih</strong><br>
                        <code style='background: {code_bg}; padding: 2px 8px; border-radius: 4px;'>15999</code><br>
                        <span style='color: {placeholder_color}; font-size: 0.85rem;'>Women & children protection</span>
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Autism Support Centers - MINIMAL DESIGN
        st.markdown(f"""
            <div style='background-color: {input_bg}; 
                        padding: 20px; 
                        border-radius: 10px; 
                        border-left: 3px solid {accent_color};
                        margin-bottom: 16px;'>
                <h4 style='color: {text_color}; margin-top: 0; font-size: 1rem;'>Autism Support Centers</h4>
                <div style='color: {text_color}; line-height: 1.8;'>
                    <p style='margin: 8px 0;'>
                        <strong>NASOM</strong><br>
                        <code style='background: {code_bg}; padding: 2px 8px; border-radius: 4px;'>03-4023 8400</code><br>
                        <span style='color: {placeholder_color}; font-size: 0.85rem;'>National Autism Society of Malaysia</span>
                    </p>
                    <p style='margin: 8px 0;'>
                        <strong>Genius Kurnia</strong><br>
                        <code style='background: {code_bg}; padding: 2px 8px; border-radius: 4px;'>03-4108 5858</code><br>
                        <span style='color: {placeholder_color}; font-size: 0.85rem;'>Early intervention & therapy</span>
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Emergency Tips - MINIMAL
        with st.expander("Emergency Response Guidelines"):
            st.markdown("""
            **During a Crisis:**
            - Stay calm, speak softly
            - Remove triggers if possible
            - Give space and time
            - Use visual supports
            - Avoid physical restraint
            
            **When to Seek Help:**
            - Risk of harm
            - Prolonged distress (30+ min)
            - Medical emergency
            - Caregiver overwhelmed
            """)
        
        # Add Personal Emergency Contact
        st.divider()
        st.subheader("Add Personal Contact")
        
        col1, col2 = st.columns(2)
        with col1:
            contact_name = st.text_input("Name", placeholder="e.g., Dr. Sarah")
        with col2:
            contact_number = st.text_input("Phone", placeholder="e.g., 012-3456789")
        
        contact_notes = st.text_area("Notes", placeholder="e.g., Family therapist, available weekdays", height=60)
        
        if st.button("Save Contact", use_container_width=True):
            if contact_name and contact_number:
                st.success(f"Contact saved: {contact_name}")
            else:
                st.warning("Please fill in name and number")
    
    # ========== TAB 4: FAMILY MEMBERS ==========
    with tab4:
        users = load_users()
        
        st.subheader("Family Members")
        
        # Display all users - MINIMAL CARDS
        for user_id, user in users.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                is_current = user_id == st.session_state.current_user_id
                active_text = ' · Active' if is_current else ''
                st.markdown(f"""
                    <div style='background-color: {input_bg};
                                padding: 12px 16px;
                                border-radius: 8px;
                                border-left: 3px solid {accent_color if is_current else border_color};
                                margin-bottom: 8px;
                                color: {text_color};
                                font-size: 0.9rem;'>
                        <strong>{user['name']}</strong> · {user['role']}{active_text}
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if not is_current:
                    if st.button("Switch", key=f"switch_{user_id}"):
                        st.session_state.current_user_id = user_id
                        st.success(f"Switched to {user['name']}")
                        st.rerun()
            
            with col3:
                if user_id != 'default' and not is_current:
                    if st.button("Delete", key=f"delete_{user_id}"):
                        del users[user_id]
                        save_users(users)
                        st.success("Member removed")
                        st.rerun()
        
        st.divider()
        
        # Add new member - CLEAN FORM
        st.subheader("Add Family Member")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Name", placeholder="e.g., Sarah", key="new_member_name")
        
        with col2:
            new_role = st.selectbox("Role", ["Parent", "Caregiver", "Therapist", "Teacher", "Other"], key="new_member_role")
        
        if st.button("Add Member", use_container_width=True, type="primary"):
            if new_name:
                new_user_id = f"user_{len(users)}"
                users[new_user_id] = create_default_user()
                users[new_user_id]['name'] = new_name
                users[new_user_id]['role'] = new_role
                save_users(users)
                st.success(f"Added {new_name}")
                st.balloons()
                st.rerun()
            else:
                st.error("Please enter a name")
    
    st.stop()

# 9. BEHAVIOR ANALYTICS PAGE
if st.session_state.show_analytics:
    st.title("📊 Behavior Analytics")
    
    logs = load_behavior_logs()
    user_id = st.session_state.get('current_user_id', 'default')
    user_logs = logs.get(user_id, [])
    
    if st.button("← Back to Chat"):
        st.session_state.show_analytics = False
        st.rerun()
    
    st.divider()
    
    if user_logs:
        df = pd.DataFrame(user_logs)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = pd.to_datetime(df['date'])
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Events", len(df))
        with col2:
            meltdown_count = len(df[df['type'] == 'Meltdown'])
            st.metric("Meltdowns", meltdown_count)
        with col3:
            if len(df) > 0:
                avg_intensity = df['intensity'].mean()
                st.metric("Avg Intensity", f"{avg_intensity:.1f}/10")
        with col4:
            success_count = len(df[df['type'] == 'Success'])
            st.metric("Successes", success_count)
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            event_counts = df['type'].value_counts()
            fig1 = px.pie(
                values=event_counts.values,
                names=event_counts.index,
                title="Event Distribution"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.box(
                df,
                x='type',
                y='intensity',
                title="Intensity by Type",
                color='type'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Timeline
        daily_counts = df.groupby('date').size().reset_index(name='count')
        fig3 = px.line(
            daily_counts,
            x='date',
            y='count',
            title="Events Over Time",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        # Recent Events
        st.subheader("Recent Events")
        recent_df = df.sort_values('timestamp', ascending=False).head(10)
        display_df = recent_df[['timestamp', 'type', 'intensity', 'description']].copy()
        st.dataframe(display_df, use_container_width=True)
        
    else:
        st.info("📭 No data yet. Start logging events!")
    
    st.stop()

# 10. MAIN CHAT UI (Only show when NOT in settings or analytics)
if not st.session_state.show_settings_page and not st.session_state.show_analytics:
    if not st.session_state.messages:
        st.markdown(f"""
            <div style='margin-top: 15vh; text-align: center;'>
                <h1 style='color: {text_color}; 
                           font-size: 3.5rem; 
                           font-weight: 700; 
                           letter-spacing: -0.03em;
                           margin-bottom: 1rem;
                           background: linear-gradient(135deg, {accent_color} 0%, #9333EA 100%);
                           -webkit-background-clip: text;
                           -webkit-text-fill-color: transparent;'>
                    {get_text('main_heading')}
                </h1>
                <p style='color: {placeholder_color}; 
                         font-size: 1.25rem;
                         font-weight: 400;
                         letter-spacing: 0.01em;'>
                    {get_text('main_subheading')}
                </p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='text-align: center; 
                        padding: 15px; 
                        border-bottom: 1.5px solid {border_color}; 
                        margin-bottom: 24px;
                        background-color: {sidebar_bg};
                        border-radius: 12px 12px 0 0;'>
                <h3 style='color: {text_color}; 
                           font-weight: 600; 
                           margin: 0;
                           font-size: 1.3rem;
                           letter-spacing: -0.01em;'>
                    💬 {get_text('chat_title')}
                </h3>
            </div>
        """, unsafe_allow_html=True)

    # Display messages
    for i, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"]):
            if msg["role"] == "user" and st.session_state.show_sentiment:
                sentiment, confidence = analyze_sentiment(msg["content"])
                emoji = get_sentiment_emoji(sentiment)
                color = get_sentiment_color(sentiment)
                
                st.markdown(f"""
                    <div style='display: inline-flex; 
                                align-items: center; 
                                gap: 8px;
                                padding: 4px 12px;
                                background-color: {input_bg};
                                border-radius: 20px;
                                border: 1px solid {border_color};
                                margin-bottom: 8px;'>
                        <span style='font-size: 1.1rem;'>{emoji}</span>
                        <span style='color: {color}; 
                                     font-size: 0.8rem; 
                                     font-weight: 600;
                                     letter-spacing: 0.03em;'>
                            {get_text(sentiment).upper()}
                        </span>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown(msg["content"])

    # 11. INPUT LOGIC
    user_input = st.chat_input(get_text('input_placeholder'))

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner(get_text('thinking')):
                try:
                    current_user = get_current_user()
                    profile_context = ""
                    
                    if current_user.get('child_name'):
                        profile_context += f"\nChild's name: {current_user['child_name']}"
                    if current_user.get('child_age'):
                        profile_context += f"\nChild's age: {current_user['child_age']}"
                    if current_user.get('diagnosis'):
                        profile_context += f"\nDiagnosis: {current_user['diagnosis']}"
                    if current_user.get('triggers'):
                        profile_context += f"\nKnown triggers: {', '.join(current_user['triggers'])}"
                    if current_user.get('communication_style'):
                        profile_context += f"\nCommunication: {current_user['communication_style']}"
                    if current_user.get('sensory_needs'):
                        profile_context += f"\nSensory needs: {current_user['sensory_needs']}"
                    
                    system_prompt = get_text('system_prompt')
                    if profile_context:
                        system_prompt += f"\n\nIMPORTANT - User Profile Context:{profile_context}"
                        system_prompt += f"\nPlease personalize your responses based on this child's profile. Use their name when appropriate."
                    
                    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
                    payload = {
                        "model": MODEL,
                        "messages": [{"role": "system", "content": system_prompt}] + st.session_state.messages,
                        "temperature": 0.5
                    }
                    response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
                    if response.status_code == 200:
                        reply = response.json()["choices"][0]["message"]["content"]
                        st.markdown(reply)
                        st.session_state.messages.append({"role": "assistant", "content": reply})
                    else:
                        st.error(get_text('api_error'))
                except:
                    st.error(get_text('connection_failed'))
