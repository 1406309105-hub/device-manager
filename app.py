import streamlit as st
import pandas as pd
import uuid
import json
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import hashlib
from io import BytesIO
import base64

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="医疗设备全生命周期管理系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== 自定义CSS样式 ====================
st.markdown("""
<style>
    /* 主标题样式 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    /* 卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    /* 侧边栏样式 */
    .sidebar-header {
        text-align: center;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 数据文件路径 ====================
DATA_FILE = "devices_data.json"
USERS_FILE = "users.json"
REPAIR_FILE = "repair_records.json"
MAINTENANCE_FILE = "maintenance_records.json"
LOG_FILE = "operation_log.json"
DEPARTMENT_FILE = "departments.json"

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

def save_log(operation, details):
    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": st.session_state.get('username', 'unknown'),
        "role": st.session_state.get('role', 'unknown'),
        "operation": operation,
        "details": details,
        "ip": st.request.headers.get('X-Forwarded-For', '127.0.0.1') if hasattr(st, 'request') else 'local'
    }
    if 'operation_log' not in st.session_state:
        st.session_state.operation_log = []
    st.session_state.operation_log.append(log_entry)
    # 只保留最近1000条记录
    if len(st.session_state.operation_log) > 1000:
        st.session_state.operation_log = st.session_state.operation_log[-1000:]
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.operation_log, f, ensure_ascii=False, indent=2)

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ==================== 辅助函数 ====================
def calculate_depreciation(price, purchase_date, years=5):
    """计算设备折旧价值（直线法）"""
    if not price or not purchase_date:
        return None
    purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
    months_used = (datetime.now() - purchase).days / 30.44
    depreciation_rate = min(months_used / (years * 12), 1)
    current_value = price * (1 - depreciation_rate)
    return max(0, current_value)

def get_maintenance_status(maintenance_date):
    """获取保养状态"""
    if not maintenance_date:
        return "未知", "⚪"
    maint = datetime.strptime(maintenance_date, "%Y-%m-%d")
    days_since = (datetime.now() - maint).days
    if days_since > 365:
        return "逾期", "🔴"
    elif days_since > 330:
        return "即将到期", "🟡"
    else:
        return "正常", "🟢"

def get_warranty_status(warranty_end):
    """获取保修状态"""
    if not warranty_end:
        return "未知", "⚪"
    end = datetime.strptime(warranty_end, "%Y-%m-%d")
    days_left = (end - datetime.now()).days
    if days_left < 0:
        return "已过期", "🔴"
    elif days_left < 30:
        return "即将过期", "🟡"
    else:
        return "有效", "🟢"

def export_to_excel(data):
    """导出数据到Excel"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='设备台账')
    return output.getvalue()
# ==================== 初始化数据 ====================
# 初始化设备数据
if 'devices' not in st.session_state:
    st.session_state.devices = load_data()
    if not st.session_state.devices:
        st.session_state.devices = [
            {
                "id": str(uuid.uuid4()),
                "name": "迈瑞监护仪",
                "model": "BeneVision N17",
                "serial_no": "MR2024001",
                "department": "ICU",
                "location": "ICU 3床",
                "status": "在用",
                "price": 58000,
                "purchase_date": "2024-01-15",
                "warranty_end": "2027-01-14",
                "maintenance_date": "2026-03-15",
                "maintenance_cycle": 365,
                "supplier": "迈瑞医疗",
                "contact_phone": "400-888-8888",
                "manufacturer": "深圳迈瑞生物医疗电子股份有限公司",
                "remarks": "高端监护仪，支持远程查看"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "西门子CT",
                "model": "SOMATOM go.",
                "serial_no": "SI2023001",
                "department": "放射科",
                "location": "CT室",
                "status": "空闲",
                "price": 2800000,
                "purchase_date": "2023-06-20",
                "warranty_end": "2028-06-19",
                "maintenance_date": "2026-02-20",
                "maintenance_cycle": 365,
                "supplier": "西门子医疗",
                "contact_phone": "400-616-6666",
                "manufacturer": "西门子医疗系统有限公司",
                "remarks": "64排128层CT"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "飞利浦除颤仪",
                "model": "HeartStart XL+",
                "serial_no": "PH2024002",
                "department": "急诊科",
                "location": "抢救室",
                "status": "在用",
                "price": 75000,
                "purchase_date": "2024-03-10",
                "warranty_end": "2027-03-09",
                "maintenance_date": "2026-04-01",
                "maintenance_cycle": 365,
                "supplier": "飞利浦医疗",
                "contact_phone": "400-818-8888",
                "manufacturer": "飞利浦医疗系统",
                "remarks": "带心电图功能"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "德尔格呼吸机",
                "model": "Savina 300",
                "serial_no": "DR2023003",
                "department": "ICU",
                "location": "ICU 5床",
                "status": "维修中",
                "price": 120000,
                "purchase_date": "2023-11-05",
                "warranty_end": "2026-11-04",
                "maintenance_date": "2026-01-10",
                "maintenance_cycle": 365,
                "supplier": "德尔格医疗",
                "contact_phone": "400-668-8888",
                "manufacturer": "德尔格医疗设备有限公司",
                "remarks": "无创呼吸机"
            },
            {
                "id": str(uuid.uuid4()),
                "name": "日立超声",
                "model": "HI VISION",
                "serial_no": "HI2024004",
                "department": "超声科",
                "location": "超声检查室",
                "status": "在用",
                "price": 450000,
                "purchase_date": "2024-05-20",
                "warranty_end": "2027-05-19",
                "maintenance_date": "2026-05-01",
                "maintenance_cycle": 365,
                "supplier": "日立医疗",
                "contact_phone": "400-628-8888",
                "manufacturer": "日立医疗系统",
                "remarks": "四维彩超"
            }
        ]

# 初始化用户数据
if 'users' not in st.session_state:
    st.session_state.users = load_users()
    if not st.session_state.users:
        st.session_state.users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "系统管理员",
                "email": "admin@hospital.com",
                "phone": "13800000000",
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "manager": {
                "password": hash_password("manager123"),
                "role": "manager",
                "name": "设备科主任",
                "email": "manager@hospital.com",
                "phone": "13800000001",
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "repair1": {
                "password": hash_password("repair123"),
                "role": "repair",
                "name": "维修工程师",
                "email": "repair@hospital.com",
                "phone": "13800000002",
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "nurse1": {
                "password": hash_password("nurse123"),
                "role": "user",
                "name": "护士长",
                "email": "nurse@hospital.com",
                "phone": "13800000003",
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        }

# 初始化维修记录
if 'repair_records' not in st.session_state:
    st.session_state.repair_records = load_repair_records()

# 初始化保养记录
if 'maintenance_records' not in st.session_state:
    st.session_state.maintenance_records = load_maintenance_records()

# 初始化科室列表
if 'departments' not in st.session_state:
    st.session_state.departments = load_departments()
    if not st.session_state.departments:
        st.session_state.departments = ["ICU", "急诊科", "放射科", "超声科", "检验科", "手术室", "内科", "外科", "儿科", "妇产科"]

# 初始化操作日志
if 'operation_log' not in st.session_state:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            st.session_state.operation_log = json.load(f)
    else:
        st.session_state.operation_log = []

# 初始化登录状态
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

# ==================== 登录页面 ====================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 40px;'>
            <h1 style='color: #667eea;'>🏥 医疗设备管理系统</h1>
            <p style='color: #666;'>Medical Equipment Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("用户名", placeholder="请输入用户名")
            password = st.text_input("密码", type="password", placeholder="请输入密码")
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("登录", use_container_width=True)
            with col_b:
                if st.form_submit_button("重置", use_container_width=True):
                    st.rerun()
            
            if submit:
                if username in st.session_state.users:
                    if st.session_state.users[username]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.role = st.session_state.users[username]["role"]
                        save_log("登录系统", f"用户 {username} 登录成功")
                        st.success("登录成功！正在跳转...")
                        st.rerun()
                    else:
                        st.error("密码错误")
                else:
                    st.error("用户不存在")
        
        st.markdown("---")
        st.caption("默认账号：admin/admin123 | manager/manager123 | repair1/repair123 | nurse1/nurse123")

# ==================== 侧边栏 ====================
def render_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style='text-align: center; padding: 10px;'>
            <h3>🏥 医疗设备MIS</h3>
            <p style='color: #4a5568;'>欢迎，{st.session_state.users[st.session_state.username]['name']}</p>
            <p style='color: #718096; font-size: 12px;'>
                {'👑 管理员' if st.session_state.role == 'admin' else 
                  '📊 经理' if st.session_state.role == 'manager' else 
                  '🔧 工程师' if st.session_state.role == 'repair' else 
                  '👤 普通用户'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 导航菜单
        menu_options = ["📊 仪表板", "📋 设备台账", "🔧 设备管理", "🚨 维修工单", "📅 保养计划", "📊 统计分析", "⚙️ 系统设置"]
        
        if st.session_state.role == "admin":
            menu_options.append("👥 用户管理")
            menu_options.append("📜 操作日志")
        
        menu = st.radio("导航菜单", menu_options, label_visibility="collapsed")
        
        st.markdown("---")
        
        # 快捷操作
        st.markdown("### ⚡ 快捷操作")
        if st.button("➕ 快速报修", use_container_width=True):
            st.session_state.quick_repair = True
        if st.button("📅 保养提醒", use_container_width=True):
            st.session_state.show_maintenance = True
        
        # 系统信息
        st.markdown("---")
        st.caption(f"系统版本: v3.0")
        st.caption(f"登录时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        return menu

# ==================== 仪表板 ====================
def dashboard_page():
    st.markdown("<h2>📊 管理仪表板</h2>", unsafe_allow_html=True)
    
    # KPI卡片
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    devices = st.session_state.devices
    
    with col1:
        st.metric("📊 总设备数", len(devices), delta=None)
    with col2:
        total_value = sum(d.get('price', 0) for d in devices)
        st.metric("💰 总资产", f"¥{total_value:,.0f}")
    with col3:
        in_use = sum(1 for d in devices if d.get('status') == "在用")
        st.metric("✅ 使用中", in_use)
    with col4:
        repairing = sum(1 for d in devices if d.get('status') == "维修中")
        st.metric("🔧 维修中", repairing)
    with col5:
        # 逾期保养
        overdue = sum(1 for d in devices if get_maintenance_status(d.get('maintenance_date', ''))[0] == "逾期")
        st.metric("⚠️ 逾期保养", overdue, delta="需处理" if overdue > 0 else None)
    with col6:
        # 当月报修数
        this_month = sum(1 for r in st.session_state.repair_records 
                        if r.get('report_time', '').startswith(datetime.now().strftime("%Y-%m")))
        st.metric("📋 本月报修", this_month)
    
    st.markdown("---")
    
    # 图表区域
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # 科室设备分布
        dept_data = pd.DataFrame(devices)
        if not dept_data.empty:
            dept_counts = dept_data['department'].value_counts().reset_index()
            dept_counts.columns = ['科室', '数量']
            fig = px.pie(dept_counts, values='数量', names='科室', title='设备科室分布',
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        # 设备状态分布
        status_data = pd.DataFrame(devices)['status'].value_counts().reset_index()
        status_data.columns = ['状态', '数量']
        colors = {'在用': '#2ecc71', '空闲': '#3498db', '维修中': '#e74c3c', '报废': '#95a5a6'}
        fig = px.bar(status_data, x='状态', y='数量', title='设备状态统计',
                    color='状态', color_discrete_map=colors)
        st.plotly_chart(fig, use_container_width=True)
    
    # 第二行图表
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        # 设备价值TOP10
        if devices:
            value_data = sorted(devices, key=lambda x: x.get('price', 0), reverse=True)[:10]
            value_df = pd.DataFrame(value_data)
            fig = px.bar(value_df, x='name', y='price', title='设备价值TOP10',
                        color='price', color_continuous_scale='Greens')
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    with col_chart4:
        # 维修趋势
        if st.session_state.repair_records:
            repair_df = pd.DataFrame(st.session_state.repair_records)
            repair_df['report_date'] = pd.to_datetime(repair_df['report_time']).dt.date
            monthly_repair = repair_df.groupby(pd.to_datetime(repair_df['report_time']).dt.strftime('%Y-%m')).size()
            fig = px.line(x=monthly_repair.index, y=monthly_repair.values, title='月度维修趋势',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
    
    # 保养提醒
    st.markdown("---")
    st.subheader("🔔 保养提醒")
    
    today = datetime.now()
    upcoming = []
    overdue = []
    
    for device in devices:
        maint_date = device.get('maintenance_date')
        if maint_date and device.get('status') != "报废":
            maint = datetime.strptime(maint_date, "%Y-%m-%d")
            days_since = (today - maint).days
            if days_since > 365:
                overdue.append(device)
            elif days_since > 330:
                upcoming.append(device)
    
    if overdue:
        st.error(f"⚠️ 有 {len(overdue)} 台设备已超过一年未保养！")
        for d in overdue[:5]:
            st.write(f"- {d['name']} ({d['model']}) - 上次保养：{d['maintenance_date']}")
    
    if upcoming and not overdue:
        st.warning(f"📅 有 {len(upcoming)} 台设备即将到达保养周期")
        for d in upcoming[:5]:
            days_left = 365 - (today - datetime.strptime(d['maintenance_date'], "%Y-%m-%d")).days
            st.write(f"- {d['name']} ({d['model']}) - 剩余{days_left}天")

# ==================== 设备台账 ====================
def device_list_page():
    st.subheader("📋 设备台账管理")
    
    # 筛选区域
    with st.expander("🔍 高级筛选", expanded=False):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            search_name = st.text_input("设备名称")
        with col2:
            search_model = st.text_input("型号")
        with col3:
            dept_filter = st.multiselect("科室", st.session_state.departments)
        with col4:
            status_filter = st.multiselect("状态", ["在用", "空闲", "维修中", "报废"])
    
    # 过滤数据
    filtered = st.session_state.devices.copy()
    if search_name:
        filtered = [d for d in filtered if search_name.lower() in d['name'].lower()]
    if search_model:
        filtered = [d for d in filtered if search_model.lower() in d['model'].lower()]
    if dept_filter:
        filtered = [d for d in filtered if d.get('department') in dept_filter]
    if status_filter:
        filtered = [d for d in filtered if d.get('status') in status_filter]
    
    # 显示统计
    st.info(f"共找到 {len(filtered)} 台设备")
    
    # 数据表格
    if filtered:
        df = pd.DataFrame(filtered)
        
        # 添加保养状态和保修状态
        df['保养状态'] = df['maintenance_date'].apply(lambda x: get_maintenance_status(x)[0])
        df['保养标识'] = df['maintenance_date'].apply(lambda x: get_maintenance_status(x)[1])
        df['保修状态'] = df['warranty_end'].apply(lambda x: get_warranty_status(x)[0] if x else '未知')
        
        display_cols = ['name', 'model', 'serial_no', 'department', 'location', 'status', 
                       'price', 'purchase_date', '保养状态', '保修状态', 'supplier']
        
        st.dataframe(
            df[display_cols],
            column_config={
                "name": "设备名称",
                "model": "型号",
                "serial_no": "序列号",
                "department": "科室",
                "location": "位置",
                "status": st.column_config.SelectboxColumn("状态", options=["在用", "空闲", "维修中", "报废"]),
                "price": st.column_config.NumberColumn("价格", format="¥%.0f"),
                "purchase_date": "采购日期",
                "保养状态": st.column_config.TextColumn("保养状态"),
                "保修状态": st.column_config.TextColumn("保修状态"),
                "supplier": "供应商"
            },
            use_container_width=True,
            hide_index=True,
            height=500
        )
        
        # 导出按钮
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        with col_exp1:
            if st.button("📥 导出CSV", use_container_width=True):
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button("下载", csv, f"设备台账_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
        with col_exp2:
            if st.button("📊 导出Excel", use_container_width=True):
                excel_data = export_to_excel(df)
                st.download_button("下载", excel_data, f"设备台账_{datetime.now().strftime('%Y%m%d')}.xlsx", 
                                 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col_exp3:
            if st.button("🖨️ 打印预览", use_container_width=True):
                st.write("请按 Ctrl+P 打印")

# ==================== 设备管理 ====================
def device_manage_page():
    st.subheader("🔧 设备管理")
    
    tab1, tab2, tab3, tab4 = st.tabs(["➕ 添加设备", "✏️ 编辑设备", "📝 状态批量更新", "🗑️ 批量删除"])
    
    with tab1:
        with st.form("add_device_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
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
                contact_phone = st.text_input("联系电话")
            
            manufacturer = st.text_input("生产厂家")
            remarks = st.text_area("备注", height=80)
            
            if st.form_submit_button("添加设备"):
                if name and model:
                    warranty_end = purchase_date + timedelta(days=warranty_years*365)
                    new_device = {
                        "id": str(uuid.uuid4()),
                        "name": name,
                        "model": model,
                        "serial_no": serial_no if serial_no else "未填写",
                        "department": department,
                        "location": location if location else department,
                        "status": "空闲",
                        "price": price,
                        "purchase_date": purchase_date.strftime("%Y-%m-%d"),
                        "warranty_end": warranty_end.strftime("%Y-%m-%d"),
                        "maintenance_date": purchase_date.strftime("%Y-%m-%d"),
                        "maintenance_cycle": 365,
                        "supplier": supplier if supplier else "未填写",
                        "contact_phone": contact_phone if contact_phone else "未填写",
                        "manufacturer": manufacturer if manufacturer else "未填写",
                        "remarks": remarks,
                        "created_by": st.session_state.username,
                        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.devices.append(new_device)
                    save_data()
                    save_log("添加设备", f"添加设备：{name}")
                    st.success(f"✅ 设备 {name} 添加成功！")
                    st.rerun()
                else:
                    st.error("请填写设备名称和型号")
    
    with tab2:
        if st.session_state.devices:
            device_options = {f"{d['name']} - {d['model']}": d['id'] for d in st.session_state.devices}
            selected = st.selectbox("选择要编辑的设备", list(device_options.keys()))
            device_id = device_options[selected]
            device = next(d for d in st.session_state.devices if d['id'] == device_id)
            
            with st.form("edit_device_form"):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("设备名称", value=device['name'])
                    model = st.text_input("型号", value=device['model'])
                    serial_no = st.text_input("序列号", value=device.get('serial_no', ''))
                    department = st.selectbox("科室", st.session_state.departments, 
                                             index=st.session_state.departments.index(device.get('department', 'ICU')) if device.get('department') in st.session_state.departments else 0)
                    location = st.text_input("存放位置", value=device.get('location', ''))
                with col2:
                    price = st.number_input("采购价格(元)", value=float(device.get('price', 0)), step=1000.0)
                    purchase_date = st.date_input("采购日期", value=datetime.strptime(device['purchase_date'], "%Y-%m-%d") if device.get('purchase_date') else datetime.now())
                    supplier = st.text_input("供应商", value=device.get('supplier', ''))
                    status = st.selectbox("状态", ["在用", "空闲", "维修中", "报废"], 
                                         index=["在用", "空闲", "维修中", "报废"].index(device.get('status', '在用')))
                
                remarks = st.text_area("备注", value=device.get('remarks', ''), height=80)
                
                if st.form_submit_button("保存修改"):
                    device['name'] = name
                    device['model'] = model
                    device['serial_no'] = serial_no
                    device['department'] = department
                    device['location'] = location
                    device['price'] = price
                    device['purchase_date'] = purchase_date.strftime("%Y-%m-%d")
                    device['supplier'] = supplier
                    device['status'] = status
                    device['remarks'] = remarks
                    save_data()
                    save_log("编辑设备", f"编辑设备：{name}")
                    st.success("保存成功！")
                    st.rerun()
        else:
            st.info("暂无设备")
    
    with tab3:
        st.warning("批量更新设备状态")
        devices_to_update = st.multiselect("选择要更新的设备", 
                                           [f"{d['name']} - {d['model']}" for d in st.session_state.devices])
        new_bulk_status = st.selectbox("新状态", ["在用", "空闲", "维修中", "报废"])
        if st.button("批量更新"):
            for device_label in devices_to_update:
                device_name = device_label.split(" - ")[0]
                for d in st.session_state.devices:
                    if d['name'] == device_name:
                        d['status'] = new_bulk_status
            save_data()
            save_log("批量更新", f"批量更新 {len(devices_to_update)} 台设备状态为 {new_bulk_status}")
            st.success(f"已更新 {len(devices_to_update)} 台设备")
            st.rerun()
    
    with tab4:
        st.error("⚠️ 危险操作：批量删除设备")
        devices_to_delete = st.multiselect("选择要删除的设备", 
                                           [f"{d['name']} - {d['model']} (ID:{d['id'][:8]})" for d in st.session_state.devices])
        confirm = st.checkbox("我确认要删除这些设备")
        if st.button("批量删除", type="primary") and confirm:
            for device_label in devices_to_delete:
                device_id = device_label.split("ID:")[1].replace(")", "")
                st.session_state.devices = [d for d in st.session_state.devices if d['id'] != device_id]
            save_data()
            save_log("批量删除", f"删除 {len(devices_to_delete)} 台设备")
            st.success(f"已删除 {len(devices_to_delete)} 台设备")
            st.rerun()

# ==================== 维修工单 ====================
def repair_page():
    st.subheader("🚨 维修工单管理")
    
    tab1, tab2, tab3 = st.tabs(["📝 报修申请", "🔧 工单处理", "📋 工单查询"])
    
    with tab1:
        if st.session_state.devices:
            device_options = {f"{d['name']} - {d['model']} ({d['department']})": d['id'] 
                             for d in st.session_state.devices if d['status'] != "报废"}
            selected_device = st.selectbox("选择报修设备", list(device_options.keys()))
            
            col1, col2 = st.columns(2)
            with col1:
                urgency = st.selectbox("紧急程度", ["普通", "紧急", "特急"])
            with col2:
                fault_type = st.selectbox("故障类型", ["硬件故障", "软件问题", "需要校准", "配件更换", "操作问题", "其他"])
            
            description = st.text_area("故障描述", height=100, placeholder="请详细描述故障情况...")
            
            if st.button("提交报修单", type="primary"):
                device_id = device_options[selected_device]
                device = next(d for d in st.session_state.devices if d['id'] == device_id)
                
                repair_record = {
                    "id": str(uuid.uuid4()),
                    "device_id": device_id,
                    "device_name": selected_device,
                    "reporter": st.session_state.username,
                    "reporter_name": st.session_state.users[st.session_state.username]['name'],
                    "report_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "urgency": urgency,
                    "fault_type": fault_type,
                    "description": description,
                    "status": "待处理",
                    "assigned_to": "",
                    "repair_result": "",
                    "complete_time": ""
                }
                st.session_state.repair_records.append(repair_record)
                device['status'] = "维修中"
                save_data()
                save_repair_records()
                save_log("提交报修", f"设备报修：{selected_device}")
                st.success(f"✅ 报修单已提交！工单号：{repair_record['id'][:8]}")
                st.rerun()
        else:
            st.info("暂无设备")
    
    with tab2:
        st.write("### 待处理工单")
        pending = [r for r in st.session_state.repair_records if r.get('status') == "待处理"]
        
        if pending:
            for p in pending:
                with st.expander(f"🆕 工单 {p['id'][:8]} - {p['device_name']} - {p['urgency']}"):
                    st.write(f"**报修人：** {p.get('reporter_name', '')}")
                    st.write(f"**报修时间：** {p.get('report_time', '')}")
                    st.write(f"**故障类型：** {p.get('fault_type', '')}")
                    st.write(f"**故障描述：** {p.get('description', '')}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        assign_to = st.selectbox("指派给", ["维修一组", "维修二组", "外包服务"], key=f"assign_{p['id']}")
                    with col2:
                        if st.button("接受工单", key=f"accept_{p['id']}"):
                            p['status'] = "处理中"
                            p['assigned_to'] = assign_to
                            p['accept_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            save_repair_records()
                            save_log("接受工单", f"接受工单 {p['id'][:8]}")
                            st.success("工单已接受")
                            st.rerun()
        else:
            st.info("暂无待处理工单")
        
        st.write("### 处理中工单")
        processing = [r for r in st.session_state.repair_records if r.get('status') == "处理中"]
        
        if processing:
            for p in processing:
                with st.expander(f"🔧 工单 {p['id'][:8]} - {p['device_name']}"):
                    st.write(f"**指派给：** {p.get('assigned_to', '')}")
                    st.write(f"**故障描述：** {p.get('description', '')}")
                    
                    repair_result = st.text_area("维修结果", key=f"result_{p['id']}")
                    if st.button("完成工单", key=f"complete_{p['id']}"):
                        p['status'] = "已完成"
                        p['repair_result'] = repair_result
                        p['complete_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # 更新设备状态
                        for d in st.session_state.devices:
                            if d['id'] == p['device_id']:
                                d['status'] = "在用"
                        
                        save_data()
                        save_repair_records()
                        save_log("完成工单", f"完成工单 {p['id'][:8]}")
                        st.success("工单已完成")
                        st.rerun()
        else:
            st.info("暂无处理中工单")
    
    with tab3:
        st.write("### 工单查询")
        
        # 搜索筛选
        col1, col2 = st.columns(2)
        with col1:
            search_repair = st.text_input("搜索设备名称")
        with col2:
            status_filter = st.selectbox("工单状态", ["全部", "待处理", "处理中", "已完成"])
        
        filtered = st.session_state.repair_records.copy()
        if search_repair:
            filtered = [r for r in filtered if search_repair.lower() in r.get('device_name', '').lower()]
        if status_filter != "全部":
            filtered = [r for r in filtered if r.get('status') == status_filter]
        
        if filtered:
            df = pd.DataFrame(filtered)
            display_cols = ['id', 'device_name', 'urgency', 'fault_type', 'reporter_name', 'report_time', 'status']
            st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
        else:
            st.info("暂无工单记录")

# ==================== 保养计划 ====================
def maintenance_page():
    st.subheader("📅 设备保养计划")
    
    # 保养记录
    with st.expander("➕ 新增保养记录", expanded=False):
        device_options = {f"{d['name']} - {d['model']}": d['id'] for d in st.session_state.devices}
        selected = st.selectbox("选择设备", list(device_options.keys()))
        
        col1, col2 = st.columns(2)
        with col1:
            maint_date = st.date_input("保养日期")
            maint_type = st.selectbox("保养类型", ["日常检查", "定期保养", "年度大修", "校准"])
        with col2:
            next_maint = st.date_input("下次保养日期")
            cost = st.number_input("保养费用(元)", min_value=0, step=100)
        
        tech_person = st.text_input("保养人员")
        remarks = st.text_area("保养内容", height=80)
        
        if st.button("保存保养记录"):
            device_id = device_options[selected]
            for d in st.session_state.devices:
                if d['id'] == device_id:
                    d['maintenance_date'] = maint_date.strftime("%Y-%m-%d")
            
            maint_record = {
                "id": str(uuid.uuid4()),
                "device_id": device_id,
                "device_name": selected,
                "maint_date": maint_date.strftime("%Y-%m-%d"),
                "maint_type": maint_type,
                "next_maint_date": next_maint.strftime("%Y-%m-%d"),
                "cost": cost,
                "tech_person": tech_person,
                "remarks": remarks,
                "created_by": st.session_state.username,
                "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.maintenance_records.append(maint_record)
            save_data()
            save_maintenance_records()
            save_log("添加保养记录", f"设备保养：{selected}")
            st.success("保养记录已保存")
            st.rerun()
    
    # 保养日历
    st.markdown("### 📆 保养日历")
    
    # 获取所有保养记录
    if st.session_state.maintenance_records:
        maint_df = pd.DataFrame(st.session_state.maintenance_records)
        maint_df['maint_date'] = pd.to_datetime(maint_df['maint_date'])
        
        # 按月统计
        monthly = maint_df.groupby(maint_df['maint_date'].dt.strftime('%Y-%m')).size()
        fig = px.bar(x=monthly.index, y=monthly.values, title='月度保养统计')
        st.plotly_chart(fig, use_container_width=True)
    
    # 保养记录列表
    st.markdown("### 📋 保养记录")
    if st.session_state.maintenance_records:
        df = pd.DataFrame(st.session_state.maintenance_records[::-1])
        st.dataframe(df[['device_name', 'maint_date', 'maint_type', 'next_maint_date', 'tech_person']], 
                    use_container_width=True, hide_index=True)
    else:
        st.info("暂无保养记录")

# ==================== 统计分析 ====================
def statistics_page():
    st.subheader("📊 数据统计分析")
    
    tab1, tab2, tab3, tab4 = st.tabs(["💰 资产分析", "📈 趋势分析", "🏥 科室对比", "📋 报表导出"])
    
    devices_df = pd.DataFrame(st.session_state.devices)
    
    with tab1:
        # 资产分布
        if not devices_df.empty:
            # 按科室资产
            dept_asset = devices_df.groupby('department')['price'].sum().reset_index()
            dept_asset = dept_asset.sort_values('price', ascending=True)
            fig = px.bar(dept_asset, x='price', y='department', title='各科室设备资产总值', 
                        orientation='h', color='price', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
            
            # 资产折旧分析
            st.markdown("### 💸 设备折旧分析")
            depreciation_data = []
            for d in st.session_state.devices:
                if d.get('price', 0) > 0:
                    current_value = calculate_depreciation(d['price'], d['purchase_date'])
                    if current_value:
                        depreciation_data.append({
                            "设备名称": d['name'],
                            "原值": d['price'],
                            "当前估值": current_value,
                            "折旧率": f"{(1 - current_value/d['price'])*100:.1f}%"
                        })
            if depreciation_data:
                st.dataframe(pd.DataFrame(depreciation_data), use_container_width=True, hide_index=True)
    
    with tab2:
        if st.session_state.repair_records:
            repair_df = pd.DataFrame(st.session_state.repair_records)
            repair_df['report_date'] = pd.to_datetime(repair_df['report_time'])
            
            # 故障类型分布
            fault_counts = repair_df['fault_type'].value_counts()
            fig = px.pie(values=fault_counts.values, names=fault_counts.index, title='故障类型分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        if not devices_df.empty:
            # 科室设备对比
            dept_status = pd.crosstab(devices_df['department'], devices_df['status'])
            fig = px.bar(dept_status, barmode='group', title='各科室设备状态分布')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📋 报表导出")
        
        report_type = st.selectbox("选择报表类型", ["设备台账", "维修记录", "保养记录"])
        date_range = st.date_input("日期范围", [datetime.now() - timedelta(days=30), datetime.now()])
        
        if st.button("生成报表"):
            if report_type == "设备台账":
                df = devices_df
            elif report_type == "维修记录":
                df = pd.DataFrame(st.session_state.repair_records)
            else:
                df = pd.DataFrame(st.session_state.maintenance_records)
            
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下载报表", csv, f"{report_type}_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")

# ==================== 系统设置 ====================
def settings_page():
    st.subheader("⚙️ 系统设置")
    
    tab1, tab2, tab3 = st.tabs(["🔧 基础设置", "🏥 科室管理", "💾 数据管理"])
    
    with tab1:
        # 保养周期设置
        st.markdown("### 保养周期设置")
        default_cycle = st.number_input("默认保养周期(天)", min_value=30, max_value=730, value=365)
        
        # 通知设置
        st.markdown("### 通知设置")
        enable_email = st.checkbox("开启邮件通知")
        enable_sms = st.checkbox("开启短信通知")
        
        if st.button("保存设置"):
            st.success("设置已保存")
    
    with tab2:
        st.markdown("### 科室管理")
        
        # 添加科室
        col1, col2 = st.columns([3, 1])
        with col1:
            new_dept = st.text_input("新科室名称")
        with col2:
            if st.button("添加科室"):
                if new_dept and new_dept not in st.session_state.departments:
                    st.session_state.departments.append(new_dept)
                    save_departments()
                    st.success(f"科室 {new_dept} 已添加")
                    st.rerun()
        
        # 科室列表
        st.markdown("### 现有科室")
        for dept in st.session_state.departments:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"- {dept}")
            with col2:
                if st.button("删除", key=f"del_{dept}"):
                    if dept != "其他":
                        st.session_state.departments.remove(dept)
                        save_departments()
                        st.rerun()
    
    with tab3:
        st.markdown("### 数据管理")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("备份所有数据", use_container_width=True):
                save_data()
                save_users()
                save_repair_records()
                save_maintenance_records()
                save_departments()
                st.success("数据已备份")
        
        with col2:
            if st.button("清空日志", use_container_width=True):
                st.session_state.operation_log = []
                with open(LOG_FILE, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                st.success("日志已清空")

# ==================== 用户管理 ====================
def user_management_page():
    st.subheader("👥 用户权限管理")
    
    tab1, tab2 = st.tabs(["👤 用户列表", "➕ 添加用户"])
    
    with tab1:
        user_list = []
        for username, info in st.session_state.users.items():
            role_display = {
                "admin": "👑 管理员",
                "manager": "📊 经理",
                "repair": "🔧 维修工程师",
                "user": "👤 普通用户"
            }.get(info['role'], info['role'])
            user_list.append({
                "用户名": username,
                "姓名": info.get('name', ''),
                "角色": role_display,
                "邮箱": info.get('email', ''),
                "电话": info.get('phone', ''),
                "创建时间": info.get('created_time', '')
            })
        
        st.dataframe(pd.DataFrame(user_list), use_container_width=True, hide_index=True)
    
    with tab2:
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("用户名")
                password = st.text_input("密码", type="password")
                name = st.text_input("姓名")
            with col2:
                role = st.selectbox("角色", ["admin", "manager", "repair", "user"])
                email = st.text_input("邮箱")
                phone = st.text_input("电话")
            
            if st.form_submit_button("创建用户"):
                if username and username not in st.session_state.users:
                    st.session_state.users[username] = {
                        "password": hash_password(password),
                        "role": role,
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    save_users()
                    save_log("添加用户", f"添加用户：{username}")
                    st.success(f"用户 {username} 创建成功")
                    st.rerun()
                else:
                    st.error("用户名已存在或为空")

# ==================== 操作日志 ====================
def log_page():
    st.subheader("📜 系统操作日志")
    
    if st.session_state.operation_log:
        df = pd.DataFrame(st.session_state.operation_log[::-1])
        st.dataframe(df, use_container_width=True, hide_index=True, height=500)
        
        if st.button("导出日志"):
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button("下载", csv, f"operation_log_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    else:
        st.info("暂无操作记录")

# ==================== 主程序 ====================
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        menu = render_sidebar()
        
        if menu == "📊 仪表板":
            dashboard_page()
        elif menu == "📋 设备台账":
            device_list_page()
        elif menu == "🔧 设备管理":
            device_manage_page()
        elif menu == "🚨 维修工单":
            repair_page()
        elif menu == "📅 保养计划":
            maintenance_page()
        elif menu == "📊 统计分析":
            statistics_page()
        elif menu == "⚙️ 系统设置":
            settings_page()
        elif menu == "👥 用户管理":
            user_management_page()
        elif menu == "📜 操作日志":
            log_page()

if __name__ == "__main__":
    main()