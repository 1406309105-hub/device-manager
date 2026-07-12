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
    "已提交", "已派单", "工程师接单", "上门检修中", "维修完成", "已关闭"
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
    # 修复 KeyError: 检查列是否存在
    if '状态' not in df.columns:
        return {
            'pending_count': 0,
            'processing_count': 0,
            'completed_count': 0,
            'urgent_count': 0,
            'total': len(df)
        }
    pending = df[df['状态'].isin(['已提交', '已派单'])]
    processing = df[df['状态'].isin(['工程师接单', '上门检修中'])]
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
    # ==================== 维修工单 ====================
def repair_page():
    st.subheader("🚨 维修工单管理")
    if st.session_state.get('quick_repair_mode', False):
        st.session_state.quick_repair_mode = False
        st.success("📱 快速报修模式已开启，请选择设备并填写报修信息")
    
    records = st.session_state.repair_records
    if records:
        total = len(records)
        pending = len([r for r in records if r.get('状态') in ['已提交', '已派单']])
        processing = len([r for r in records if r.get('状态') in ['工程师接单', '上门检修中']])
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
        st.markdown("### ⚡ 快捷报修模板")
        template_cols = st.columns(4)
        templates = [
            {"名称": "监护仪黑屏", "类型": "硬件故障", "描述": "设备开机后屏幕无显示，电源指示灯亮"},
            {"名称": "呼吸机报警", "类型": "硬件故障", "描述": "设备持续发出报警声，显示压力异常"},
            {"名称": "CT扫描失败", "类型": "软件问题", "描述": "扫描过程中中断，报错代码E-1024"},
            {"名称": "除颤仪无法充电", "类型": "电源故障", "描述": "设备插电后电池无充电指示"}
        ]
        for i, t in enumerate(templates):
            with template_cols[i]:
                if st.button(t["名称"], key=f"template_{i}", use_container_width=True):
                    st.session_state.template_fault_type = t["类型"]
                    st.session_state.template_description = t["描述"]
                    st.rerun()
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
                if st.session_state.template_fault_type:
                    fault_types = st.multiselect("故障类型（可多选）", FAULT_TYPES, default=[st.session_state.template_fault_type])
                    st.session_state.template_fault_type = None
                else:
                    fault_types = st.multiselect("故障类型（可多选）", FAULT_TYPES)
                fault_level = st.selectbox("故障等级", FAULT_LEVELS)
            with col2:
                impact_scope = st.multiselect("影响范围（可多选）", IMPACT_SCOPES)
            if st.session_state.template_description:
                fault_description = st.text_area("故障描述（富文本，支持换行）", height=100, 
                                                value=st.session_state.template_description,
                                                placeholder="请详细描述故障情况...")
                st.session_state.template_description = None
            else:
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
                            "处理措施": ""
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
            
            # 用 expander 展开工单
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
                
                # 知识库推荐
                fault_desc = fault_info.get('故障描述', '')
                if fault_desc and r.get('状态') not in ['维修完成', '已关闭']:
                    st.markdown("### 📚 知识库推荐")
                    keywords = fault_desc.split()[:3]
                    matched_kb = []
                    for k in st.session_state.knowledge_base:
                        for kw in keywords:
                            if kw in k['title'] or kw in k['content']:
                                matched_kb.append(k)
                                break
                    if matched_kb:
                        st.caption(f"找到 {len(matched_kb)} 条相关维修方案")
                        for kb in matched_kb[:2]:
                            with st.expander(f"📖 {kb['title']}"):
                                st.write(kb['content'])
                                if st.button("使用此方案", key=f"use_kb_{kb['id']}_{r.get('id','')}"):
                                    st.success("已应用方案到处理结果")
                
                # 历史故障推荐
                device_model = device_info.get('设备型号', '')
                if device_model and r.get('状态') not in ['维修完成', '已关闭']:
                    similar_records = [rec for rec in st.session_state.repair_records 
                                       if rec.get('设备信息', {}).get('设备型号') == device_model 
                                       and rec.get('状态') in ['维修完成', '已关闭']
                                       and rec.get('工单号') != r.get('工单号')]
                    if similar_records:
                        st.markdown("### 💡 同型号历史方案")
                        for sr in similar_records[-2:]:
                            with st.expander(f"📋 {sr.get('工单号')} - {sr.get('故障信息', {}).get('故障等级', '')}级"):
                                st.write(f"**故障现象：** {sr.get('故障信息', {}).get('故障描述', '')[:80]}...")
                                st.write(f"**处理方案：** {sr.get('处理信息', {}).get('处理结果', '暂无')}")
                
                # ===== 操作按钮 =====
                st.markdown("---")
                st.markdown("#### 操作")
                current_status = r.get('状态', '')
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                
                if current_status == "已提交":
                    with col_btn1:
                        if st.button("📤 派单", key=f"dispatch_{r['id']}"):
                            r['状态'] = "已派单"
                            r['状态流转'].append({
                                "状态": "已派单",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": "已派单"
                            })
                            save_repair_records()
                            st.success("✅ 已派单！")
                            st.rerun()
                    with col_btn2:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            for d in st.session_state.devices:
                                if d['id'] == r['设备信息']['资产ID']:
                                    d['status'] = "在用"
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_data()
                            save_repair_records()
                            st.success("工单已删除")
                            st.rerun()
                
                elif current_status == "已派单":
                    with col_btn1:
                        if st.button("✅ 接单", key=f"accept_{r['id']}"):
                            r['状态'] = "工程师接单"
                            r['处理信息']['处理人'] = st.session_state.username
                            r['状态流转'].append({
                                "状态": "工程师接单",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": f"工程师 {st.session_state.username} 接单"
                            })
                            save_repair_records()
                            st.success("✅ 已接单！")
                            st.rerun()
                    with col_btn2:
                        with st.popover("🔄 改派"):
                            new_engineer = st.text_input("改派工程师", key=f"reassign_{r['id']}")
                            reason = st.text_area("改派原因", key=f"reason_{r['id']}")
                            if st.button("确认改派", key=f"confirm_reassign_{r['id']}"):
                                if new_engineer and reason:
                                    r['状态'] = "已派单"
                                    r['状态流转'].append({
                                        "状态": "已派单",
                                        "操作人": st.session_state.username,
                                        "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                        "备注": f"改派给 {new_engineer}，原因：{reason}"
                                    })
                                    save_repair_records()
                                    st.success(f"已改派给 {new_engineer}")
                                    st.rerun()
                                else:
                                    st.error("请填写工程师和改派原因")
                    with col_btn3:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            for d in st.session_state.devices:
                                if d['id'] == r['设备信息']['资产ID']:
                                    d['status'] = "在用"
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_data()
                            save_repair_records()
                            st.rerun()
                
                elif current_status == "工程师接单":
                    # 显示维修执行表单
                    st.markdown("### 🔧 维修执行")
                    with st.form(key=f"repair_exec_form_{r['id']}"):
                        st.markdown("**📸 维修照片**")
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            before_photos = st.file_uploader("维修前", type=["jpg","png"], accept_multiple_files=True, key=f"before_{r['id']}")
                        with c2:
                            during_photos = st.file_uploader("维修中", type=["jpg","png"], accept_multiple_files=True, key=f"during_{r['id']}")
                        with c3:
                            after_photos = st.file_uploader("维修后", type=["jpg","png"], accept_multiple_files=True, key=f"after_{r['id']}")
                        
                        st.markdown("**🔩 配件登记**")
                        col_p1, col_p2, col_p3 = st.columns(3)
                        with col_p1:
                            part_name = st.text_input("配件名称", key=f"pname_{r['id']}")
                            part_qty = st.number_input("数量", min_value=1, value=1, key=f"pqty_{r['id']}")
                        with col_p2:
                            part_model = st.text_input("配件编号/型号", key=f"pmodel_{r['id']}")
                            part_unit = st.selectbox("单位", ["个", "根", "片", "套", "块"], key=f"punit_{r['id']}")
                        with col_p3:
                            old_part_status = st.selectbox("旧件去向", ["报废", "回收", "返厂"], key=f"pstatus_{r['id']}")
                        if st.button("登记配件", key=f"add_part_{r['id']}"):
                            if part_name:
                                if '配件清单' not in r['处理信息']:
                                    r['处理信息']['配件清单'] = []
                                r['处理信息']['配件清单'].append({
                                    "名称": part_name,
                                    "型号": part_model,
                                    "数量": part_qty,
                                    "单位": part_unit,
                                    "旧件去向": old_part_status,
                                    "登记人": st.session_state.username,
                                    "登记时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                save_repair_records()
                                st.success("配件已登记")
                                st.rerun()
                        
                        fault_reason = st.text_input("故障原因分析", key=f"freason_{r['id']}")
                        measures = st.text_area("处理措施描述", key=f"measures_{r['id']}", placeholder="请描述具体处理措施")
                        repair_cost = st.number_input("维修费用(元)", min_value=0, step=10, key=f"cost_{r['id']}")
                        
                        submitted_repair = st.form_submit_button("✅ 提交维修记录并完成工单")
                        if submitted_repair:
                            if not measures:
                                st.error("请填写处理措施描述")
                            else:
                                img_paths_before = [save_photo(img, f"before_{r['id'][:8]}") for img in before_photos[:5] if img]
                                img_paths_during = [save_photo(img, f"during_{r['id'][:8]}") for img in during_photos[:5] if img]
                                img_paths_after = [save_photo(img, f"after_{r['id'][:8]}") for img in after_photos[:5] if img]
                                r['状态'] = "维修完成"
                                r['处理信息']['维修前照片'] = img_paths_before
                                r['处理信息']['维修中照片'] = img_paths_during
                                r['处理信息']['维修后照片'] = img_paths_after
                                r['处理信息']['维修费用'] = repair_cost
                                r['处理信息']['处理结果'] = measures
                                r['处理信息']['故障原因分析'] = fault_reason
                                r['处理信息']['处理措施'] = measures
                                r['处理信息']['完成时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                r['状态流转'].append({
                                    "状态": "维修完成",
                                    "操作人": st.session_state.username,
                                    "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "备注": f"维修完成，费用：{repair_cost}"
                                })
                                for d in st.session_state.devices:
                                    if d['id'] == r['设备信息']['资产ID']:
                                        d['status'] = "在用"
                                save_data()
                                save_repair_records()
                                st.success("维修记录已提交，工单已完成！")
                                st.rerun()
                    
                    with col_btn1:
                        if st.button("🚗 上门检修", key=f"visit_{r['id']}"):
                            r['状态'] = "上门检修中"
                            r['状态流转'].append({
                                "状态": "上门检修中",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": "工程师已出发"
                            })
                            save_repair_records()
                            st.rerun()
                    with col_btn2:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            for d in st.session_state.devices:
                                if d['id'] == r['设备信息']['资产ID']:
                                    d['status'] = "在用"
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_data()
                            save_repair_records()
                            st.rerun()
                
                elif current_status == "上门检修中":
                    # 同样显示维修执行表单
                    st.markdown("### 🔧 维修执行")
                    with st.form(key=f"repair_exec_form2_{r['id']}"):
                        st.markdown("**📸 维修照片**")
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            before_photos = st.file_uploader("维修前", type=["jpg","png"], accept_multiple_files=True, key=f"before2_{r['id']}")
                        with c2:
                            during_photos = st.file_uploader("维修中", type=["jpg","png"], accept_multiple_files=True, key=f"during2_{r['id']}")
                        with c3:
                            after_photos = st.file_uploader("维修后", type=["jpg","png"], accept_multiple_files=True, key=f"after2_{r['id']}")
                        
                        st.markdown("**🔩 配件登记**")
                        col_p1, col_p2, col_p3 = st.columns(3)
                        with col_p1:
                            part_name = st.text_input("配件名称", key=f"pname2_{r['id']}")
                            part_qty = st.number_input("数量", min_value=1, value=1, key=f"pqty2_{r['id']}")
                        with col_p2:
                            part_model = st.text_input("配件编号/型号", key=f"pmodel2_{r['id']}")
                            part_unit = st.selectbox("单位", ["个", "根", "片", "套", "块"], key=f"punit2_{r['id']}")
                        with col_p3:
                            old_part_status = st.selectbox("旧件去向", ["报废", "回收", "返厂"], key=f"pstatus2_{r['id']}")
                        if st.button("登记配件", key=f"add_part2_{r['id']}"):
                            if part_name:
                                if '配件清单' not in r['处理信息']:
                                    r['处理信息']['配件清单'] = []
                                r['处理信息']['配件清单'].append({
                                    "名称": part_name,
                                    "型号": part_model,
                                    "数量": part_qty,
                                    "单位": part_unit,
                                    "旧件去向": old_part_status,
                                    "登记人": st.session_state.username,
                                    "登记时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                save_repair_records()
                                st.success("配件已登记")
                                st.rerun()
                        
                        fault_reason = st.text_input("故障原因分析", key=f"freason2_{r['id']}")
                        measures = st.text_area("处理措施描述", key=f"measures2_{r['id']}", placeholder="请描述具体处理措施")
                        repair_cost = st.number_input("维修费用(元)", min_value=0, step=10, key=f"cost2_{r['id']}")
                        
                        submitted_repair2 = st.form_submit_button("✅ 提交维修记录并完成工单")
                        if submitted_repair2:
                            if not measures:
                                st.error("请填写处理措施描述")
                            else:
                                img_paths_before = [save_photo(img, f"before_{r['id'][:8]}") for img in before_photos[:5] if img]
                                img_paths_during = [save_photo(img, f"during_{r['id'][:8]}") for img in during_photos[:5] if img]
                                img_paths_after = [save_photo(img, f"after_{r['id'][:8]}") for img in after_photos[:5] if img]
                                r['状态'] = "维修完成"
                                r['处理信息']['维修前照片'] = img_paths_before
                                r['处理信息']['维修中照片'] = img_paths_during
                                r['处理信息']['维修后照片'] = img_paths_after
                                r['处理信息']['维修费用'] = repair_cost
                                r['处理信息']['处理结果'] = measures
                                r['处理信息']['故障原因分析'] = fault_reason
                                r['处理信息']['处理措施'] = measures
                                r['处理信息']['完成时间'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                r['状态流转'].append({
                                    "状态": "维修完成",
                                    "操作人": st.session_state.username,
                                    "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                    "备注": f"维修完成，费用：{repair_cost}"
                                })
                                for d in st.session_state.devices:
                                    if d['id'] == r['设备信息']['资产ID']:
                                        d['status'] = "在用"
                                save_data()
                                save_repair_records()
                                st.success("维修记录已提交，工单已完成！")
                                st.rerun()
                    with col_btn1:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            for d in st.session_state.devices:
                                if d['id'] == r['设备信息']['资产ID']:
                                    d['status'] = "在用"
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_data()
                            save_repair_records()
                            st.rerun()
                
                elif current_status == "维修完成":
                    with col_btn1:
                        if st.button("🔒 关闭工单", key=f"close_{r['id']}"):
                            r['状态'] = "已关闭"
                            r['状态流转'].append({
                                "状态": "已关闭",
                                "操作人": st.session_state.username,
                                "操作时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "备注": "工单已关闭"
                            })
                            save_repair_records()
                            st.success("工单已关闭")
                            st.rerun()
                    with col_btn2:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_repair_records()
                            st.rerun()
                
                elif current_status == "已关闭":
                    with col_btn1:
                        if st.button("🗑️ 删除", key=f"del_{r['id']}"):
                            st.session_state.repair_records = [rec for rec in st.session_state.repair_records if rec['id'] != r['id']]
                            save_repair_records()
                            st.rerun()


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
