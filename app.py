<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>工单操作 - 全字段编辑</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" />
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: #f0f4f8;
            padding: 24px;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }
        .container {
            max-width: 1100px;
            width: 100%;
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.08);
            padding: 32px 36px 40px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
        }
        .badge {
            background: #ef4444;
            color: #fff;
            font-size: 12px;
            font-weight: 700;
            padding: 4px 14px;
            border-radius: 100px;
        }
        .header-left h1 { font-size: 22px; font-weight: 600; color: #0f172a; }
        .ticket-id {
            color: #64748b;
            font-size: 14px;
            background: #f1f5f9;
            padding: 4px 14px;
            border-radius: 100px;
        }
        .header-actions button {
            background: #f1f5f9;
            border: none;
            padding: 8px 18px;
            border-radius: 30px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .header-actions button:hover { background: #e2e8f0; }

        /* 编辑区域 */
        .edit-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px 40px;
            background: #fafcff;
            border-radius: 16px;
            padding: 24px 28px;
            border: 1px solid #eef2f6;
            margin-bottom: 28px;
        }
        .edit-item {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .edit-item label {
            font-size: 13px;
            font-weight: 600;
            color: #334155;
        }
        .edit-item input, .edit-item select, .edit-item textarea {
            padding: 8px 12px;
            border: 1px solid #d1d9e6;
            border-radius: 10px;
            font-size: 14px;
            background: #fff;
            font-family: inherit;
            transition: border 0.2s;
        }
        .edit-item input:focus, .edit-item select:focus, .edit-item textarea:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
        }
        .edit-item textarea { resize: vertical; min-height: 60px; }
        .edit-item .full-width { grid-column: 1 / -1; }

        .btn-group {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 8px 0 20px 0;
        }
        .btn-primary {
            background: #2563eb;
            color: #fff;
            border: none;
            padding: 10px 32px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(37,99,235,0.25);
            transition: 0.2s;
        }
        .btn-primary:hover { background: #1d4ed8; }
        .btn-success {
            background: #16a34a;
            color: #fff;
            border: none;
            padding: 10px 32px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(22,163,74,0.25);
            transition: 0.2s;
        }
        .btn-success:hover { background: #15803d; }
        .btn-secondary {
            background: #f1f5f9;
            color: #1e293b;
            border: none;
            padding: 10px 24px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-secondary:hover { background: #e2e8f0; }
        .btn-danger {
            background: #dc2626;
            color: #fff;
            border: none;
            padding: 10px 24px;
            border-radius: 40px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-danger:hover { background: #b91c1c; }

        /* 状态时间线 */
        .status-section {
            border: 1px solid #eef2f6;
            border-radius: 16px;
            padding: 20px 24px;
            background: #fafcff;
            margin-bottom: 28px;
        }
        .status-section .section-title {
            font-size: 14px;
            font-weight: 600;
            color: #475569;
            text-transform: uppercase;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .timeline-item {
            display: flex;
            align-items: center;
            gap: 14px;
            font-size: 14px;
            padding: 6px 0;
            border-bottom: 1px dashed #e9edf2;
        }
        .timeline-item:last-child { border-bottom: none; }
        .timeline-item .dot {
            width: 10px; height: 10px;
            border-radius: 50%;
            background: #cbd5e1;
            flex-shrink: 0;
        }
        .timeline-item .dot.active { background: #3b82f6; }
        .timeline-item .time { color: #94a3b8; width: 150px; flex-shrink: 0; }
        .status-meta {
            display: flex; gap: 20px; flex-wrap: wrap;
            font-size: 13px; color: #475569;
            background: #f8fafc; padding: 10px 16px; border-radius: 10px;
            margin-top: 14px;
        }

        /* 操作填写卡片 */
        .operation-card {
            background: #fff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 24px 28px;
            margin: 20px 0 16px 0;
        }
        .operation-card .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 18px;
        }
        .operation-card .card-header h3 {
            font-size: 17px; font-weight: 600;
            display: flex; align-items: center; gap: 10px;
        }
        .op-form .form-row {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-bottom: 16px;
        }
        .op-form .form-row label { font-size: 13px; font-weight: 600; color: #334155; }
        .op-form .form-row textarea {
            width: 100%;
            min-height: 100px;
            padding: 14px 16px;
            border: 1px solid #d1d9e6;
            border-radius: 12px;
            font-size: 14px;
            font-family: inherit;
            resize: vertical;
        }
        .op-form .form-row textarea:focus {
            outline: none;
            border-color: #3b82f6;
        }
        .op-form .form-row .char-count { text-align: right; font-size: 12px; color: #94a3b8; margin-top: 4px; }
        .op-form .form-actions {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 14px 20px;
            border-top: 1px solid #f1f5f9;
            padding-top: 14px;
        }
        .file-upload {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #475569;
            cursor: pointer;
            background: #f8fafc;
            padding: 6px 16px;
            border-radius: 30px;
            border: 1px dashed #cbd5e1;
        }
        .file-upload:hover { background: #f1f5f9; }
        .file-upload input[type="file"] { display: none; }

        /* 操作记录列表 */
        .history-log {
            margin-top: 24px;
            border-top: 1px solid #eef2f6;
            padding-top: 22px;
        }
        .history-log .log-title {
            font-size: 14px; font-weight: 600; color: #475569;
            display: flex; align-items: center; gap: 8px;
            margin-bottom: 14px;
        }
        .log-item {
            display: flex;
            gap: 16px;
            padding: 12px 0;
            border-bottom: 1px solid #f1f5f9;
        }
        .log-item:last-child { border-bottom: none; }
        .log-item .avatar {
            width: 36px; height: 36px;
            border-radius: 50%;
            background: #dbeafe;
            color: #1d4ed8;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
            flex-shrink: 0;
        }
        .log-item .log-content { flex: 1; }
        .log-item .log-meta {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px 16px;
            font-size: 13px;
            color: #64748b;
            margin-bottom: 4px;
        }
        .log-item .log-meta .name { font-weight: 600; color: #0f172a; }
        .log-item .log-text { font-size: 14px; color: #1e293b; line-height: 1.6; }
        .tag {
            display: inline-block;
            padding: 0 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }

        @media (max-width: 820px) {
            .container { padding: 20px 18px; }
            .edit-grid { grid-template-columns: 1fr; padding: 18px 20px; }
            .header-left h1 { font-size: 18px; }
            .op-form .form-actions { flex-direction: column; align-items: stretch; }
            .op-form .form-actions .btn-primary { justify-content: center; }
        }
        @media (max-width: 480px) {
            body { padding: 12px; }
            .container { padding: 16px 12px; }
            .edit-item input, .edit-item select { font-size: 13px; }
        }
        .custom-toast {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #2563eb;
            color: #fff;
            padding: 14px 32px;
            border-radius: 50px;
            font-size: 15px;
            font-weight: 500;
            box-shadow: 0 12px 40px rgba(0,0,0,0.18);
            z-index: 9999;
            animation: slideUp 0.35s ease-out;
            transition: opacity 0.3s;
            max-width: 90%;
            text-align: center;
        }
        @keyframes slideUp {
            0% { opacity:0; transform: translateX(-50%) translateY(30px); }
            100% { opacity:1; transform: translateX(-50%) translateY(0); }
        }
    </style>
</head>
<body>

<div class="container">

    <!-- ===== HEADER ===== -->
    <div class="header">
        <div class="header-left">
            <span class="badge"><i class="fas fa-exclamation-triangle" style="margin-right:6px;"></i>紧急</span>
            <h1 id="pageTitle">监护仪 · 工单</h1>
            <span class="ticket-id" id="ticketIdDisplay">#T202607111553C2A5</span>
        </div>
        <div class="header-actions">
            <button><i class="fas fa-print"></i>打印</button>
            <button><i class="fas fa-history"></i>历史</button>
        </div>
    </div>

    <!-- ===== 工单信息 - 全部可编辑 ===== -->
    <div class="edit-grid">
        <!-- 左列 -->
        <div class="edit-item">
            <label>设备名称 <span style="color:#ef4444;">*</span></label>
            <input type="text" id="deviceName" value="监护仪" />
        </div>
        <div class="edit-item">
            <label>资产编号</label>
            <input type="text" id="assetNo" value="12345" />
        </div>
        <div class="edit-item">
            <label>设备型号</label>
            <input type="text" id="model" value="ipm8" />
        </div>
        <div class="edit-item">
            <label>存放位置</label>
            <input type="text" id="location" value="1床" />
        </div>
        <div class="edit-item">
            <label>生产厂家</label>
            <input type="text" id="manufacturer" value="迈瑞" />
        </div>
        <div class="edit-item">
            <label>所属区域</label>
            <input type="text" id="region" placeholder="例如：急诊科" />
        </div>
        <div class="edit-item">
            <label>报修科室</label>
            <input type="text" id="dept" placeholder="填写科室" />
        </div>
        <div class="edit-item">
            <label>病区/房间号</label>
            <input type="text" id="ward" placeholder="如：A区-3楼" />
        </div>
        <div class="edit-item">
            <label>故障类型</label>
            <select id="faultType">
                <option value="软件问题" selected>软件问题</option>
                <option value="硬件故障">硬件故障</option>
                <option value="网络异常">网络异常</option>
                <option value="其他">其他</option>
            </select>
        </div>
        <div class="edit-item">
            <label>故障等级</label>
            <select id="faultLevel">
                <option value="紧急" selected>紧急</option>
                <option value="高">高</option>
                <option value="中">中</option>
                <option value="低">低</option>
            </select>
        </div>
        <div class="edit-item">
            <label>影响范围</label>
            <select id="impactScope">
                <option value="单机" selected>单机</option>
                <option value="科室">科室</option>
                <option value="全院">全院</option>
            </select>
        </div>
        <div class="edit-item">
            <label>维修方式</label>
            <select id="repairMethod">
                <option value="院内维修" selected>院内维修</option>
                <option value="外送维修">外送维修</option>
                <option value="远程支持">远程支持</option>
            </select>
        </div>
        <div class="edit-item">
            <label>故障发生时间</label>
            <input type="datetime-local" id="faultTime" value="2026-07-11T14:30" />
        </div>
        <div class="edit-item full-width">
            <label>故障描述</label>
            <textarea id="faultDesc" rows="2">设备坏了，无法开机</textarea>
        </div>
        <!-- 报修人信息 -->
        <div class="edit-item">
            <label>报修人</label>
            <input type="text" id="reporter" value="系统管理员" />
        </div>
        <div class="edit-item">
            <label>联系电话</label>
            <input type="text" id="phone" value="12345789" />
        </div>
        <div class="edit-item">
            <label>提交时间</label>
            <input type="datetime-local" id="submitTime" value="2026-07-11T15:53" />
        </div>
        <div class="edit-item">
            <label>SLA截止</label>
            <input type="datetime-local" id="slaDeadline" value="2026-07-12T15:53" />
        </div>
    </div>

    <!-- 按钮组 -->
    <div class="btn-group">
        <button class="btn-success" onclick="newTicket()"><i class="fas fa-plus"></i> 新建工单</button>
        <button class="btn-primary" onclick="saveTicket()"><i class="fas fa-save"></i> 保存工单</button>
        <button class="btn-secondary" onclick="resetTicket()"><i class="fas fa-undo-alt"></i> 重置为示例</button>
        <button class="btn-danger" onclick="clearAll()"><i class="fas fa-trash"></i> 清空所有</button>
    </div>

    <!-- ===== 状态时间线 (动态从操作记录生成) ===== -->
    <div class="status-section">
        <div class="section-title"><i class="fas fa-clock"></i> 状态流转历史</div>
        <div class="timeline" id="timelineContainer">
            <!-- 由 JS 动态渲染 -->
        </div>
        <div class="status-meta" id="statusMeta">
            <!-- 由 JS 动态渲染 -->
        </div>
    </div>

    <!-- ===== 工单操作：填写处理内容 ===== -->
    <div class="operation-card">
        <div class="card-header">
            <h3><i class="fas fa-pen-to-square"></i> 填写操作记录</h3>
            <span class="hint"><i class="far fa-circle-check"></i> 带 <span style="color:#ef4444;">*</span> 为必填</span>
        </div>
        <form class="op-form" id="operationForm">
            <div class="form-row">
                <label for="opContent"><span style="color:#ef4444;">*</span> 处理内容 / 维修记录</label>
                <textarea id="opContent" placeholder="请详细描述本次操作…" maxlength="800"></textarea>
                <div class="char-count"><span id="charCounter">0</span> / 800</div>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                <div class="form-row">
                    <label>操作类型</label>
                    <select id="opStatus">
                        <option value="维修完成">维修完成</option>
                        <option value="待备件">待备件</option>
                        <option value="转外修">转外修</option>
                        <option value="暂无法修复" selected>暂无法修复</option>
                        <option value="其他">其他</option>
                    </select>
                </div>
                <div class="form-row">
                    <label>处理人</label>
                    <input type="text" id="opEngineer" value="张伟" />
                </div>
            </div>
            <div class="form-actions">
                <div class="file-upload">
                    <i class="fas fa-paperclip"></i> 添加附件
                    <input type="file" multiple />
                </div>
                <button type="button" class="btn-secondary" onclick="resetOpForm()"><i class="fas fa-undo-alt"></i> 重置</button>
                <button type="button" class="btn-primary" onclick="submitOperation()"><i class="fas fa-paper-plane"></i> 提交操作</button>
            </div>
        </form>
    </div>

    <!-- ===== 操作记录列表 ===== -->
    <div class="history-log">
        <div class="log-title"><i class="fas fa-list-ul"></i> 最近操作记录</div>
        <div id="logList">
            <!-- 由 JS 动态渲染 -->
        </div>
    </div>

    <!-- 底部 -->
    <div style="margin-top:28px;border-top:1px solid #eef2f6;padding-top:18px;display:flex;justify-content:space-between;flex-wrap:wrap;font-size:13px;color:#94a3b8;">
        <span><i class="far fa-clock"></i> 工单创建：<span id="createTime">2026-07-11 15:53:22</span></span>
        <span><i class="fas fa-rotate-right"></i> 最后更新：<span id="lastUpdate">2026-07-11 17:20:33</span></span>
        <span><i class="fas fa-user"></i> 当前处理人：<span id="currentHandler">张伟</span></span>
    </div>

</div>

<script>
    // ================================================================
    // 数据管理（使用 localStorage 持久化）
    // ================================================================

    const STORAGE_KEY_TICKET = 'ticketData';
    const STORAGE_KEY_OPS = 'operations';

    // 默认工单示例
    const defaultTicket = {
        deviceName: '监护仪',
        assetNo: '12345',
        model: 'ipm8',
        location: '1床',
        manufacturer: '迈瑞',
        region: '',
        dept: '',
        ward: '',
        faultType: '软件问题',
        faultLevel: '紧急',
        impactScope: '单机',
        repairMethod: '院内维修',
        faultTime: '2026-07-11T14:30',
        faultDesc: '设备坏了，无法开机',
        reporter: '系统管理员',
        phone: '12345789',
        submitTime: '2026-07-11T15:53',
        slaDeadline: '2026-07-12T15:53'
    };

    // 默认操作记录
    const defaultOps = [
        { engineer: '张伟', time: '2026-07-11 17:20:33', status: '处理中', content: '开始诊断，初步判断为软件冲突，需进一步检查日志。' },
        { engineer: '系统管理员', time: '2026-07-11 15:53:22', status: '已提交', content: '创建工单，故障描述：设备坏了。' }
    ];

    // 当前数据
    let ticketData = {};
    let operations = [];

    // 加载数据（从 localStorage 或默认）
    function loadData() {
        const savedTicket = localStorage.getItem(STORAGE_KEY_TICKET);
        const savedOps = localStorage.getItem(STORAGE_KEY_OPS);
        if (savedTicket) {
            try { ticketData = JSON.parse(savedTicket); } catch(e) { ticketData = { ...defaultTicket }; }
        } else {
            ticketData = { ...defaultTicket };
        }
        if (savedOps) {
            try { operations = JSON.parse(savedOps); } catch(e) { operations = [...defaultOps]; }
        } else {
            operations = [...defaultOps];
        }
    }

    // 保存数据到 localStorage
    function saveData() {
        localStorage.setItem(STORAGE_KEY_TICKET, JSON.stringify(ticketData));
        localStorage.setItem(STORAGE_KEY_OPS, JSON.stringify(operations));
    }

    // ================================================================
    // DOM 引用
    // ================================================================
    const fieldIds = [
        'deviceName', 'assetNo', 'model', 'location', 'manufacturer',
        'region', 'dept', 'ward', 'faultType', 'faultLevel',
        'impactScope', 'repairMethod', 'faultTime', 'faultDesc',
        'reporter', 'phone', 'submitTime', 'slaDeadline'
    ];

    // ================================================================
    // 渲染函数
    // ================================================================

    // 将 ticketData 填充到表单
    function renderTicket() {
        fieldIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.value = ticketData[id] || '';
            }
        });
        // 更新工单编号显示
        const ticketIdDisplay = document.getElementById('ticketIdDisplay');
        if (ticketData.ticketId) {
            ticketIdDisplay.textContent = '#' + ticketData.ticketId;
        } else {
            // 若没有编号，生成一个临时编号（基于时间）
            const ts = new Date().getTime().toString(16).toUpperCase();
            ticketIdDisplay.textContent = '#T' + ts;
        }
        // 更新标题
        document.getElementById('pageTitle').textContent = (ticketData.deviceName || '设备') + ' · 工单';
    }

    // 渲染操作记录列表（按时间倒序）
    function renderOperations() {
        const container = document.getElementById('logList');
        container.innerHTML = '';
        const sorted = [...operations].sort((a, b) => new Date(b.time) - new Date(a.time));
        sorted.forEach(op => {
            const div = document.createElement('div');
            div.className = 'log-item';
            const statusMap = {
                '维修完成': { bg: '#dcfce7', color: '#15803d', label: '已完成' },
                '待备件': { bg: '#fef3c7', color: '#b45309', label: '待备件' },
                '转外修': { bg: '#fce7f3', color: '#be185d', label: '转外修' },
                '暂无法修复': { bg: '#fee2e2', color: '#b91c1c', label: '暂无法修复' },
                '已提交': { bg: '#dbeafe', color: '#1d4ed8', label: '已提交' },
                '处理中': { bg: '#fef3c7', color: '#b45309', label: '处理中' },
                '其他': { bg: '#f1f5f9', color: '#475569', label: '其他' },
            };
            const s = statusMap[op.status] || statusMap['其他'];
            div.innerHTML = `
                <div class="avatar">${op.engineer ? op.engineer.charAt(0) : '?'}</div>
                <div class="log-content">
                    <div class="log-meta">
                        <span class="name">${op.engineer || '未知'}</span>
                        <span>·</span>
                        <span>${op.time || ''}</span>
                        <span class="tag" style="background:${s.bg};color:${s.color};">${s.label}</span>
                    </div>
                    <div class="log-text">${op.content || ''}</div>
                </div>
            `;
            container.appendChild(div);
        });
        // 更新状态时间线（从操作记录生成）
        renderTimeline(sorted);
        // 更新状态元信息
        updateStatusMeta(sorted);
    }

    // 渲染时间线
    function renderTimeline(sortedOps) {
        const container = document.getElementById('timelineContainer');
        container.innerHTML = '';
        if (sortedOps.length === 0) {
            container.innerHTML = '<div style="color:#94a3b8;font-size:14px;">暂无操作记录</div>';
            return;
        }
        sortedOps.forEach((op, index) => {
            const div = document.createElement('div');
            div.className = 'timeline-item';
            const dotClass = index === 0 ? 'dot active' : 'dot';
            div.innerHTML = `
                <span class="${dotClass}"></span>
                <span class="time">${op.time}</span>
                <span><strong>${op.status}</strong> — ${op.engineer} ${op.content ? '：' + op.content : ''}</span>
            `;
            container.appendChild(div);
        });
    }

    // 更新状态元信息
    function updateStatusMeta(sortedOps) {
        const meta = document.getElementById('statusMeta');
        if (sortedOps.length === 0) {
            meta.innerHTML = '<span>暂无状态信息</span>';
            return;
        }
        const latest = sortedOps[0];
        const submitTime = document.getElementById('submitTime').value || '未设置';
        const sla = document.getElementById('slaDeadline').value || '未设置';
        meta.innerHTML = `
            <span><i class="far fa-calendar-alt"></i> 提交：${submitTime}</span>
            <span><i class="far fa-hourglass"></i> SLA截止：<strong style="color:#dc2626;">${sla}</strong></span>
            <span><i class="fas fa-user-cog"></i> 当前状态：<span style="background:#dbeafe;color:#1d4ed8;padding:0 12px;border-radius:12px;">${latest.status}</span></span>
            <span><i class="fas fa-user"></i> 最新处理人：${latest.engineer}</span>
        `;
        // 更新底部
        document.getElementById('currentHandler').textContent = latest.engineer || '未知';
        document.getElementById('lastUpdate').textContent = latest.time || '未知';
        document.getElementById('createTime').textContent = submitTime;
    }

    // ================================================================
    // 操作函数
    // ================================================================

    // 从表单收集数据
    function collectTicketFromForm() {
        const data = {};
        fieldIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) data[id] = el.value;
        });
        return data;
    }

    // 保存工单
    function saveTicket() {
        const newData = collectTicketFromForm();
        // 保留原有 ticketId（如果有）
        if (ticketData.ticketId) {
            newData.ticketId = ticketData.ticketId;
        }
        ticketData = newData;
        saveData();
        renderTicket();
        showToast('✅ 工单信息已保存', '#16a34a');
        console.log('保存的工单数据：', ticketData);
    }

    // 新建工单（清空所有字段，生成新编号，清空操作记录）
    function newTicket() {
        if (!confirm('确认新建工单？当前数据将被清空（可先保存）。')) return;
        // 清空 ticketData 为默认空值
        const emptyTicket = {};
        fieldIds.forEach(id => {
            emptyTicket[id] = '';
        });
        // 生成新工单编号
        const ts = new Date().getTime().toString(16).toUpperCase();
        emptyTicket.ticketId = 'T' + ts;
        // 设置默认故障等级为“紧急”
        emptyTicket.faultLevel = '紧急';
        emptyTicket.faultType = '软件问题';
        emptyTicket.impactScope = '单机';
        emptyTicket.repairMethod = '院内维修';
        // 设置当前时间为提交时间
        const now = new Date();
        const iso = now.toISOString().slice(0, 16);
        emptyTicket.submitTime = iso;
        emptyTicket.faultTime = iso;
        // SLA 设为提交时间 + 24小时
        const sla = new Date(now.getTime() + 24 * 3600 * 1000);
        emptyTicket.slaDeadline = sla.toISOString().slice(0, 16);

        ticketData = emptyTicket;
        operations = []; // 清空操作记录
        saveData();
        renderTicket();
        renderOperations();
        // 重置操作表单
        document.getElementById('opContent').value = '';
        document.getElementById('charCounter').textContent = '0';
        document.getElementById('opStatus').selectedIndex = 3;
        document.getElementById('opEngineer').value = '';
        showToast('✅ 已创建新工单', '#16a34a');
    }

    // 重置为示例数据
    function resetTicket() {
        if (!confirm('重置为示例数据？当前数据将被覆盖。')) return;
        ticketData = { ...defaultTicket };
        operations = [...defaultOps];
        saveData();
        renderTicket();
        renderOperations();
        // 重置操作表单
        document.getElementById('opContent').value = '';
        document.getElementById('charCounter').textContent = '0';
        document.getElementById('opStatus').selectedIndex = 3;
        document.getElementById('opEngineer').value = '张伟';
        showToast('已重置为示例数据', '#64748b');
    }

    // 清空所有（包括工单和操作记录）
    function clearAll() {
        if (!confirm('确认清空所有数据？此操作不可撤销！')) return;
        const emptyTicket = {};
        fieldIds.forEach(id => { emptyTicket[id] = ''; });
        ticketData = emptyTicket;
        operations = [];
        saveData();
        renderTicket();
        renderOperations();
        document.getElementById('opContent').value = '';
        document.getElementById('charCounter').textContent = '0';
        document.getElementById('opStatus').selectedIndex = 3;
        document.getElementById('opEngineer').value = '';
        showToast('已清空所有数据', '#64748b');
    }

    // 提交操作
    function submitOperation() {
        const content = document.getElementById('opContent').value.trim();
        if (!content) {
            showToast('请填写处理内容', '#dc2626');
            document.getElementById('opContent').focus();
            return;
        }
        const status = document.getElementById('opStatus').value;
        const engineer = document.getElementById('opEngineer').value.trim() || '未知';
        const now = new Date().toLocaleString('zh-CN', { hour12: false });
        const newOp = {
            engineer: engineer,
            time: now,
            status: status,
            content: content
        };
        operations.push(newOp);
        // 限制最多20条
        if (operations.length > 20) {
            operations = operations.slice(-20);
        }
        saveData();
        renderOperations();
        // 清空输入
        document.getElementById('opContent').value = '';
        document.getElementById('charCounter').textContent = '0';
        showToast(`✅ 操作已提交 (${status})`, '#16a34a');
        console.log('新操作：', newOp);
    }

    // 重置操作表单
    function resetOpForm() {
        document.getElementById('opContent').value = '';
        document.getElementById('charCounter').textContent = '0';
        document.getElementById('opStatus').selectedIndex = 3;
        document.getElementById('opEngineer').value = '';
        const fileInput = document.querySelector('.file-upload input[type="file"]');
        if (fileInput) fileInput.value = '';
        showToast('已重置操作表单', '#64748b');
    }

    // ================================================================
    // Toast 提示
    // ================================================================
    function showToast(msg, color = '#2563eb') {
        const old = document.querySelector('.custom-toast');
        if (old) old.remove();
        const toast = document.createElement('div');
        toast.className = 'custom-toast';
        toast.style.background = color;
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 400);
        }, 2500);
    }

    // ================================================================
    // 初始化
    // ================================================================
    document.addEventListener('DOMContentLoaded', function() {
        loadData();
        renderTicket();
        renderOperations();

        // 字符计数器
        const textarea = document.getElementById('opContent');
        const counter = document.getElementById('charCounter');
        textarea.addEventListener('input', function() {
            counter.textContent = this.value.length;
        });
        counter.textContent = textarea.value.length;

        // 监听表单字段变化，自动更新 ticketData（但不自动保存）
        fieldIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener('change', function() {
                    // 只是同步到 ticketData，但不保存到 localStorage（用户点击保存才保存）
                    ticketData[id] = this.value;
                });
                el.addEventListener('input', function() {
                    ticketData[id] = this.value;
                });
            }
        });
    });
</script>

</body>
</html>
