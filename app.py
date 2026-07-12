import streamlit as st
import pandas as pd
import uuid
import json
import os
import base64
import qrcode
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import hashlib
from io import BytesIO
from PIL import Image
from collections import Counter

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="医疗设备全生命周期管理系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 数据文件路径 ====================
DATA_FILE = "devices_data.json"
USERS_FILE = "users.json"
REPAIR_FILE = "repair_records.json"
MAINTENANCE_FILE = "maintenance_records.json"
LOG_FILE = "operation_log.json"
DEPARTMENT_FILE = "departments.json"
CONTRACT_FILE = "contracts_data.json"
TRANSFER_FILE = "transfer_records.json"
SCRAP_FILE = "scrap_records.json"
CHECK_FILE = "check_records.json"
PARTS_FILE = "parts_data.json"
KNOWLEDGE_FILE = "knowledge_data.json"

PHOTO_DIR = "device_photos"
FILE_DIR = "device_files"
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(FILE_DIR, exist_ok=True)

# ==================== 枚举定义 ====================
FAULT_TYPES = [
    "硬件故障", "软件问题", "网络故障", "电源故障", "传感器故障",
    "显示屏故障", "按键/面板故障", "连接线缆故障", "机械故障",
    "耗材问题", "校准问题", "系统崩溃", "数据异常", "其他"
]

FAULT_LEVELS = ["紧急", "重要", "一般"]

IMPACT_SCOPES = ["单机", "科室内部", "全院", "跨院区"]

REPAIR_METHODS = ["院内维修", "厂家维修", "外包维修"]

SLA_MAP = {"紧急": 24, "重要": 48, "一般": 72}

REPAIR_STATUSES = [
    "已提交", "已派单", "工程师接单", "维修完成", "已关闭"
]


# ==================== 数据持久化函数 ====================
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.devices, f, ensure_ascii=False, indent=2)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_users():
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.users, f, ensure_ascii=False, indent=2)

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_repair_records():
    with open(REPAIR_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.repair_records, f, ensure_ascii=False, indent=2)

def load_repair_records():
    if os.path.exists(REPAIR_FILE):
        try:
            with open(REPAIR_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_maintenance_records():
    with open(MAINTENANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.maintenance_records, f, ensure_ascii=False, indent=2)

def load_maintenance_records():
    if os.path.exists(MAINTENANCE_FILE):
        try:
            with open(MAINTENANCE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_contracts():
    with open(CONTRACT_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.contracts, f, ensure_ascii=False, indent=2)

def load_contracts():
    if os.path.exists(CONTRACT_FILE):
        try:
            with open(CONTRACT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_departments():
    with open(DEPARTMENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.departments, f, ensure_ascii=False, indent=2)

def load_departments():
    if os.path.exists(DEPARTMENT_FILE):
        try:
            with open(DEPARTMENT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_transfer_records():
    with open(TRANSFER_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.transfer_records, f, ensure_ascii=False, indent=2)

def load_transfer_records():
    if os.path.exists(TRANSFER_FILE):
        try:
            with open(TRANSFER_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_scrap_records():
    with open(SCRAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.scrap_records, f, ensure_ascii=False, indent=2)

def load_scrap_records():
    if os.path.exists(SCRAP_FILE):
        try:
            with open(SCRAP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_check_records():
    with open(CHECK_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.check_records, f, ensure_ascii=False, indent=2)

def load_check_records():
    if os.path.exists(CHECK_FILE):
        try:
            with open(CHECK_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_parts():
    with open(PARTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.parts, f, ensure_ascii=False, indent=2)

def load_parts():
    if os.path.exists(PARTS_FILE):
        try:
            with open(PARTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_knowledge():
    with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.knowledge_base, f, ensure_ascii=False, indent=2)

def load_knowledge():
    if os.path.exists(KNOWLEDGE_FILE):
        try:
            with open(KNOWLEDGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_log(operation, details):
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": st.session_state.get('username', 'unknown'),
        "role": st.session_state.get('role', 'unknown'),
        "operation": operation,
        "details": details
    }
    if 'operation_log' not in st.session_state:
        st.session_state.operation_log = []
    st.session_state.operation_log.append(log_entry)
    if len(st.session_state.operation_log) > 1000:
        st.session_state.operation_log = st.session_state.operation_log[-1000:]
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.operation_log, f, ensure_ascii=False, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_photo(uploaded_file, prefix):
    if uploaded_file is None:
        return ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = os.path.join(PHOTO_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filepath

def save_file(uploaded_file, device_id):
    if uploaded_file is None:
        return "", ""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    original_name = uploaded_file.name
    safe_name = f"{device_id}_{timestamp}_{original_name}"
    filepath = os.path.join(FILE_DIR, safe_name)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return original_name, filepath


# ==================== 辅助函数 ====================
def get_maintenance_status(maintenance_date):
    if not maintenance_date:
        return "未知", "⚪"
    try:
        maint = datetime.strptime(maintenance_date, "%Y-%m-%d")
        days_since = (datetime.now() - maint).days
        if days_since > 365:
            return "逾期", "🔴"
        elif days_since > 330:
            return "即将到期", "🟡"
        else:
            return "正常", "🟢"
    except:
        return "未知", "⚪"

def get_warranty_status(warranty_end):
    if not warranty_end:
        return "未知", "⚪"
    try:
        end = datetime.strptime(warranty_end, "%Y-%m-%d")
        days_left = (end - datetime.now()).days
        if days_left < 0:
            return "已过期", "🔴"
        elif days_left < 30:
            return "即将过期", "🟡"
        else:
            return "有效", "🟢"
    except:
        return "未知", "⚪"

def export_to_excel(data):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='设备台账')
    return output.getvalue()

def calculate_depreciation(device):
    purchase_date = device.get('purchase_date')
    price = device.get('price', 0)
    if not purchase_date or price <= 0:
        return 0, 0, price
    try:
        purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
        years = (datetime.now() - purchase).days / 365.25
        salvage_rate = 0.05
        useful_life = 5
        annual_depreciation = price * (1 - salvage_rate) / useful_life
        monthly_depreciation = annual_depreciation / 12
        total_depreciation = min(years * annual_depreciation, price * (1 - salvage_rate))
        net_value = price - total_depreciation
        if net_value < 0:
            net_value = 0
        return annual_depreciation / price, monthly_depreciation, net_value
    except:
        return 0, 0, price

def generate_device_qr(device_id, device_name):
    base_url = "https://device-manager-main-app-1406309105-hub.streamlit.app"
    qr_data = f"{base_url}?page=scan_repair&device_id={device_id}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a3a6b", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()
    return img_base64, qr_data

def generate_repair_no():
    today = datetime.now().strftime("%Y%m%d")
    today_records = [r for r in st.session_state.repair_records if r.get('工单号', '').startswith(f"REP-{today}")]
    seq = len(today_records) + 1
    return f"REP-{today}-{seq:03d}"

def get_repair_statistics():
    df = pd.DataFrame(st.session_state.repair_records) if st.session_state.repair_records else pd.DataFrame()
    if df.empty:
        return {'pending_count': 0, 'processing_count': 0, 'completed_count': 0, 'urgent_count': 0, 'total': 0}
    if '状态' not in df.columns:
        return {
            'pending_count': 0,
            'processing_count': 0,
            'completed_count': 0,
            'urgent_count': 0,
            'total': len(df)
        }
    pending = df[df['状态'].isin(['已提交', '已派单'])]
    processing = df[df['状态'].isin(['工程师接单'])]
    completed = df[df['状态'].isin(['维修完成', '已关闭'])]
    if '故障等级' in df.columns:
        urgent = pending[pending['故障等级'].isin(['紧急'])]
    elif 'urgency' in df.columns:
        urgent = pending[pending['urgency'].isin(['紧急', '特急'])]
    else:
        urgent = pd.DataFrame()
    return {
        'pending_count': len(pending),
        'processing_count': len(processing),
        'completed_count': len(completed),
        'urgent_count': len(urgent),
        'total': len(df)
    }

def show_repair_reminders():
    stats = get_repair_statistics()
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔔 报修提醒")
    if stats['urgent_count'] > 0:
        st.sidebar.error(f"🚨 紧急报修 {stats['urgent_count']} 单")
    if stats['pending_count'] > 0:
        st.sidebar.warning(f"📋 待处理报修 {stats['pending_count']} 单")
    if stats['urgent_count'] == 0 and stats['pending_count'] == 0:
        st.sidebar.success("✅ 暂无待处理报修")
    col1, col2, col3 = st.sidebar.columns(3)
    col1.metric("待处理", stats['pending_count'])
    col2.metric("处理中", stats['processing_count'])
    col3.metric("已完成", stats['completed_count'])
    return stats

def check_warranty_status():
    devices = st.session_state.devices
    expiring = []
    expired = []
    for d in devices:
        warranty_end = d.get('warranty_end', '')
        if warranty_end:
            try:
                end = datetime.strptime(warranty_end, "%Y-%m-%d")
                days_left = (end - datetime.now()).days
                if days_left < 0:
                    expired.append(d['name'])
                elif days_left < 30:
                    expiring.append(d['name'])
            except:
                pass
    return expiring, expired

def get_device_fault_rate():
    devices = st.session_state.devices
    records = st.session_state.repair_records
    if not devices or not records:
        return []
    fault_count = {}
    for r in records:
        device_info = r.get('设备信息', {})
        device_name = device_info.get('设备名称', '')
        if device_name:
            fault_count[device_name] = fault_count.get(device_name, 0) + 1
    result = []
    for d in devices:
        name = d.get('name', '')
        count = fault_count.get(name, 0)
        result.append({
            "设备名称": name,
            "报修次数": count,
            "状态": "🔴 高频故障" if count >= 3 else "🟡 偶尔故障" if count >= 1 else "🟢 正常"
        })
    return sorted(result, key=lambda x: x['报修次数'], reverse=True)[:10]


# ==================== 初始化数据 ====================
if 'devices' not in st.session_state:
    st.session_state.devices = load_data()
    if not st.session_state.devices:
        st.session_state.devices = []

if 'users' not in st.session_state:
    st.session_state.users = load_users()
    if not st.session_state.users:
        st.session_state.users = {
            "admin": {"password": hash_password("admin123"), "role": "admin", "name": "系统管理员"},
        }

if 'repair_records' not in st.session_state:
    st.session_state.repair_records = load_repair_records()

if 'maintenance_records' not in st.session_state:
    st.session_state.maintenance_records = load_maintenance_records()

if 'contracts' not in st.session_state:
    st.session_state.contracts = load_contracts()
    if not st.session_state.contracts:
        st.session_state.contracts = []

if 'transfer_records' not in st.session_state:
    st.session_state.transfer_records = load_transfer_records()
    if not st.session_state.transfer_records:
        st.session_state.transfer_records = []

if 'scrap_records' not in st.session_state:
    st.session_state.scrap_records = load_scrap_records()
    if not st.session_state.scrap_records:
        st.session_state.scrap_records = []

if 'check_records' not in st.session_state:
    st.session_state.check_records = load_check_records()
    if not st.session_state.check_records:
        st.session_state.check_records = []

if 'parts' not in st.session_state:
    st.session_state.parts = load_parts()
    if not st.session_state.parts:
        st.session_state.parts = [
            {"id": str(uuid.uuid4()), "name": "心电导联线", "model": "MR-ECG-01", "stock": 15, "unit": "根", "price": 280, "supplier": "迈瑞医疗"},
            {"id": str(uuid.uuid4()), "name": "CT球管", "model": "CT-TUBE-64", "stock": 2, "unit": "个", "price": 120000, "supplier": "西门子医疗"},
            {"id": str(uuid.uuid4()), "name": "除颤仪电极片", "model": "PD-ELEC-01", "stock": 30, "unit": "片", "price": 150, "supplier": "飞利浦医疗"},
        ]

if 'departments' not in st.session_state:
    st.session_state.departments = load_departments()
    if not st.session_state.departments:
        st.session_state.departments = ["ICU", "急诊科", "放射科", "超声科", "检验科", "手术室", "内科", "外科", "儿科", "妇产科"]

if 'operation_log' not in st.session_state:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            st.session_state.operation_log = json.load(f)
    else:
        st.session_state.operation_log = []

if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = load_knowledge()
    if not st.session_state.knowledge_base:
        st.session_state.knowledge_base = [
            {"id": str(uuid.uuid4()), "title": "监护仪常见故障", "category": "操作手册", 
             "content": "1. 黑屏：检查电源连接\n2. 无波形：检查导联线连接", 
             "author": "系统管理员", "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
            {"id": str(uuid.uuid4()), "title": "CT设备日常维护", "category": "维护指南", 
             "content": "1. 每日清洁扫描架\n2. 每周校准探测器", 
             "author": "系统管理员", "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        ]

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if 'quick_repair_mode' not in st.session_state:
    st.session_state.quick_repair_mode = False

if 'show_maintenance_reminder' not in st.session_state:
    st.session_state.show_maintenance_reminder = False

if 'target_menu' not in st.session_state:
    st.session_state.target_menu = None

if 'template_fault_type' not in st.session_state:
    st.session_state.template_fault_type = None

if 'template_description' not in st.session_state:
    st.session_state.template_description = None


# ==================== 登录页面 ====================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align:center;color:#1a3a6b;'>🏥 医疗设备管理系统</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;color:#666;'>Medical Equipment Management System</p>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            if st.form_submit_button("登录", use_container_width=True):
                if username in st.session_state.users:
                    if st.session_state.users[username]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = st.session_state.users[username]["role"]
                        save_log("登录系统", f"用户 {username} 登录成功")
                        st.success("登录成功！")
                        st.rerun()
                    else:
                        st.error("密码错误")
                else:
                    st.error("用户不存在")


# ==================== 侧边栏 ====================
def render_sidebar():
    with st.sidebar:
        st.markdown("### 🏥 医疗设备MIS")
        st.markdown(f"欢迎，**{st.session_state.username}**")
        show_repair_reminders()
        st.markdown("---")
        st.markdown("### 📋 导航菜单")
        menu_options = [
            "📊 仪表板",
            "📋 设备台账",
            "🔧 设备管理",
            "📋 设备验收",
            "🔄 资产调拨",
            "🗑️ 报废处置",
            "📊 资产盘点",
            "💰 资产折旧",
            "🏷️ 资产标签",
            "📱 扫码报修",
            "🚨 维修工单",
            "📅 保养计划",
            "📊 统计分析",
            "📄 合同管理",
            "⚙️ 系统设置"
        ]
        if st.session_state.role == "admin":
            menu_options.append("👥 用户管理")
            menu_options.append("📜 操作日志")
        menu = st.radio("", menu_options, label_visibility="collapsed")
        st.markdown("---")
        st.markdown("### ⚡ 快捷操作")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏥 快速报修", use_container_width=True):
                st.session_state.quick_repair_mode = True
                st.session_state.target_menu = "🚨 维修工单"
                st.rerun()
        with col2:
            if st.button("🔔 保养提醒", use_container_width=True):
                st.session_state.show_maintenance_reminder = True
                st.session_state.target_menu = "📅 保养计划"
                st.rerun()
        return menu


# ==================== 仪表板 ====================
def dashboard_page():
    st.markdown("<h2>📊 管理仪表板</h2>", unsafe_allow_html=True)
    devices = st.session_state.devices
    expiring, expired = check_warranty_status()
    if expired:
        st.error(f"🚨 {len(expired)} 台设备保修已过期：{', '.join(expired)}")
    if expiring:
        st.warning(f"⚠️ {len(expiring)} 台设备保修即将到期：{', '.join(expiring)}")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 总设备数", len(devices))
    with col2:
        total_value = sum(d.get('price', 0) for d in devices)
        st.metric("💰 总资产", f"¥{total_value:,.0f}")
    with col3:
        in_use = sum(1 for d in devices if d.get('status') == "在用")
        st.metric("✅ 使用中", in_use)
    with col4:
        repairing = sum(1 for d in devices if d.get('status') == "维修中")
        st.metric("🔧 维修中", repairing)
    st.markdown("---")
    stats = get_repair_statistics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📋 总报修", stats['total'])
    col2.metric("⏳ 待处理", stats['pending_count'])
    col3.metric("🛠️ 处理中", stats['processing_count'])
    col4.metric("✅ 已完成", stats['completed_count'])
    st.markdown("---")
    st.markdown("### 🔍 快速查找设备")
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        search_keyword = st.text_input("输入设备名称/型号/序列号/科室", placeholder="例如：监护仪、ICU、CT...")
    with search_col2:
        st.write("")
        st.write("")
        if st.button("🔍 搜索", use_container_width=True):
            pass
    if search_keyword:
        keyword = search_keyword.lower()
        search_results = []
        for d in devices:
            if (keyword in d.get('name', '').lower() or 
                keyword in d.get('model', '').lower() or 
                keyword in d.get('serial_no', '').lower() or
                keyword in d.get('department', '').lower()):
                search_results.append(d)
        if search_results:
            st.success(f"找到 {len(search_results)} 台设备")
            df = pd.DataFrame(search_results)
            display_cols = ['name', 'model', 'serial_no', 'department', 'status', 'price']
            display_cols = [c for c in display_cols if c in df.columns]
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        else:
            st.info("未找到匹配的设备")
    if devices:
        st.markdown("---")
        col1, col2 = st.columns(2)
        df = pd.DataFrame(devices)
        with col1:
            if 'department' in df.columns and not df['department'].isna().all():
                dept_counts = df['department'].value_counts().reset_index()
                dept_counts.columns = ['科室', '数量']
                fig = px.pie(dept_counts, values='数量', names='科室', title='设备科室分布')
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            if 'status' in df.columns and not df['status'].isna().all():
                status_counts = df['status'].value_counts().reset_index()
                status_counts.columns = ['状态', '数量']
                fig = px.bar(status_counts, x='状态', y='数量', title='设备状态统计')
                st.plotly_chart(fig, use_container_width=True)


# ==================== 设备台账 ====================
def device_list_page():
    st.subheader("📋 设备台账管理")
    devices = st.session_state.devices
    st.markdown("### 🔍 搜索与筛选")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_keyword = st.text_input("搜索设备", placeholder="输入名称/型号/序列号/科室...")
    with col2:
        status_filter = st.selectbox("状态筛选", ["全部", "在用", "空闲", "维修中", "报废"])
    with col3:
        st.write("")
        st.write("")
        if st.button("🔄 重置"):
            st.rerun()
    filtered_devices = devices.copy()
    if status_filter != "全部":
        filtered_devices = [d for d in filtered_devices if d.get('status') == status_filter]
    if search_keyword:
        keyword = search_keyword.lower()
        filtered_devices = [
            d for d in filtered_devices
            if keyword in d.get('name', '').lower()
            or keyword in d.get('model', '').lower()
            or keyword in d.get('serial_no', '').lower()
            or keyword in d.get('department', '').lower()
            or keyword in d.get('supplier', '').lower()
        ]
    if not filtered_devices:
        st.info("📭 暂无匹配的设备")
        if devices:
            st.caption(f"共 {len(devices)} 台设备，当前筛选无结果")
        else:
            st.caption("💡 请前往 **设备管理** 页面添加设备")
        return
    df = pd.DataFrame(filtered_devices)
    df['保养状态'] = df['maintenance_date'].apply(lambda x: get_maintenance_status(x)[0] if x else '未知')
    df['保修状态'] = df['warranty_end'].apply(lambda x: get_warranty_status(x)[0] if x else '未知')
    st.caption(f"共找到 {len(filtered_devices)} 台设备")
    display_cols = ['name', 'model', 'serial_no', 'department', 'location', 'status', 'price', 'purchase_date', '保养状态', '保修状态', 'supplier']
    display_cols = [c for c in display_cols if c in df.columns]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 导出CSV"):
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下载", csv, f"设备台账_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    with col2:
        if st.button("📊 导出Excel"):
            excel_data = export_to_excel(df)
            st.download_button("下载", excel_data, f"设备台账_{datetime.now().strftime('%Y%m%d')}.xlsx",
                             "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ==================== 设备管理（自定义资产ID） ====================
def device_manage_page():
    st.subheader("🔧 设备管理")
    tab1, tab2, tab3, tab4 = st.tabs(["➕ 添加设备", "✏️ 编辑设备", "📝 批量操作", "📎 上传资料"])
    with tab1:
        with st.form("add_device_form"):
            col1, col2 = st.columns(2)
            with col1:
                asset_id_input = st.text_input("资产编号/ID（可自定义，留空自动生成）", 
                                               placeholder="例如：SB-2024-001 或 留空自动生成")
                name = st.text_input("设备名称 *")
                model = st.text_input("型号 *")
                serial_no = st.text_input("序列号")
                department = st.selectbox("科室", st.session_state.departments)
                location = st.text_input("存放位置")
            with col2:
                price = st.number_input("采购价格(元)", min_value=0, step=1000)
                purchase_date = st.date_input("采购日期")
                warranty_years = st.number_input("保修年限", min_value=0, max_value=10, value=3)
                supplier = st.text_input("供应商")
                manufacturer = st.text_input("品牌/生产厂家")
            submitted = st.form_submit_button("添加设备")
            if submitted:
                if not name or not model:
                    st.error("请填写设备名称和型号")
                else:
                    if asset_id_input and asset_id_input.strip():
                        device_id = asset_id_input.strip()
                        existing_ids = [d.get('id', '') for d in st.session_state.devices]
                        if device_id in existing_ids:
                            st.error(f"❌ 资产编号 '{device_id}' 已存在，请使用其他编号")
                            st.stop()
                    else:
                        device_id = str(uuid.uuid4())
                    warranty_end = purchase_date + timedelta(days=warranty_years * 365)
                    new_device = {
                        "id": device_id,
                        "name": name,
                        "model": model,
                        "serial_no": serial_no or "未填写",
                        "department": department,
                        "location": location or department,
                        "status": "空闲",
                        "price": price,
                        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                        "warranty_end": warranty_end.strftime("%Y-%m-%d"),
                        "maintenance_date": purchase_date.strftime("%Y-%m-%d"),
                        "maintenance_cycle": 365,
                        "supplier": supplier or "未填写",
                        "manufacturer": manufacturer or "未填写",
                        "contact_phone": "未填写",
                        "remarks": "",
                        "created_by": st.session_state.username,
                        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "files": []
                    }
                    st.session_state.devices.append(new_device)
                    save_data()
                    save_log("添加设备", f"添加设备：{name} (ID:{device_id})")
                    st.success(f"✅ 设备 {name} 添加成功！资产编号：{device_id}")
                    st.rerun()
    with tab2:
        devices = st.session_state.devices
        if not devices:
            st.info("暂无设备可编辑")
        else:
            device_options = {f"{d['name']} - {d['model']} (ID:{d.get('id', '')[:12]})": d['id'] for d in devices}
            selected = st.selectbox("选择要编辑的设备", list(device_options.keys()))
            device_id = device_options[selected]
            device = next(d for d in devices if d['id'] == device_id)
            with st.form("edit_device_form"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text_input("资产编号/ID（不可修改）", value=device.get('id', ''), disabled=True)
                    name = st.text_input("设备名称", value=device['name'])
                    model = st.text_input("型号", value=device['model'])
                    department = st.selectbox("科室", st.session_state.departments,
                                             index=st.session_state.departments.index(device.get('department', 'ICU')) if device.get('department') in st.session_state.departments else 0)
                with col2:
                    price = st.number_input("采购价格(元)", value=float(device.get('price', 0)), step=1000.0)
                    status = st.selectbox("状态", ["在用", "空闲", "维修中", "报废"],
                                         index=["在用", "空闲", "维修中", "报废"].index(device.get('status', '在用')))
                    manufacturer = st.text_input("品牌/生产厂家", value=device.get('manufacturer', ''))
                if st.form_submit_button("保存修改"):
                    device['name'] = name
                    device['model'] = model
                    device['department'] = department
                    device['price'] = price
                    device['status'] = status
                    device['manufacturer'] = manufacturer
                    save_data()
                    save_log("编辑设备", f"编辑设备：{name}")
                    st.success("保存成功！")
                    st.rerun()
    with tab3:
        devices = st.session_state.devices
        if not devices:
            st.info("暂无设备")
            return
        st.subheader("📌 选择要操作的设备")
        device_names = [f"{d['name']} - {d['model']} (ID:{d.get('id','')[:6]})" for d in devices]
        selected_batch = st.multiselect("选择设备（可多选）", device_names)
        if not selected_batch:
            st.info("请至少选择一台设备")
            return
        selected_devices = []
        for label in selected_batch:
            name = label.split(" - ")[0]
            for d in devices:
                if d['name'] == name:
                    selected_devices.append(d)
                    break
        st.info(f"已选择 {len(selected_devices)} 台设备")
        st.markdown("---")
        st.subheader("🛠️ 批量操作")
        batch_action = st.selectbox(
            "选择操作",
            [
                "更新状态",
                "更新科室",
                "更新供应商",
                "更新存放位置",
                "批量删除",
                "导出选中设备"
            ]
        )
        if batch_action == "更新状态":
            new_status = st.selectbox("新状态", ["在用", "空闲", "维修中", "报废"])
            if st.button("确认更新状态"):
                for d in selected_devices:
                    d['status'] = new_status
                save_data()
                save_log("批量更新状态", f"更新 {len(selected_devices)} 台设备状态为 {new_status}")
                st.success(f"✅ 已更新 {len(selected_devices)} 台设备状态")
                st.rerun()
        elif batch_action == "更新科室":
            new_department = st.selectbox("新科室", st.session_state.departments)
            if st.button("确认更新科室"):
                for d in selected_devices:
                    d['department'] = new_department
                    d['location'] = new_department
                save_data()
                save_log("批量更新科室", f"更新 {len(selected_devices)} 台设备科室为 {new_department}")
                st.success(f"✅ 已更新 {len(selected_devices)} 台设备科室")
                st.rerun()
        elif batch_action == "更新供应商":
            new_supplier = st.text_input("新供应商名称")
            if st.button("确认更新供应商"):
                if new_supplier:
                    for d in selected_devices:
                        d['supplier'] = new_supplier
                    save_data()
                    save_log("批量更新供应商", f"更新 {len(selected_devices)} 台设备供应商")
                    st.success(f"✅ 已更新 {len(selected_devices)} 台设备供应商")
                    st.rerun()
                else:
                    st.error("请填写供应商名称")
        elif batch_action == "更新存放位置":
            new_location = st.text_input("新存放位置")
            if st.button("确认更新位置"):
                if new_location:
                    for d in selected_devices:
                        d['location'] = new_location
                    save_data()
                    save_log("批量更新位置", f"更新 {len(selected_devices)} 台设备位置")
                    st.success(f"✅ 已更新 {len(selected_devices)} 台设备位置")
                    st.rerun()
                else:
                    st.error("请填写存放位置")
        elif batch_action == "批量删除":
            confirm = st.checkbox("☑ 我确认要删除这些设备（此操作不可恢复）")
            if st.button("🗑️ 确认批量删除", type="primary"):
                if not confirm:
                    st.error("请先勾选确认删除")
                else:
                    delete_ids = [d['id'] for d in selected_devices]
                    st.session_state.devices = [d for d in devices if d['id'] not in delete_ids]
                    save_data()
                    save_log("批量删除", f"批量删除 {len(delete_ids)} 台设备")
                    st.success(f"✅ 成功删除 {len(delete_ids)} 台设备！当前剩余 {len(st.session_state.devices)} 台")
                    st.rerun()
        elif batch_action == "导出选中设备":
            if st.button("导出为CSV"):
                df = pd.DataFrame(selected_devices)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button("下载CSV", csv, f"设备导出_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
            if st.button("导出为Excel"):
                df = pd.DataFrame(selected_devices)
                excel_data = export_to_excel(df)
                st.download_button("下载Excel", excel_data, f"设备导出_{datetime.now().strftime('%Y%m%d')}.xlsx",
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with tab4:
        st.markdown("### 📎 上传设备资料（说明书、证书、图纸等）")
        devices = st.session_state.devices
        if not devices:
            st.warning("暂无设备，请先添加设备")
            return
        device_options = {f"{d['name']} - {d['model']}": d['id'] for d in devices}
        selected_device = st.selectbox("选择设备", list(device_options.keys()))
        device_id = device_options[selected_device]
        device = next(d for d in devices if d['id'] == device_id)
        uploaded_file = st.file_uploader("选择文件", type=["pdf", "docx", "txt", "jpg", "png", "xlsx", "zip"])
        file_description = st.text_input("文件描述（选填）")
        if st.button("上传文件"):
            if uploaded_file:
                original_name, filepath = save_file(uploaded_file, device_id)
                if 'files' not in device:
                    device['files'] = []
                device['files'].append({
                    "name": original_name,
                    "path": filepath,
                    "description": file_description,
                    "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "uploader": st.session_state.username
                })
                save_data()
                save_log("上传资料", f"为设备 {device['name']} 上传文件 {original_name}")
                st.success("文件上传成功！")
                st.rerun()
            else:
                st.error("请选择文件")
        st.markdown("---")
        st.markdown("### 📄 已上传资料")
        if device.get('files'):
            for f in device['files']:
                col1, col2, col3 = st.columns([4, 2, 1])
                with col1:
                    st.write(f"📄 {f['name']} - {f.get('description', '无描述')}")
                    st.caption(f"上传时间：{f['upload_time']}")
                with col2:
                    if os.path.exists(f['path']):
                        with open(f['path'], "rb") as file:
                            st.download_button("下载", data=file, file_name=f['name'], key=f"dl_{f['name']}")
                with col3:
                    if st.button("删除", key=f"del_{f['name']}"):
                        if os.path.exists(f['path']):
                            os.remove(f['path'])
                        device['files'].remove(f)
                        save_data()
                        st.rerun()
        else:
            st.info("暂无资料")


# ==================== 设备验收 ====================
def acceptance_page():
    st.subheader("📋 设备验收管理")
    with st.form("acceptance_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("设备名称 *")
            model = st.text_input("型号 *")
            serial_no = st.text_input("序列号 *")
            department = st.selectbox("使用科室", st.session_state.departments)
        with col2:
            purchase_date = st.date_input("采购日期")
            price = st.number_input("采购价格(元)", min_value=0, step=1000)
            supplier = st.text_input("供应商")
            manufacturer = st.text_input("品牌/生产厂家")
            warranty_years = st.number_input("保修年限", min_value=1, max_value=10, value=3)
        st.markdown("### 📸 设备照片")
        photo = st.camera_input("拍摄设备照片（选填）")
        if photo:
            st.image(photo, width=200, caption="预览照片")
        st.markdown("### ✅ 验收标准")
        col1, col2 = st.columns(2)
        with col1:
            check1 = st.checkbox("外观完好")
            check2 = st.checkbox("功能正常")
        with col2:
            check3 = st.checkbox("配件齐全")
            check4 = st.checkbox("资料完整")
        if st.form_submit_button("确认验收", type="primary"):
            if name and model and serial_no:
                warranty_end = purchase_date + timedelta(days=warranty_years*365)
                photo_path = ""
                if photo:
                    photo_path = save_photo(photo, f"accept_{serial_no}")
                new_device = {
                    "id": str(uuid.uuid4()),
                    "name": name,
                    "model": model,
                    "serial_no": serial_no,
                    "department": department,
                    "location": department,
                    "status": "在用",
                    "price": price,
                    "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                    "warranty_end": warranty_end.strftime("%Y-%m-%d"),
                    "maintenance_date": purchase_date.strftime("%Y-%m-%d"),
                    "maintenance_cycle": 365,
                    "supplier": supplier or "未填写",
                    "manufacturer": manufacturer or "未填写",
                    "contact_phone": "未填写",
                    "remarks": f"验收人：{st.session_state.users[st.session_state.username]['name']}",
                    "acceptance_date": datetime.now().strftime("%Y-%m-%d"),
                    "acceptance_person": st.session_state.users[st.session_state.username]['name'],
                    "photo_path": photo_path,
                    "created_by": st.session_state.username,
                    "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "files": []
                }
                st.session_state.devices.append(new_device)
                save_data()
                save_log("设备验收", f"验收设备：{name}")
                st.success(f"✅ 设备 {name} 验收成功！")
                st.balloons()
                st.rerun()
            else:
                st.error("请填写完整信息")


# ==================== 资产调拨 ====================
def transfer_page():
    st.subheader("🔄 资产调拨与借用")
    tab1, tab2 = st.tabs(["📝 调拨/借用", "📋 历史记录"])
    with tab1:
        devices = [d for d in st.session_state.devices if d.get('status') != "报废"]
        if not devices:
            st.warning("没有可用设备")
            return
        device_options = {f"{d['name']} - {d['model']} (当前科室：{d.get('department','未分配')})": d['id'] for d in devices}
        selected = st.selectbox("选择设备", list(device_options.keys()))
        device_id = device_options[selected]
        device = next(d for d in devices if d['id'] == device_id)
        op_type = st.radio("操作类型", ["调拨", "借用"])
        with st.form("transfer_form"):
            col1, col2 = st.columns(2)
            with col1:
                if op_type == "调拨":
                    target_dept = st.selectbox("目标科室", [d for d in st.session_state.departments if d != device.get('department')])
                    reason = st.text_area("调拨原因")
                else:
                    borrower = st.text_input("借用人姓名")
                    borrow_date = st.date_input("借用日期")
                    borrow_time = st.time_input("借用时间", value=datetime.now().time())
                    return_date = st.date_input("预计归还日期")
                    return_time = st.time_input("预计归还时间", value=(datetime.now() + timedelta(days=7)).time())
                    reason = st.text_area("借用事由")
                    target_dept = device.get('department')
            submitted = st.form_submit_button("提交")
            if submitted:
                if op_type == "调拨" and not target_dept:
                    st.error("请选择目标科室")
                elif op_type == "借用" and not borrower:
                    st.error("请填写借用人")
                else:
                    record = {
                        "id": str(uuid.uuid4()),
                        "device_id": device['id'],
                        "device_name": device['name'],
                        "from_dept": device.get('department'),
                        "to_dept": target_dept if op_type == "调拨" else device.get('department'),
                        "type": op_type,
                        "borrower": borrower if op_type == "借用" else "",
                        "borrow_date": borrow_date.strftime("%Y-%m-%d") if op_type == "借用" else "",
                        "borrow_time": borrow_time.strftime("%H:%M") if op_type == "借用" else "",
                        "return_date": return_date.strftime("%Y-%m-%d") if op_type == "借用" else "",
                        "return_time": return_time.strftime("%H:%M") if op_type == "借用" else "",
                        "status": "已借出" if op_type == "借用" else "已完成",
                        "reason": reason,
                        "applicant": st.session_state.username,
                        "apply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    if op_type == "调拨":
                        device['department'] = target_dept
                        device['location'] = target_dept
                        save_data()
                    st.session_state.transfer_records.append(record)
                    save_transfer_records()
                    save_log(f"{op_type}操作", f"{op_type} {device['name']}")
                    st.success(f"{op_type}成功！")
                    st.rerun()
        st.markdown("---")
        st.subheader("↩️ 归还借用设备")
        borrowed = [r for r in st.session_state.transfer_records if r.get('type') == '借用' and r.get('status') == '已借出']
        if borrowed:
            for r in borrowed:
                with st.expander(f"{r['device_name']} - 借用人：{r.get('borrower')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"借用时间：{r.get('borrow_date')} {r.get('borrow_time', '')}")
                        st.write(f"预计归还：{r.get('return_date')} {r.get('return_time', '')}")
                    with col2:
                        if st.button(f"确认归还", key=f"return_{r['id']}"):
                            r['status'] = '已归还'
                            for d in st.session_state.devices:
                                if d['id'] == r['device_id']:
                                    d['status'] = "在用"
                            save_data()
                            save_transfer_records()
                            save_log("归还设备", f"归还 {r['device_name']}")
                            st.success("归还成功")
                            st.rerun()
        else:
            st.info("暂无待归还的借用设备")
    with tab2:
        if st.session_state.transfer_records:
            df = pd.DataFrame(st.session_state.transfer_records[::-1])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无记录")


# ==================== 报废处置 ====================
def scrap_page():
    st.subheader("🗑️ 报废与处置管理")
    tab1, tab2 = st.tabs(["📝 报废申请", "📋 报废记录"])
    with tab1:
        devices = [d for d in st.session_state.devices if d.get('status') != "报废"]
        if not devices:
            st.warning("没有可用设备")
            return
        device_options = {f"{d['name']} - {d['model']}": d['id'] for d in devices}
        selected = st.selectbox("选择设备", list(device_options.keys()))
        device_id = device_options[selected]
        device = next(d for d in devices if d['id'] == device_id)
        with st.form("scrap_form"):
            reason = st.selectbox("报废原因", ["达到使用年限", "严重故障", "技术淘汰", "事故损坏", "其他"])
            disposal_method = st.selectbox("处置方式", ["拍卖", "销毁", "捐赠", "返厂", "其他"])
            scrap_date = st.date_input("报废日期")
            scrap_location = st.text_input("报废地点", value="院内")
            disposal_amount = st.number_input("处置收入(元)", min_value=0, step=100, value=0)
            note = st.text_area("备注")
            if st.form_submit_button("确认报废"):
                device['status'] = "报废"
                device['scrap_date'] = scrap_date.strftime("%Y-%m-%d")
                record = {
                    "id": str(uuid.uuid4()),
                    "device_id": device['id'],
                    "device_name": device['name'],
                    "scrap_reason": reason,
                    "disposal_method": disposal_method,
                    "disposal_amount": disposal_amount,
                    "scrap_date": scrap_date.strftime("%Y-%m-%d"),
                    "scrap_location": scrap_location,
                    "note": note,
                    "applicant": st.session_state.username,
                    "apply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.scrap_records.append(record)
                save_data()
                save_scrap_records()
                save_log("设备报废", f"报废设备：{device['name']}")
                st.success("报废成功！")
                st.rerun()
    with tab2:
        if st.session_state.scrap_records:
            df = pd.DataFrame(st.session_state.scrap_records[::-1])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("暂无报废记录")


# ==================== 资产盘点 ====================
def check_page():
    st.subheader("📊 资产盘点")
    tab1, tab2 = st.tabs(["📝 创建盘点", "📋 盘点记录"])
    with tab1:
        if not st.session_state.devices:
            st.warning("暂无设备，请先添加设备")
            return
        st.markdown("### 盘点清单")
        dept_filter = st.multiselect("选择科室（留空表示全部）", st.session_state.departments)
        devices_to_check = [d for d in st.session_state.devices if not dept_filter or d.get('department') in dept_filter]
        if not devices_to_check:
            st.info("没有匹配的设备")
            return
        check_data = []
        for d in devices_to_check:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"{d['name']} - {d['model']} (科室：{d.get('department')})")
            with col2:
                actual_qty = st.number_input("实际数量", min_value=0, step=1, key=f"qty_{d['id']}", value=1)
            with col3:
                st.write(f"系统数量：1")
            check_data.append({
                "device_id": d['id'],
                "device_name": d['name'],
                "department": d.get('department'),
                "system_qty": 1,
                "actual_qty": actual_qty,
                "diff": actual_qty - 1
            })
        if st.button("📋 提交盘点结果"):
            check_no = f"CHK{datetime.now().strftime('%Y%m%d%H%M')}"
            for item in check_data:
                record = {
                    "id": str(uuid.uuid4()),
                    "check_no": check_no,
                    "device_id": item['device_id'],
                    "device_name": item['device_name'],
                    "department": item['department'],
                    "system_qty": item['system_qty'],
                    "actual_qty": item['actual_qty'],
                    "diff": item['diff'],
                    "checker": st.session_state.username,
                    "check_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.check_records.append(record)
                if item['diff'] != 0:
                    save_log("盘点差异", f"设备 {item['device_name']} 系统数量 {item['system_qty']}，实际 {item['actual_qty']}")
            save_check_records()
            st.success(f"盘点完成！共盘点 {len(check_data)} 台设备")
            st.rerun()
    with tab2:
        if st.session_state.check_records:
            df = pd.DataFrame(st.session_state.check_records[::-1])
            st.dataframe(df, use_container_width=True, hide_index=True)
            diff_df = df[df['diff'] != 0]
            if not diff_df.empty:
                st.warning(f"发现 {len(diff_df)} 条差异记录")
                st.dataframe(diff_df[['device_name', 'department', 'system_qty', 'actual_qty', 'diff']], use_container_width=True)
        else:
            st.info("暂无盘点记录")


# ==================== 资产折旧 ====================
def depreciation_page():
    st.subheader("💰 资产折旧")
    devices = st.session_state.devices
    if not devices:
        st.info("暂无设备")
        return
    st.markdown("### 📊 设备折旧明细")
    dep_data = []
    for d in devices:
        rate, monthly, net = calculate_depreciation(d)
        dep_data.append({
            "设备名称": d['name'],
            "型号": d['model'],
            "原值(元)": d.get('price', 0),
            "年折旧率": f"{rate*100:.2f}%",
            "月折旧额(元)": round(monthly, 2),
            "当前净值(元)": round(net, 2),
            "购买日期": d.get('purchase_date')
        })
    df = pd.DataFrame(dep_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.metric("总资产原值", f"¥{df['原值(元)'].sum():,.2f}")
    st.metric("总资产净值", f"¥{df['当前净值(元)'].sum():,.2f}")
    if len(devices) > 0:
        fig = px.bar(df, x='设备名称', y=['原值(元)', '当前净值(元)'], title='资产原值与净值对比', barmode='group')
        st.plotly_chart(fig, use_container_width=True)


# ==================== 资产标签 ====================
def tag_page():
    st.subheader("🏷️ 资产标签（固定资产卡片）")
    devices = st.session_state.devices
    if not devices:
        st.info("暂无设备")
        return
    st.markdown("### ⚙️ 标签设置")
    col_set1, col_set2 = st.columns(2)
    with col_set1:
        hospital_name = st.text_input("医院名称", value="中山大学附属第六医院")
    with col_set2:
        dept_label = st.text_input("科室字段显示名称", value="使用科室")
    st.markdown("---")
    st.markdown("### 🔍 搜索设备")
    search_keyword = st.text_input("输入设备名称/型号/序列号/科室", placeholder="例如：监护仪、CT、ICU...")
    filtered_devices = devices
    if search_keyword:
        keyword = search_keyword.lower()
        filtered_devices = [
            d for d in devices
            if keyword in d.get('name', '').lower()
            or keyword in d.get('model', '').lower()
            or keyword in d.get('serial_no', '').lower()
            or keyword in d.get('department', '').lower()
        ]
        if not filtered_devices:
            st.warning("未找到匹配的设备，请调整搜索条件")
            filtered_devices = devices
    if filtered_devices:
        device_options = {f"{d.get('name', '未知')} - {d.get('model', '未知')} (SN:{d.get('serial_no', '无')})": d for d in filtered_devices}
        selected_label = st.selectbox("选择设备生成标签", list(device_options.keys()))
        device = device_options[selected_label]
    else:
        st.info("没有可用的设备")
        return
    if device:
        device_id = device.get('id', '')
        device_name = device.get('name', '未命名设备')
        serial_no = device.get('serial_no', '无')
        model = device.get('model', '无型号')
        manufacturer = device.get('manufacturer', '未填写')
        supplier = device.get('supplier', '未填写')
        department = device.get('department', '未分配')
        location = device.get('location', department)
        purchase_date = device.get('purchase_date', '未设置')
        if not device_id:
            device_id = "无ID"
        if device_id == "无ID":
            card_no = f"1-{datetime.now().strftime('%Y%m%d')}001"
        else:
            short_id = device_id[-6:] if len(device_id) >= 6 else device_id
            card_no = f"1-{datetime.now().strftime('%Y%m%d')}{short_id}"
        try:
            img_base64, qr_url = generate_device_qr(device_id, device_name)
        except Exception as e:
            st.error(f"二维码生成失败：{e}")
            img_base64 = None
            qr_url = ""
        tag_html = f'''
        <div style="
            width: 440px;
            padding: 15px 20px 20px 20px;
            background: white;
            border: 3px solid #1a3a6b;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            font-family: 'Microsoft YaHei', 'SimSun', Arial, sans-serif;
            margin: 0 auto;
            position: relative;
        ">
            <div style="
                text-align: center;
                padding-bottom: 8px;
                border-bottom: 3px double #1a3a6b;
                margin-bottom: 12px;
            ">
                <div style="
                    font-size: 18px;
                    font-weight: bold;
                    color: #1a3a6b;
                    letter-spacing: 2px;
                ">
                    🏥 {hospital_name}
                </div>
                <div style="
                    font-size: 10px;
                    color: #999;
                    margin-top: 2px;
                    letter-spacing: 1px;
                ">
                    FIXED ASSET LABEL
                </div>
            </div>
            <div style="
                background: #f0f4f8;
                padding: 4px 10px;
                border-radius: 4px;
                margin-bottom: 12px;
                text-align: center;
                font-size: 13px;
                color: #1a3a6b;
                border: 1px dashed #1a3a6b;
            ">
                <strong>卡片编号：</strong>{card_no}
            </div>
            <div style="display: flex; gap: 15px; align-items: stretch;">
                <div style="flex: 1;">
                    <table style="
                        width: 100%;
                        font-size: 13px;
                        border-collapse: collapse;
                        line-height: 1.8;
                    ">
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                width: 70px;
                                white-space: nowrap;
                            ">资产名称</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                                font-weight: bold;
                                border-bottom: 1px solid #eee;
                            ">{device_name}</td>
                        </tr>
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                white-space: nowrap;
                            ">型号</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                                border-bottom: 1px solid #eee;
                            ">{model}</td>
                        </tr>
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                white-space: nowrap;
                            ">供应商</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                                border-bottom: 1px solid #eee;
                            ">{supplier}</td>
                        </tr>
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                white-space: nowrap;
                            ">{dept_label}</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                                font-weight: bold;
                                border-bottom: 1px solid #eee;
                            ">{department}</td>
                        </tr>
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                white-space: nowrap;
                            ">存放地点</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                                border-bottom: 1px solid #eee;
                            ">{location}</td>
                        </tr>
                        <tr>
                            <td style="
                                padding: 3px 8px 3px 0;
                                color: #555;
                                font-weight: bold;
                                white-space: nowrap;
                            ">开始日期</td>
                            <td style="
                                padding: 3px 0;
                                color: #222;
                            ">{purchase_date}</td>
                        </tr>
                    </table>
                </div>
                <div style="
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    min-width: 130px;
                    padding-left: 10px;
                    border-left: 1px solid #eee;
                ">
                    {f'<img src="data:image/png;base64,{img_base64}" style="width: 120px; height: 120px; border: 2px solid #1a3a6b; border-radius: 6px;">' if img_base64 else '<div style="width:120px;height:120px;background:#f0f0f0;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#999;font-size:11px;border:2px solid #ddd;">二维码</div>'}
                    <span style="
                        font-size: 10px; 
                        color: #1a3a6b; 
                        margin-top: 6px;
                        font-weight: bold;
                        letter-spacing: 1px;
                    ">扫码报修</span>
                </div>
            </div>
            <div style="
                margin-top: 12px;
                padding-top: 8px;
                border-top: 1px dashed #ddd;
                text-align: right;
                font-size: 11px;
                color: #999;
            ">
                <span>SN: {serial_no}</span>
                <span style="margin-left: 15px; font-size: 9px; color: #ccc;">系统生成</span>
            </div>
        </div>
        '''
        st.markdown(tag_html, unsafe_allow_html=True)
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if img_base64:
                qr_img = qrcode.make(qr_url)
                buffered = BytesIO()
                qr_img.save(buffered, format="PNG")
                st.download_button(
                    "📥 下载二维码", 
                    data=buffered.getvalue(),
                    file_name=f"QR_{device_name}.png", 
                    mime="image/png"
                )
            else:
                st.warning("二维码生成失败")
        with col2:
            st.download_button(
                "📥 下载标签(HTML)",
                data=tag_html,
                file_name=f"标签_{device_name}.html",
                mime="text/html"
            )
        with col3:
            text_label = f"""
╔════════════════════════════════════════════════╗
║              🏥 {hospital_name}               ║
╠════════════════════════════════════════════════╣
║  卡片编号：{card_no}
║  资产名称：{device_name}
║  型号：{model}
║  供应商：{supplier}
║  {dept_label}：{department}
║  存放地点：{location}
║  开始日期：{purchase_date}
║  SN：{serial_no}
╚════════════════════════════════════════════════╝
            """
            st.download_button(
                "📥 下载标签(文本)",
                data=text_label,
                file_name=f"标签_{device_name}.txt",
                mime="text/plain"
            )
    st.markdown("---")
    st.subheader("📦 批量标签预览")
    if st.button("显示所有设备标签预览"):
        for d in devices[:10]:
            try:
                device_id = d.get('id', '')
                device_name = d.get('name', '未知')
                img_base64, qr_url = generate_device_qr(device_id, device_name)
                st.markdown(f'''
                <div style="
                    display: inline-block;
                    width: 160px;
                    margin: 5px;
                    padding: 8px;
                    background: white;
                    border: 1px solid #1a3a6b;
                    border-radius: 6px;
                    text-align: center;
                    font-size: 10px;
                ">
                    <img src="data:image/png;base64,{img_base64}" style="width: 60px; height: 60px;">
                    <div style="font-weight: bold; margin-top: 4px;">{d.get('name', '')}</div>
                    <div style="color: #666;">{d.get('model', '')}</div>
                    <div style="color: #999; font-size: 8px;">SN:{d.get('serial_no', '')}</div>
                </div>
                ''', unsafe_allow_html=True)
            except:
                pass


# ==================== 手机扫码报修 ====================
def scan_repair_page():
    st.subheader("📱 手机扫码报修")
    device_id = st.query_params.get("device_id", None)
    if device_id:
        device = next((d for d in st.session_state.devices if d['id'] == device_id), None)
        if device:
            st.success(f"✅ 已识别设备：{device['name']} ({device['model']})")
            with st.form("scan_repair_form"):
                st.markdown("### 📋 设备信息")
                st.write(f"**设备名称：** {device['name']}")
                st.write(f"**型号：** {device['model']}")
                st.write(f"**序列号：** {device.get('serial_no', '无')}")
                st.write(f"**科室：** {device.get('department', '未分配')}")
                st.markdown("---")
                st.markdown("### 🔧 故障信息")
                col1, col2 = st.columns(2)
                with col1:
                    urgency = st.selectbox("紧急程度", ["普通", "紧急", "特急"])
                    fault_type = st.selectbox("故障类型", FAULT_TYPES)
                with col2:
                    phone = st.text_input("联系电话")
                description = st.text_area("故障描述", height=80, placeholder="请详细描述故障情况...")
                fault_photo = st.camera_input("拍摄故障照片（选填）")
                if fault_photo:
                    st.image(fault_photo, width=150, caption="预览")
                if st.form_submit_button("🚨 提交报修", type="primary"):
                    if description:
                        repair = {
                            "id": str(uuid.uuid4()),
                            "device_id": device['id'],
                            "device_name": device['name'],
                            "reporter": st.session_state.username,
                            "reporter_name": st.session_state.users[st.session_state.username]['name'],
                            "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "urgency": urgency,
                            "fault_type": fault_type,
                            "description": description,
                            "phone": phone,
                            "status": "待处理",
                            "source": "扫码报修"
                        }
                        st.session_state.repair_records.append(repair)
                        device['status'] = "维修中"
                        save_data()
                        save_repair_records()
                        st.success("✅ 报修成功！工单已创建")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("请填写故障描述")
        else:
            st.error("未找到该设备，请检查二维码是否正确")
    else:
        st.info("📷 请使用手机扫描设备二维码进入报修页面")
        st.caption("或选择下方设备手动报修")
        devices = [d for d in st.session_state.devices if d.get('status') != "报废"]
        if devices:
            device_options = {f"{d['name']} - {d['model']}": d['id'] for d in devices}
            selected = st.selectbox("选择设备", list(device_options.keys()))
            if st.button("进入报修"):
                st.query_params["device_id"] = device_options[selected]
                st.rerun()


# ==================== 维修工单（最新版：含管理员删除权限 + 退回功能 + 操作备注） ====================
def repair_page():
    st.subheader("🚨 维修工单管理")
    if st.session_state.get('quick_repair_mode', False):
        st.session_state.quick_repair_mode = False
        st.success("📱 快速报修模式已开启，请选择设备并填写报修信息")
    
    records = st.session_state.repair_records
    if records:
        total = len(records)
        pending = len([r for r in records if r.get('状态') in ['已提交', '已派单']])
        processing = len([r for r in records if r.get('状态') in ['工程师接单']])
        completed = len([r for r in records if r.get('状态') in ['维修完成', '已关闭']])
        engineer_stats = {}
        for r in records:
            engineer = r.get('处理信息', {}).get('处理人', '未分配')
            if engineer not in engineer_stats:
                engineer_stats[engineer] = 0
            if r.get('状态') in ['维修完成', '已关闭']:
                engineer_stats[engineer] += 1
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 总工单", total)
        with col2:
            st.metric("⏳ 待处理", pending)
        with col3:
            st.metric("🛠️ 处理中", processing)
        with col4:
            st.metric("✅ 已完成", completed)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔧 工程师工作量")
            if engineer_stats:
                eng_df = pd.DataFrame(list(engineer_stats.items()), columns=['工程师', '完成工单数'])
                st.dataframe(eng_df, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("### 📊 故障类型TOP5")
            fault_types = []
            for r in records:
                fault_info = r.get('故障信息', {})
                if fault_info.get('故障类型'):
                    fault_types.extend(fault_info['故障类型'])
            if fault_types:
                top_faults = Counter(fault_types).most_common(5)
                st.dataframe(pd.DataFrame(top_faults, columns=['故障类型', '次数']), use_container_width=True, hide_index=True)
        st.markdown("---")

    tab1, tab2 = st.tabs(["📝 报修申请", "📋 工单列表"])

    with tab1:
        devices = st.session_state.devices
        if not devices:
            st.warning("⚠️ 请先添加设备")
            return
        available_devices = [d for d in devices if d.get('status') != "报废"]
        if not available_devices:
            st.info("暂无可用设备（所有设备已报废）")
            return

        device_options = {f"{d['name']} - {d['model']} (ID:{d.get('id','')[:8]})": d for d in available_devices}
        selected_label = st.selectbox("选择设备", list(device_options.keys()))
        selected_device = device_options[selected_label]
        
        with st.form("repair_form"):
            st.markdown("### 📋 设备信息")
            col1, col2 = st.columns(2)
            with col1:
                asset_id = st.text_input("资产ID", value=selected_device.get('id', ''))
                asset_code = st.text_input("资产编号", value=selected_device.get('serial_no', ''))
                device_name = st.text_input("设备名称", value=selected_device.get('name', ''))
            with col2:
                device_model = st.text_input("设备型号", value=selected_device.get('model', ''))
                location = st.text_input("存放位置", value=selected_device.get('location', selected_device.get('department', '')))
                manufacturer = st.text_input("品牌/生产厂家", value=selected_device.get('manufacturer', ''))
            
            st.markdown("### 📍 报修信息")
            col1, col2 = st.columns(2)
            with col1:
                report_dept = st.selectbox("报修科室 *", st.session_state.departments)
                ward_room = st.text_input("病区/房间号 *", placeholder="例如：住院部A区3楼305室")
                reporter_name = st.text_input("报修人姓名 *", value=st.session_state.users[st.session_state.username]['name'])
            with col2:
                contact_phone = st.text_input("联系电话 *", value="")
                fault_time = st.date_input("故障发生时间", datetime.now())
                region = st.selectbox("所属区域", ["门诊楼", "住院楼", "ICU", "手术室", "急诊科", "检验科", "放射科", "其他"])
            
            st.markdown("---")
            st.markdown("### 🔧 故障信息")
            col1, col2 = st.columns(2)
            with col1:
                fault_types = st.multiselect("故障类型（可多选）", FAULT_TYPES)
                fault_level = st.selectbox("故障等级", FAULT_LEVELS)
            with col2:
                impact_scope = st.multiselect("影响范围（可多选）", IMPACT_SCOPES)
            
            fault_description = st.text_area("故障描述（富文本，支持换行）", height=100, 
                                            placeholder="请详细描述故障情况...")
            
            st.markdown("**故障部位照片（最多9张）**")
            fault_images = st.file_uploader("上传故障照片", type=["jpg", "png", "jpeg"], 
                                           accept_multiple_files=True, key="fault_images_new")
            if fault_images:
                st.caption(f"已上传 {len(fault_images)} 张（最多9张）")
                cols = st.columns(min(len(fault_images), 9))
                for i, img in enumerate(fault_images[:9]):
                    with cols[i]:
                        st.image(img, width=80, caption=f"{i+1}")
                if len(fault_images) > 9:
                    st.warning("最多上传9张，多余的已被忽略")
            
            st.markdown("---")
            st.markdown("### 📝 报修信息")
            col1, col2, col3 = st.columns(3)
            with col1:
                reporter_id = st.text_input("报修人ID", value=st.session_state.username)
            with col2:
                repair_method = st.selectbox("维修方式", REPAIR_METHODS)
            with col3:
                parts_options = {f"{p['name']} - {p['model']} (库存:{p.get('stock',0)}{p.get('unit','')})": p['id'] for p in st.session_state.parts}
                selected_parts = st.multiselect("预估配件（可多选）", list(parts_options.keys()))
                selected_part_ids = [parts_options[p] for p in selected_parts]
            
            submitted = st.form_submit_button("🚨 提交报修", type="primary")
            if submitted:
                if not fault_types:
                    st.error("请至少选择一种故障类型")
                elif not fault_description:
                    st.error("请填写故障描述")
                elif not contact_phone:
                    st.error("请填写联系电话")
                elif not ward_room:
                    st.error("请填写病区/房间号")
                else:
                    image_paths = []
                    for img in fault_images[:9]:
                        path = save_photo(img, f"fault_{selected_device.get('id', '')[:8]}")
                        if path:
                            image_paths.append(path)
                    sla_hours = SLA_MAP.get(fault_level, 48)
                    sla_deadline = datetime.now() + timedelta(hours=sla_hours)
                    ticket_no = generate_repair_no()
                    repair_record = {
                        "id": str(uuid.uuid4()),
                        "工单号": ticket_no,
                        "状态": "已提交",
                        "状态流转": [
                            {
                                "状态": "已提交",
                                "操作人": reporter_name,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": "提交报修申请"
                            }
                        ],
                        "设备信息": {
                            "资产ID": asset_id,
                            "资产编号": asset_code,
                            "设备名称": device_name,
                            "设备型号": device_model,
                            "存放位置": location,
                            "生产厂家": manufacturer,
                            "所属区域": region
                        },
                        "报修信息": {
                            "报修科室": report_dept,
                            "病区/房间号": ward_room,
                            "报修人姓名": reporter_name,
                            "报修人ID": reporter_id,
                            "联系电话": contact_phone,
                            "故障发生时间": fault_time.strftime("%Y-%m-%d"),
                            "维修方式": repair_method,
                            "预估配件ID": selected_part_ids
                        },
                        "故障信息": {
                            "故障类型": fault_types,
                            "故障等级": fault_level,
                            "故障描述": fault_description,
                            "故障图片": image_paths,
                            "影响范围": impact_scope
                        },
                        "系统字段": {
                            "提交时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "SLA截止时间": sla_deadline.strftime("%Y-%m-%d %H:%M:%S"),
                            "SLA状态": "正常"
                        },
                        "处理信息": {
                            "处理人": "",
                            "处理时间": "",
                            "处理结果": "",
                            "维修费用": 0,
                            "修复图片": [],
                            "维修前照片": [],
                            "维修中照片": [],
                            "维修后照片": [],
                            "配件清单": [],
                            "耗材清单": [],
                            "故障原因分析": "",
                            "处理措施": "",
                            "备件清单": []
                        }
                    }
                    st.session_state.repair_records.append(repair_record)
                    for d in st.session_state.devices:
                        if d.get('id') == selected_device.get('id'):
                            d['status'] = "维修中"
                    save_data()
                    save_repair_records()
                    save_log("提交报修", f"报修工单：{ticket_no} - {device_name}")
                    st.success(f"✅ 报修成功！工单号：{ticket_no}")
                    st.balloons()
                    st.rerun()

    with tab2:
        st.markdown("### 📋 工单列表")
        col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
        with col1:
            search_keyword = st.text_input("🔍 搜索工单", placeholder="工单号/设备名称/报修人...")
        with col2:
            status_filter = st.selectbox("状态筛选", ["全部"] + REPAIR_STATUSES)
        with col3:
            level_filter = st.selectbox("等级筛选", ["全部"] + FAULT_LEVELS)
        with col4:
            if st.button("🔄 刷新"):
                st.rerun()
        repair_records = st.session_state.repair_records
        if not repair_records:
            st.info("暂无工单记录")
            return
        filtered = repair_records.copy()
        if status_filter != "全部":
            filtered = [r for r in filtered if r.get('状态') == status_filter]
        if level_filter != "全部":
            filtered = [r for r in filtered if r.get('故障信息', {}).get('故障等级') == level_filter]
        if search_keyword:
            kw = search_keyword.lower()
            filtered = [
                r for r in filtered
                if kw in r.get('工单号', '').lower()
                or kw in r.get('设备信息', {}).get('设备名称', '').lower()
                or kw in r.get('报修信息', {}).get('报修人姓名', '').lower()
                or kw in r.get('故障信息', {}).get('故障描述', '').lower()
            ]
        st.caption(f"共找到 {len(filtered)} 条工单")
        if not filtered:
            st.info("未找到匹配的工单")
            return
        table_data = []
        for r in filtered:
            device_info = r.get('设备信息', {})
            fault_info = r.get('故障信息', {})
            repair_info = r.get('报修信息', {})
            table_data.append({
                "工单号": r.get('工单号', ''),
                "设备名称": device_info.get('设备名称', ''),
                "故障类型": ", ".join(fault_info.get('故障类型', [])),
                "故障等级": fault_info.get('故障等级', ''),
                "状态": r.get('状态', ''),
                "报修人": repair_info.get('报修人姓名', ''),
                "提交时间": r.get('系统字段', {}).get('提交时间', ''),
            })
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
        st.markdown("---")
        st.subheader("🔧 工单操作")
        
        for r in filtered:
            device_info = r.get('设备信息', {})
            fault_info = r.get('故障信息', {})
            repair_info = r.get('报修信息', {})
            sys_info = r.get('系统字段', {})
            process_info = r.get('处理信息', {})
            
            with st.expander(f"📋 {r.get('工单号', '')} - {device_info.get('设备名称', '')} ({fault_info.get('故障等级', '')})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**设备名称：** {device_info.get('设备名称', '')}")
                    st.write(f"**资产编号：** {device_info.get('资产编号', '')}")
                    st.write(f"**设备型号：** {device_info.get('设备型号', '')}")
                    st.write(f"**存放位置：** {device_info.get('存放位置', '')}")
                    st.write(f"**生产厂家：** {device_info.get('生产厂家', '')}")
                    st.write(f"**所属区域：** {device_info.get('所属区域', '')}")
                    st.write(f"**报修科室：** {repair_info.get('报修科室', '')}")
                    st.write(f"**病区/房间号：** {repair_info.get('病区/房间号', '')}")
                    st.write(f"**故障类型：** {', '.join(fault_info.get('故障类型', []))}")
                    st.write(f"**故障等级：** {fault_info.get('故障等级', '')}")
                    st.write(f"**影响范围：** {', '.join(fault_info.get('影响范围', []))}")
                    st.write(f"**维修方式：** {repair_info.get('维修方式', '')}")
                    st.write(f"**故障发生时间：** {repair_info.get('故障发生时间', '')}")
                with col2:
                    st.write(f"**报修人：** {repair_info.get('报修人姓名', '')}")
                    st.write(f"**联系电话：** {repair_info.get('联系电话', '')}")
                    st.write(f"**提交时间：** {sys_info.get('提交时间', '')}")
                    st.write(f"**SLA截止：** {sys_info.get('SLA截止时间', '')}")
                    st.write(f"**当前状态：** {r.get('状态', '')}")
                    if fault_info.get('故障图片'):
                        st.write("**故障图片：**")
                        for img_path in fault_info['故障图片'][:3]:
                            if os.path.exists(img_path):
                                st.image(img_path, width=100)
                    st.write("**状态流转历史：**")
                    for log in r.get('状态流转', []):
                        st.write(f"- {log.get('状态')} | {log.get('操作人')} | {log.get('操作时间')} | {log.get('备注', '')}")
                st.write(f"**故障描述：** {fault_info.get('故障描述', '')}")
                
                if process_info.get('处理结果'):
                    st.write(f"**处理结果：** {process_info.get('处理结果', '')}")
                    st.write(f"**维修费用：** ¥{process_info.get('维修费用', 0)}")
                    if process_info.get('修复图片'):
                        st.write("**修复图片：**")
                        for img_path in process_info['修复图片']:
                            if os.path.exists(img_path):
                                st.image(img_path, width=100)
                if process_info.get('配件清单'):
                    st.write("**更换配件清单：**")
                    for part in process_info['配件清单']:
                        st.write(f"- {part.get('名称')} x{part.get('数量')} ({part.get('型号')}) 旧件去向：{part.get('旧件去向')}")
                
                # ===== 操作备注（可填写） =====
                remark_key = f"op_remark_{r['id']}"
                st.text_area(
                    "📝 操作备注（选填）",
                    key=remark_key,
                    placeholder="请输入本次操作说明，将记录到状态流转历史...",
                    height=68
                )
                st.markdown("---")
                st.markdown("#### 操作")
                current_status = r.get('状态', '')
                engineer_options = sorted([u for u in st.session_state.users.keys() if st.session_state.users[u]['role'] in ['repair', 'admin', 'manager']])
                if not engineer_options:
                    engineer_options = ["暂无可用工程师"]
                
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                is_admin = st.session_state.role == "admin"
                
                if current_status == "已提交":
                    assigned_to = st.selectbox("指派给", engineer_options, key=f"assign_to_{r['id']}")
                    with col_btn1:
                        if st.button("📤 派单", key=f"dispatch_{r['id']}"):
                            if not assigned_to or assigned_to == "暂无可用工程师":
                                st.error("❌ 请选择指派的工程师")
                            else:
                                r['状态'] = "已派单"
                                r['处理信息']['处理人'] = assigned_to
                                remark = st.session_state.get(remark_key, "")
                                r['状态流转'].append({
                                    "状态": "已派单",
                                    "操作人": st.session_state.username,
                                    "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "备注": f"指派给 {assigned_to}。备注：{remark}" if remark else f"指派给 {assigned_to}"
                                })
                                save_repair_records()
                                st.success(f"✅ 已派单给 **{assigned_to}**！")
                                st.rerun()
                    if is_admin:
                        with col_btn4:
                            with st.popover("🗑️ 删除工单", use_container_width=True):
                                st.warning("⚠️ 删除后将无法恢复，且设备状态将恢复为'在用'")
                                confirm_del = st.checkbox("我确认删除此工单", key=f"confirm_del_{r['id']}")
                                if st.button("确认删除", key=f"del_confirm_{r['id']}"):
                                    if confirm_del:
                                        for d in st.session_state.devices:
                                            if d['id'] == r['设备信息']['资产ID']:
                                                d['status'] = "在用"
                                        st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                                        save_data()
                                        save_repair_records()
                                        st.success("工单已删除")
                                        st.rerun()
                                    else:
                                        st.error("请先勾选确认")
                
                elif current_status == "已派单":
                    st.markdown("### 📋 工单摘要")
                    col_sum1, col_sum2 = st.columns(2)
                    with col_sum1:
                        st.write(f"**设备名称：** {device_info.get('设备名称', '')}")
                        st.write(f"**设备型号：** {device_info.get('设备型号', '')}")
                        st.write(f"**故障类型：** {', '.join(fault_info.get('故障类型', []))}")
                    with col_sum2:
                        st.write(f"**故障等级：** {fault_info.get('故障等级', '')}")
                        st.write(f"**报修科室：** {repair_info.get('报修科室', '')}")
                        st.write(f"**指派工程师：** {r.get('处理信息', {}).get('处理人', '未指派')}")
                    st.write(f"**故障描述：** {fault_info.get('故障描述', '')[:100]}...")
                    
                    with col_btn1:
                        if st.button("✅ 接单", key=f"accept_{r['id']}"):
                            r['状态'] = "工程师接单"
                            r['处理信息']['处理人'] = st.session_state.username
                            remark = st.session_state.get(remark_key, "")
                            r['状态流转'].append({
                                "状态": "工程师接单",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": f"工程师 {st.session_state.username} 已接单。备注：{remark}" if remark else f"工程师 {st.session_state.username} 已接单"
                            })
                            save_repair_records()
                            st.success("✅ 接单成功！请填写维修记录")
                            st.rerun()
                    with col_btn2:
                        with st.popover("🔄 改派", use_container_width=True):
                            new_engineer = st.selectbox("改派给", engineer_options, key=f"reassign_{r['id']}")
                            reason = st.text_area("改派原因", key=f"reason_{r['id']}")
                            if st.button("确认改派", key=f"confirm_reassign_{r['id']}"):
                                if new_engineer and new_engineer != "暂无可用工程师" and reason:
                                    old_engineer = r.get('处理信息', {}).get('处理人', '未指派')
                                    r['状态'] = "已派单"
                                    r['处理信息']['处理人'] = new_engineer
                                    r['状态流转'].append({
                                        "状态": "已派单",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"改派给 {new_engineer}，原因：{reason}"
                                    })
                                    save_repair_records()
                                    st.success(f"✅ 已改派给 {new_engineer}")
                                    st.rerun()
                                else:
                                    st.error("请填写工程师和改派原因")
                    with col_btn3:
                        with st.popover("⏪ 退回", use_container_width=True):
                            st.warning("退回后工单将回到'已提交'状态，可重新派单。")
                            confirm_back = st.checkbox("我确认退回此工单", key=f"confirm_back_{r['id']}")
                            if st.button("确认退回", key=f"back_confirm_{r['id']}"):
                                if confirm_back:
                                    r['状态'] = "已提交"
                                    r['处理信息']['处理人'] = ""
                                    remark = st.session_state.get(remark_key, "")
                                    r['状态流转'].append({
                                        "状态": "已提交",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"退回至已提交。备注：{remark}" if remark else "退回至已提交"
                                    })
                                    save_repair_records()
                                    st.success("工单已退回至'已提交'状态")
                                    st.rerun()
                                else:
                                    st.error("请先勾选确认")
                    if is_admin:
                        with col_btn4:
                            with st.popover("🗑️ 删除工单", use_container_width=True):
                                st.warning("⚠️ 删除后将无法恢复，且设备状态将恢复为'在用'")
                                confirm_del = st.checkbox("我确认删除此工单", key=f"confirm_del_{r['id']}")
                                if st.button("确认删除", key=f"del_confirm_{r['id']}"):
                                    if confirm_del:
                                        for d in st.session_state.devices:
                                            if d['id'] == r['设备信息']['资产ID']:
                                                d['status'] = "在用"
                                        st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                                        save_data()
                                        save_repair_records()
                                        st.success("工单已删除")
                                        st.rerun()
                                    else:
                                        st.error("请先勾选确认")
                
                elif current_status == "工程师接单":
                    st.success("✅ 您已接单，请填写维修记录")
                    
                    col_back_del1, col_back_del2 = st.columns(2)
                    with col_back_del1:
                        with st.popover("⏪ 退回", use_container_width=True):
                            st.warning("退回后工单将回到'已派单'状态，可重新指派或接单。")
                            confirm_back = st.checkbox("我确认退回此工单", key=f"confirm_back_{r['id']}")
                            if st.button("确认退回", key=f"back_confirm_{r['id']}"):
                                if confirm_back:
                                    r['状态'] = "已派单"
                                    remark = st.session_state.get(remark_key, "")
                                    r['状态流转'].append({
                                        "状态": "已派单",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"退回至已派单。备注：{remark}" if remark else "退回至已派单"
                                    })
                                    save_repair_records()
                                    st.success("工单已退回至'已派单'状态")
                                    st.rerun()
                                else:
                                    st.error("请先勾选确认")
                    if is_admin:
                        with col_back_del2:
                            with st.popover("🗑️ 删除工单", use_container_width=True):
                                st.warning("⚠️ 删除后将无法恢复，且设备状态将恢复为'在用'")
                                confirm_del = st.checkbox("我确认删除此工单", key=f"confirm_del_{r['id']}")
                                if st.button("确认删除", key=f"del_confirm_{r['id']}"):
                                    if confirm_del:
                                        for d in st.session_state.devices:
                                            if d['id'] == r['设备信息']['资产ID']:
                                                d['status'] = "在用"
                                        st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                                        save_data()
                                        save_repair_records()
                                        st.success("工单已删除")
                                        st.rerun()
                                    else:
                                        st.error("请先勾选确认")
                    
                    st.markdown("---")
                    st.markdown("## 📋 维修记录单")
                    
                    with st.form(key=f"repair_form_{r['id']}"):
                        st.markdown(f"**No.** {r.get('工单号', '')}")
                        st.markdown("---")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.text_input("科室名称", value=repair_info.get('报修科室', ''), disabled=True)
                        with col2:
                            st.text_input("设备名称", value=device_info.get('设备名称', ''), disabled=True)
                        with col3:
                            system_no = st.text_input("系统编号", value="", placeholder="请输入")
                        with col4:
                            qr_code = st.text_input("二维码编号", value="", placeholder="请输入")
                        with col5:
                            st.text_input("设备厂家", value=device_info.get('生产厂家', ''), disabled=True)
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.text_input("派工单号", value=r.get('工单号', ''), disabled=True)
                        with col2:
                            st.text_input("设备型号", value=device_info.get('设备型号', ''), disabled=True)
                        with col3:
                            st.text_input("序列号", value=device_info.get('资产编号', ''), disabled=True)
                        with col4:
                            st.text_input("设备编号", value=device_info.get('资产ID', '')[:12], disabled=True)
                        with col5:
                            production_date = st.text_input("生产日期", value="", placeholder="例如：2021.3.1")
                        
                        st.markdown("---")
                        
                        col1, col2, col3 = st.columns([1, 2, 2])
                        with col1:
                            st.markdown("**服务类型**")
                            st.text_input("", value="自修", disabled=True, key=f"service_type_{r['id']}")
                        with col2:
                            st.markdown("**设备状态**")
                            device_status = st.radio(
                                "",
                                ["正常使用", "完全停机", "局部使用"],
                                horizontal=True,
                                key=f"device_status_{r['id']}"
                            )
                        with col3:
                            st.markdown("**故障或服务原因**")
                            fault_reason = st.text_input("", value=fault_info.get('故障描述', '')[:50], key=f"fault_reason_{r['id']}")
                        
                        st.markdown("---")
                        
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            report_time = st.text_input("报修时间", value=sys_info.get('提交时间', '').split()[0] if sys_info.get('提交时间') else "", disabled=True)
                        with col2:
                            arrive_time = st.date_input("到达时间", value=datetime.now().date(), key=f"arrive_time_{r['id']}")
                        with col3:
                            work_date = st.date_input("日期", value=datetime.now().date(), key=f"work_date_{r['id']}")
                        with col4:
                            start_time = st.time_input("开始时间", value=datetime.now().time(), key=f"start_time_{r['id']}")
                        with col5:
                            end_time = st.time_input("结束时间", value=datetime.now().time(), key=f"end_time_{r['id']}")
                        
                        st.markdown("---")
                        
                        st.markdown("**服务内容**")
                        service_content = st.text_area(
                            "",
                            height=80,
                            placeholder="请详细描述维修服务内容...",
                            key=f"service_content_{r['id']}"
                        )
                        
                        st.markdown("---")
                        
                        st.markdown("**备件使用记录**")
                        part_rows = st.number_input(
                            "备件行数",
                            min_value=1,
                            max_value=20,
                            step=1,
                            value=st.session_state.get(f"part_rows_{r['id']}", 1),
                            key=f"part_rows_num_{r['id']}"
                        )
                        st.session_state[f"part_rows_{r['id']}"] = part_rows
                        
                        part_data = []
                        for i in range(part_rows):
                            col1, col2, col3, col4, col5 = st.columns([1.5, 2, 1.5, 1, 2])
                            with col1:
                                part_no = st.text_input("备件号", key=f"part_no_{r['id']}_{i}")
                            with col2:
                                part_name = st.text_input("备件名称", key=f"part_name_{r['id']}_{i}")
                            with col3:
                                part_sn = st.text_input("序列号", key=f"part_sn_{r['id']}_{i}")
                            with col4:
                                part_qty = st.number_input("数量", min_value=0, step=1, key=f"part_qty_{r['id']}_{i}", value=0)
                            with col5:
                                part_note = st.text_input("备注", key=f"part_note_{r['id']}_{i}")
                            if part_no or part_name:
                                part_data.append({
                                    "备件号": part_no,
                                    "备件名称": part_name,
                                    "序列号": part_sn,
                                    "数量": part_qty,
                                    "备注": part_note
                                })
                        
                        st.markdown("---")
                        
                        st.markdown("**服务结果及建议**")
                        service_result = st.text_area(
                            "",
                            height=60,
                            placeholder="请描述服务结果及建议...",
                            key=f"service_result_{r['id']}"
                        )
                        
                        st.markdown("---")
                        
                        submitted_repair = st.form_submit_button("✅ 提交维修记录", type="primary")
                        
                        if submitted_repair:
                            if not service_content and not service_result:
                                st.error("请至少填写服务内容或服务结果")
                            else:
                                r['状态'] = "维修完成"
                                r['处理信息']['处理结果'] = service_result
                                r['处理信息']['服务内容'] = service_content
                                r['处理信息']['设备状态'] = device_status
                                r['处理信息']['故障原因'] = fault_reason
                                r['处理信息']['到达时间'] = arrive_time.strftime("%Y-%m-%d")
                                r['处理信息']['工作日期'] = work_date.strftime("%Y-%m-%d")
                                r['处理信息']['开始时间'] = start_time.strftime("%H:%M")
                                r['处理信息']['结束时间'] = end_time.strftime("%H:%M")
                                r['处理信息']['生产日期'] = production_date
                                r['处理信息']['系统编号'] = system_no
                                r['处理信息']['二维码编号'] = qr_code
                                r['处理信息']['备件清单'] = part_data
                                r['处理信息']['完成时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                r['状态流转'].append({
                                    "状态": "维修完成",
                                    "操作人": st.session_state.username,
                                    "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "备注": "维修完成，已提交记录"
                                })
                                for d in st.session_state.devices:
                                    if d['id'] == r['设备信息']['资产ID']:
                                        d['status'] = "在用"
                                save_data()
                                save_repair_records()
                                st.success("✅ 维修记录已提交，工单已完成！")
                                st.balloons()
                                st.rerun()
                
                elif current_status == "维修完成":
                    with col_btn1:
                        if st.button("🔒 关闭工单", key=f"close_{r['id']}"):
                            r['状态'] = "已关闭"
                            remark = st.session_state.get(remark_key, "")
                            r['状态流转'].append({
                                "状态": "已关闭",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": f"工单已关闭。备注：{remark}" if remark else "工单已关闭"
                            })
                            save_repair_records()
                            st.success("工单已关闭")
                            st.rerun()
                    with col_btn2:
                        with st.popover("⏪ 退回", use_container_width=True):
                            st.warning("退回后工单将回到'工程师接单'状态，可重新填写维修记录。")
                            confirm_back = st.checkbox("我确认退回此工单", key=f"confirm_back_{r['id']}")
                            if st.button("确认退回", key=f"back_confirm_{r['id']}"):
                                if confirm_back:
                                    r['状态'] = "工程师接单"
                                    remark = st.session_state.get(remark_key, "")
                                    r['状态流转'].append({
                                        "状态": "工程师接单",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"退回至工程师接单。备注：{remark}" if remark else "退回至工程师接单"
                                    })
                                    save_repair_records()
                                    st.success("工单已退回至'工程师接单'状态")
                                    st.rerun()
                                else:
                                    st.error("请先勾选确认")
                    if is_admin:
                        with col_btn4:
                            with st.popover("🗑️ 删除工单", use_container_width=True):
                                st.warning("⚠️ 删除后将无法恢复")
                                confirm_del = st.checkbox("我确认删除此工单", key=f"confirm_del_{r['id']}")
                                if st.button("确认删除", key=f"del_confirm_{r['id']}"):
                                    if confirm_del:
                                        st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                                        save_repair_records()
                                        st.success("工单已删除")
                                        st.rerun()
                                    else:
                                        st.error("请先勾选确认")
                
                elif current_status == "已关闭":
                    with col_btn1:
                        with st.popover("⏪ 退回", use_container_width=True):
                            st.warning("退回后工单将回到'维修完成'状态，可重新关闭或修改。")
                            confirm_back = st.checkbox("我确认退回此工单", key=f"confirm_back_{r['id']}")
                            if st.button("确认退回", key=f"back_confirm_{r['id']}"):
                                if confirm_back:
                                    r['状态'] = "维修完成"
                                    remark = st.session_state.get(remark_key, "")
                                    r['状态流转'].append({
                                        "状态": "维修完成",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"退回至维修完成。备注：{remark}" if remark else "退回至维修完成"
                                    })
                                    save_repair_records()
                                    st.success("工单已退回至'维修完成'状态")
                                    st.rerun()
                                else:
                                    st.error("请先勾选确认")
                    if is_admin:
                        with col_btn4:
                            with st.popover("🗑️ 删除工单", use_container_width=True):
                                st.warning("⚠️ 删除后将无法恢复")
                                confirm_del = st.checkbox("我确认删除此工单", key=f"confirm_del_{r['id']}")
                                if st.button("确认删除", key=f"del_confirm_{r['id']}"):
                                    if confirm_del:
                                        st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                                        save_repair_records()
                                        st.success("工单已删除")
                                        st.rerun()
                                    else:
                                        st.error("请先勾选确认")


# ==================== 保养计划 ====================
def maintenance_page():
    st.subheader("📅 设备保养计划")
    if st.session_state.get('show_maintenance_reminder', False):
        st.session_state.show_maintenance_reminder = False
        overdue_devices = []
        expiring_devices = []
        for d in st.session_state.devices:
            status, icon = get_maintenance_status(d.get('maintenance_date', ''))
            if status == "逾期":
                overdue_devices.append(d['name'])
            elif status == "即将到期":
                expiring_devices.append(d['name'])
        if overdue_devices:
            st.error(f"🚨 **保养逾期提醒**：以下设备保养已逾期，请立即处理！\n\n{', '.join(overdue_devices)}")
        if expiring_devices:
            st.warning(f"⚠️ **保养即将到期提醒**：以下设备保养即将到期，请尽快安排保养！\n\n{', '.join(expiring_devices)}")
        if not overdue_devices and not expiring_devices:
            st.success("✅ 所有设备保养状态正常")
    st.markdown("### 📌 今日保养任务")
    devices = st.session_state.devices
    today = datetime.now().date()
    today_tasks = []
    if devices:
        for d in devices:
            maint_date_str = d.get('maintenance_date', '')
            if maint_date_str and maint_date_str != '未设置':
                try:
                    maint_date = datetime.strptime(maint_date_str, "%Y-%m-%d").date()
                    cycle = d.get('maintenance_cycle', 365)
                    next_date = maint_date + timedelta(days=cycle)
                    if next_date <= today + timedelta(days=7):
                        days_left = (next_date - today).days
                        days_left_display = f"{days_left}天后" if days_left > 0 else "逾期"
                        today_tasks.append({
                            "设备名称": d['name'],
                            "科室": d.get('department', '未分配'),
                            "上次保养": maint_date_str,
                            "下次保养": next_date.strftime("%Y-%m-%d"),
                            "状态": "🔴 已逾期" if days_left < 0 else f"🟡 {days_left_display}",
                            "device_id": d['id']
                        })
                except:
                    pass
    if today_tasks:
        df_tasks = pd.DataFrame(today_tasks)
        dept_filter = st.selectbox("选择科室查看今日任务", ["全部"] + st.session_state.departments, key="today_dept_filter")
        if dept_filter != "全部":
            df_tasks = df_tasks[df_tasks['科室'] == dept_filter]
        st.dataframe(df_tasks[['设备名称', '科室', '上次保养', '下次保养', '状态']], 
                    use_container_width=True, hide_index=True)
        st.markdown("---")
        st.subheader("✅ 执行保养")
        task_options = {f"{row['设备名称']} - {row['科室']}": row['device_id'] for _, row in df_tasks.iterrows()}
        if task_options:
            selected_task = st.selectbox("选择设备执行保养", list(task_options.keys()))
            with st.form("execute_maintenance_form"):
                col1, col2 = st.columns(2)
                with col1:
                    maint_date = st.date_input("保养日期", today)
                    maint_type = st.selectbox("保养类型", ["日常检查", "定期保养", "年度大修"])
                with col2:
                    tech_person = st.text_input("保养人员")
                    cost = st.number_input("保养费用(元)", min_value=0, step=100)
                if st.form_submit_button("✅ 确认执行保养"):
                    device_id = task_options[selected_task]
                    for d in st.session_state.devices:
                        if d['id'] == device_id:
                            d['maintenance_date'] = maint_date.strftime("%Y-%m-%d")
                            break
                    maint_record = {
                        "id": str(uuid.uuid4()),
                        "device_id": device_id,
                        "device_name": selected_task.split(" - ")[0],
                        "department": next((d.get('department', '') for d in devices if d['id'] == device_id), ''),
                        "maint_date": maint_date.strftime("%Y-%m-%d"),
                        "maint_type": maint_type,
                        "next_maint_date": (maint_date + timedelta(days=365)).strftime("%Y-%m-%d"),
                        "cost": cost,
                        "tech_person": tech_person,
                        "created_by": st.session_state.username,
                        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "is_daily": True
                    }
                    st.session_state.maintenance_records.append(maint_record)
                    save_data()
                    save_maintenance_records()
                    save_log("执行保养", f"保养：{selected_task}")
                    st.success("✅ 保养执行成功！")
                    st.rerun()
    else:
        st.success("✅ 所有设备保养状态正常，暂无今日保养任务")
    st.markdown("---")
    st.markdown("### 🏥 科室保养总览")
    if devices:
        dept_status = {}
        for d in devices:
            dept = d.get('department', '未分配')
            if dept not in dept_status:
                dept_status[dept] = {"total": 0, "正常": 0, "即将到期": 0, "逾期": 0, "今日任务": 0}
            dept_status[dept]["total"] += 1
            status, _ = get_maintenance_status(d.get('maintenance_date', ''))
            if status in dept_status[dept]:
                dept_status[dept][status] += 1
        for task in today_tasks:
            dept = task.get('科室', '未分配')
            if dept in dept_status:
                dept_status[dept]["今日任务"] += 1
        dept_df = []
        for dept, data in dept_status.items():
            completed = data.get('正常', 0) + data.get('即将到期', 0)
            completion_rate = (completed / data["total"] * 100) if data["total"] > 0 else 0
            if data.get('逾期', 0) > 0:
                status_icon = "🔴"
                status_text = "有逾期"
            elif data.get('今日任务', 0) > 0:
                status_icon = "🟡"
                status_text = f"{data.get('今日任务', 0)}项待保养"
            elif completion_rate < 100:
                status_icon = "🟡"
                status_text = "部分完成"
            else:
                status_icon = "🟢"
                status_text = "全部完成"
            dept_df.append({
                "科室": dept,
                "设备总数": data["total"],
                "✅ 正常": data.get('正常', 0),
                "🟡 即将到期": data.get('即将到期', 0),
                "🔴 逾期": data.get('逾期', 0),
                "📌 今日任务": data.get('今日任务', 0),
                "完成率": f"{completion_rate:.0f}%",
                "状态": f"{status_icon} {status_text}"
            })
        st.dataframe(pd.DataFrame(dept_df), use_container_width=True, hide_index=True)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            chart_df = pd.DataFrame(dept_df)
            fig = px.bar(chart_df, x='科室', y=['设备总数', '🔴 逾期', '📌 今日任务'], 
                        title='各科室设备状态统计', barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(chart_df, values='设备总数', names='科室', title='各科室设备占比')
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无设备数据")
    st.markdown("---")
    st.markdown("### 📊 设备保养状态")
    if st.session_state.devices:
        devices = st.session_state.devices
        status_data = []
        for d in devices:
            status, icon = get_maintenance_status(d.get('maintenance_date', ''))
            status_data.append({
                "设备名称": d['name'],
                "科室": d.get('department', '未分配'),
                "保养日期": d.get('maintenance_date', '未设置'),
                "保养状态": f"{icon} {status}"
            })
        st.dataframe(pd.DataFrame(status_data), use_container_width=True, hide_index=True)
    else:
        st.info("暂无设备")
    st.markdown("---")
    devices = st.session_state.devices
    if not devices:
        st.warning("⚠️ 请先添加设备")
        return
    with st.expander("➕ 新增保养记录", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            dept_filter = st.selectbox("选择科室", ["全部"] + st.session_state.departments, key="add_maintenance_dept")
            device_options = {f"{d['name']} - {d['model']}": d['id'] for d in devices}
            if dept_filter != "全部":
                device_options = {f"{d['name']} - {d['model']}": d['id'] for d in devices if d.get('department') == dept_filter}
            selected = st.selectbox("选择设备", list(device_options.keys()))
        with col2:
            maint_date = st.date_input("保养日期")
            maint_type = st.selectbox("保养类型", ["日常检查", "定期保养", "年度大修"])
            tech_person = st.text_input("保养人员")
        col1, col2 = st.columns(2)
        with col1:
            next_maint = st.date_input("下次保养日期")
        with col2:
            cost = st.number_input("保养费用(元)", min_value=0, step=100)
        if st.button("保存保养记录"):
            if selected:
                device_id = device_options[selected]
                for d in st.session_state.devices:
                    if d['id'] == device_id:
                        d['maintenance_date'] = maint_date.strftime("%Y-%m-%d")
                maint_record = {
                    "id": str(uuid.uuid4()),
                    "device_id": device_id,
                    "device_name": selected,
                    "department": next((d.get('department', '') for d in devices if d['id'] == device_id), ''),
                    "maint_date": maint_date.strftime("%Y-%m-%d"),
                    "maint_type": maint_type,
                    "next_maint_date": next_maint.strftime("%Y-%m-%d"),
                    "cost": cost,
                    "tech_person": tech_person,
                    "created_by": st.session_state.username,
                    "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.maintenance_records.append(maint_record)
                save_data()
                save_maintenance_records()
                save_log("添加保养", f"保养：{selected}")
                st.success("保养记录已保存")
                st.rerun()
    st.markdown("---")
    st.markdown("### 📋 保养记录")
    if st.session_state.maintenance_records:
        df = pd.DataFrame(st.session_state.maintenance_records[::-1])
        dept_filter = st.selectbox("筛选科室", ["全部"] + st.session_state.departments, key="filter_maintenance")
        if dept_filter != "全部":
            df = df[df['department'] == dept_filter]
        st.dataframe(df[['device_name', 'department', 'maint_date', 'maint_type', 'next_maint_date', 'tech_person']], 
                    use_container_width=True, hide_index=True)
        st.markdown("---")
        st.subheader("🗑️ 删除保养记录")
        if not df.empty:
            record_options = {f"{row['device_name']} - {row['maint_date']}": idx for idx, row in df.iterrows()}
            selected_delete = st.selectbox("选择要删除的保养记录", list(record_options.keys()))
            if st.button("删除保养记录", key="delete_maintenance"):
                idx = record_options[selected_delete]
                del st.session_state.maintenance_records[idx]
                save_maintenance_records()
                st.success("保养记录已删除")
                st.rerun()
        else:
            st.info("暂无保养记录可删除")
    else:
        st.info("暂无保养记录")


# ==================== 统计分析 ====================
def statistics_page():
    st.subheader("📊 数据统计分析")
    col_refresh, _ = st.columns([1, 5])
    with col_refresh:
        if st.button("🔄 刷新数据"):
            st.session_state.devices = load_data()
            st.session_state.repair_records = load_repair_records()
            st.session_state.maintenance_records = load_maintenance_records()
            st.session_state.contracts = load_contracts()
            st.session_state.transfer_records = load_transfer_records()
            st.session_state.scrap_records = load_scrap_records()
            st.session_state.check_records = load_check_records()
            st.rerun()
    st.caption(f"数据更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    tab1, tab2, tab3 = st.tabs(["📊 设备统计", "💰 维修成本", "📈 保养统计"])
    with tab1:
        devices = st.session_state.devices
        if devices:
            df = pd.DataFrame(devices)
            col1, col2 = st.columns(2)
            with col1:
                if 'department' in df.columns and not df['department'].isna().all():
                    dept_counts = df['department'].value_counts().reset_index()
                    dept_counts.columns = ['科室', '数量']
                    fig = px.bar(dept_counts, x='科室', y='数量', title='各科室设备数量')
                    st.plotly_chart(fig, use_container_width=True)
            with col2:
                if 'status' in df.columns and not df['status'].isna().all():
                    status_counts = df['status'].value_counts().reset_index()
                    status_counts.columns = ['状态', '数量']
                    fig = px.pie(status_counts, values='数量', names='状态', title='设备状态分布')
                    st.plotly_chart(fig, use_container_width=True)
            col1, col2 = st.columns(2)
            with col1:
                st.metric("总设备数", len(df))
            with col2:
                st.metric("总资产", f"¥{df['price'].sum():,.0f}")
            st.markdown("---")
            st.markdown("### 🔥 设备故障率统计（TOP10）")
            fault_data = get_device_fault_rate()
            if fault_data:
                st.dataframe(pd.DataFrame(fault_data), use_container_width=True, hide_index=True)
            st.markdown("---")
            st.markdown("### 📥 批量导出维修报表")
            if st.button("生成维修报表"):
                records = st.session_state.repair_records
                if records:
                    report_data = []
                    for r in records:
                        report_data.append({
                            "工单号": r.get('工单号', ''),
                            "设备名称": r.get('设备信息', {}).get('设备名称', ''),
                            "科室": r.get('报修信息', {}).get('报修科室', ''),
                            "报修人": r.get('报修信息', {}).get('报修人姓名', ''),
                            "故障类型": ", ".join(r.get('故障信息', {}).get('故障类型', [])),
                            "故障等级": r.get('故障信息', {}).get('故障等级', ''),
                            "状态": r.get('状态', ''),
                            "提交时间": r.get('系统字段', {}).get('提交时间', ''),
                            "完成时间": r.get('处理信息', {}).get('完成时间', ''),
                            "维修费用": r.get('处理信息', {}).get('维修费用', 0)
                        })
                    df_report = pd.DataFrame(report_data)
                    csv = df_report.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button("📥 下载CSV报表", data=csv, 
                                       file_name=f"维修报表_{datetime.now().strftime('%Y%m%d')}.csv", 
                                       mime="text/csv")
                    st.success(f"共导出 {len(report_data)} 条记录")
                else:
                    st.warning("暂无维修数据")
        else:
            st.info("暂无设备数据")
    with tab2:
        repair_data = st.session_state.repair_records
        if repair_data:
            cost_data = []
            for r in repair_data:
                fault_info = r.get('故障信息', {})
                fault_type = fault_info.get('故障类型', ['其他'])[0] if fault_info.get('故障类型') else '其他'
                cost_map = {"硬件故障": 1500, "软件问题": 500, "网络故障": 400, "电源故障": 300, 
                           "传感器故障": 800, "显示屏故障": 1000, "按键/面板故障": 600, "连接线缆故障": 200,
                           "机械故障": 1200, "耗材问题": 100, "校准问题": 500, "系统崩溃": 300,
                           "数据异常": 200, "其他": 500}
                cost_data.append({
                    "故障类型": fault_type,
                    "估算成本": cost_map.get(fault_type, 500),
                    "状态": r.get('状态', '未知')
                })
            df = pd.DataFrame(cost_data)
            if not df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.pie(df, values='估算成本', names='故障类型', title='维修成本分布')
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    status_counts = df['状态'].value_counts().reset_index()
                    status_counts.columns = ['状态', '数量']
                    fig = px.bar(status_counts, x='状态', y='数量', title='工单状态分布')
                    st.plotly_chart(fig, use_container_width=True)
                st.metric("总维修成本", f"¥{df['估算成本'].sum():,.0f}")
                st.metric("总工单数", len(df))
            else:
                st.info("暂无维修数据")
        else:
            st.info("暂无维修数据")
    with tab3:
        if st.session_state.maintenance_records:
            df = pd.DataFrame(st.session_state.maintenance_records)
            if 'maint_date' in df.columns:
                df['maint_date'] = pd.to_datetime(df['maint_date'])
                monthly = df.groupby(df['maint_date'].dt.strftime('%Y-%m')).size().reset_index()
                monthly.columns = ['月份', '数量']
                fig = px.bar(monthly, x='月份', y='数量', title='月度保养统计')
                st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df[['device_name', 'maint_date', 'maint_type', 'cost']], use_container_width=True, hide_index=True)
        else:
            st.info("暂无保养数据")


# ==================== 合同管理 ====================
def contract_page():
    st.subheader("📄 合同管理")
    tab1, tab2 = st.tabs(["📋 合同列表", "➕ 添加合同"])
    with tab1:
        if st.session_state.contracts:
            df = pd.DataFrame(st.session_state.contracts)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown("---")
            st.subheader("🗑️ 删除合同")
            contract_options = {f"{c.get('contract_no', '')} - {c.get('device_name', '')}": idx 
                               for idx, c in enumerate(st.session_state.contracts)}
            if contract_options:
                selected_delete = st.selectbox("选择要删除的合同", list(contract_options.keys()))
                confirm_delete = st.checkbox("我确认删除此合同")
                if st.button("🗑️ 确认删除", key="delete_contract_btn"):
                    if not confirm_delete:
                        st.error("请先勾选确认删除")
                    else:
                        idx = contract_options[selected_delete]
                        deleted_name = st.session_state.contracts[idx].get('contract_no', '')
                        if 'file_path' in st.session_state.contracts[idx] and os.path.exists(st.session_state.contracts[idx]['file_path']):
                            os.remove(st.session_state.contracts[idx]['file_path'])
                        del st.session_state.contracts[idx]
                        save_contracts()
                        save_log("删除合同", f"删除合同：{deleted_name}")
                        st.success(f"✅ 合同 {deleted_name} 删除成功")
                        st.rerun()
            else:
                st.info("暂无合同可删除")
        else:
            st.info("暂无合同")
    with tab2:
        with st.form("add_contract_form"):
            col1, col2 = st.columns(2)
            with col1:
                contract_no = st.text_input("合同编号 *")
                device_name = st.text_input("设备名称 *")
                supplier = st.text_input("供应商 *")
            with col2:
                quantity = st.number_input("数量", min_value=1, value=1)
                unit_price = st.number_input("单价(元)", min_value=0)
                sign_date = st.date_input("签订日期")
            status = st.selectbox("状态", ["执行中", "已完成", "已终止"])
            st.markdown("### 📸 合同资料拍照/上传")
            contract_photo = st.camera_input("拍摄合同照片/文档（选填）")
            contract_file = st.file_uploader("或上传合同文件（PDF/图片）", type=["pdf", "jpg", "png", "jpeg", "docx"])
            if contract_photo:
                st.image(contract_photo, width=200, caption="预览")
            if contract_file:
                st.success(f"已选择文件：{contract_file.name}")
            if st.form_submit_button("添加合同"):
                if contract_no and device_name and supplier:
                    file_path = ""
                    if contract_photo:
                        file_path = save_photo(contract_photo, f"contract_{contract_no}")
                    elif contract_file:
                        file_path = save_file(contract_file, f"contract_{contract_no}")[1]
                    new_contract = {
                        "id": str(uuid.uuid4()),
                        "contract_no": contract_no,
                        "device_name": device_name,
                        "supplier": supplier,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "total_amount": quantity * unit_price,
                        "sign_date": sign_date.strftime("%Y-%m-%d"),
                        "status": status,
                        "file_path": file_path,
                        "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.contracts.append(new_contract)
                    save_contracts()
                    save_log("添加合同", f"添加合同：{contract_no}")
                    st.success("合同添加成功")
                    st.rerun()
                else:
                    st.error("请填写完整信息")


# ==================== 用户管理 ====================
def user_management_page():
    st.subheader("👥 用户管理")
    exclude_users = ["manager", "repair1", "nurse1"]
    user_list = []
    for username, info in st.session_state.users.items():
        if username in exclude_users:
            continue
        role_display = {"admin": "管理员", "manager": "经理", "repair": "维修工程师", "user": "普通用户"}.get(info['role'], info['role'])
        user_list.append({"用户名": username, "姓名": info.get('name', ''), "角色": role_display})
    if user_list:
        st.dataframe(pd.DataFrame(user_list), use_container_width=True, hide_index=True)
    else:
        st.info("暂无其他用户")
    st.markdown("---")
    st.subheader("🔑 修改密码")
    with st.form("change_password_form"):
        user_options = [u for u in st.session_state.users.keys() if u not in exclude_users]
        if user_options:
            target_user = st.selectbox("选择要修改密码的用户", user_options)
            new_password = st.text_input("新密码", type="password")
            confirm_password = st.text_input("确认新密码", type="password")
            if st.form_submit_button("修改密码"):
                if not new_password:
                    st.error("请输入新密码")
                elif new_password != confirm_password:
                    st.error("两次输入的密码不一致")
                else:
                    st.session_state.users[target_user]["password"] = hash_password(new_password)
                    save_users()
                    save_log("修改密码", f"修改用户 {target_user} 的密码")
                    st.success(f"✅ 用户 {target_user} 的密码已修改")
                    st.rerun()
        else:
            st.info("没有可修改密码的用户")
    st.markdown("---")
    st.subheader("➕ 添加用户")
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
        with col2:
            role = st.selectbox("角色", ["admin", "manager", "repair", "user"])
            name = st.text_input("姓名")
        if st.form_submit_button("创建用户"):
            if username and username not in st.session_state.users:
                st.session_state.users[username] = {
                    "password": hash_password(password),
                    "role": role,
                    "name": name or username
                }
                save_users()
                save_log("添加用户", f"添加用户：{username}")
                st.success(f"用户 {username} 创建成功")
                st.rerun()
            else:
                st.error("用户名已存在或为空")


# ==================== 操作日志 ====================
def log_page():
    st.subheader("📜 操作日志")
    if st.session_state.operation_log:
        df = pd.DataFrame(st.session_state.operation_log[::-1])
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)
        if st.button("导出日志"):
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下载", csv, f"operation_log_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("暂无操作记录")


# ==================== 系统设置 ====================
def settings_page():
    st.subheader("⚙️ 系统设置")
    tab1, tab2 = st.tabs(["🏥 科室管理", "💾 数据管理"])
    with tab1:
        col1, col2 = st.columns([3, 1])
        with col1:
            new_dept = st.text_input("新科室名称")
        with col2:
            if st.button("添加科室"):
                if new_dept and new_dept not in st.session_state.departments:
                    st.session_state.departments.append(new_dept)
                    save_departments()
                    st.rerun()
        for dept in st.session_state.departments:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"- {dept}")
            with col2:
                if st.button("删除", key=f"del_{dept}"):
                    if dept not in ["ICU", "急诊科", "放射科"]:
                        st.session_state.departments.remove(dept)
                        save_departments()
                        st.rerun()
    with tab2:
        if st.session_state.role == "admin":
            if st.button("🗑️ 清空所有设备数据"):
                st.session_state.devices = []
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("所有设备数据已清空！")
                st.rerun()
            if st.button("💾 备份所有数据"):
                save_data()
                save_users()
                save_repair_records()
                save_maintenance_records()
                save_contracts()
                save_transfer_records()
                save_scrap_records()
                save_check_records()
                save_departments()
                save_parts()
                save_knowledge()
                st.success("所有数据已备份")
        else:
            st.warning("⚠️ 只有管理员可以操作数据管理，请联系管理员")


# ==================== 主程序 ====================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        menu = render_sidebar()
        if st.session_state.get('target_menu'):
            menu = st.session_state.target_menu
        if menu == "📊 仪表板":
            dashboard_page()
        elif menu == "📋 设备台账":
            device_list_page()
        elif menu == "🔧 设备管理":
            device_manage_page()
        elif menu == "📋 设备验收":
            acceptance_page()
        elif menu == "🔄 资产调拨":
            transfer_page()
        elif menu == "🗑️ 报废处置":
            scrap_page()
        elif menu == "📊 资产盘点":
            check_page()
        elif menu == "💰 资产折旧":
            depreciation_page()
        elif menu == "🏷️ 资产标签":
            tag_page()
        elif menu == "📱 扫码报修":
            scan_repair_page()
        elif menu == "🚨 维修工单":
            repair_page()
        elif menu == "📅 保养计划":
            maintenance_page()
        elif menu == "📊 统计分析":
            statistics_page()
        elif menu == "📄 合同管理":
            contract_page()
        elif menu == "⚙️ 系统设置":
            settings_page()
        elif menu == "👥 用户管理":
            user_management_page()
        elif menu == "📜 操作日志":
            log_page()
        if st.session_state.get('target_menu'):
            st.session_state.target_menu = None


if __name__ == "__main__":
    main()
