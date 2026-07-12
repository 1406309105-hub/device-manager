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
            <h1>监护仪 · 工单</h1>
            <span class="ticket-id">#T202607111553C2A5</span>
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

    <!-- 保存工单信息按钮 -->
    <div class="btn-group">
        <button class="btn-primary" onclick="saveTicket()"><i class="fas fa-save"></i> 保存工单信息</button>
        <button class="btn-secondary" onclick="resetTicket()"><i class="fas fa-undo-alt"></i> 重置为示例</button>
    </div>

    <!-- ===== 状态时间线 (仍为只读示例，可后续动态) ===== -->
    <div class="status-section">
        <div class="section-title"><i class="fas fa-clock"></i> 状态流转历史</div>
        <div class="timeline" id="timelineContainer">
            <div class="timeline-item">
                <span class="dot active"></span>
                <span class="time">2026-07-11 15:53:22</span>
                <span><strong>已提交</strong> — 系统管理员 创建工单</span>
            </div>
            <div class="timeline-item">
                <span class="dot"></span>
                <span class="time">2026-07-11 16:10:05</span>
                <span><strong>已派单</strong> — 派发给 张伟</span>
            </div>
            <div class="timeline-item">
                <span class="dot"></span>
                <span class="time">2026-07-11 17:20:33</span>
                <span><strong>处理中</strong> — 张伟 开始诊断</span>
            </div>
        </div>
        <div class="status-meta">
            <span><i class="far fa-calendar-alt"></i> 提交：2026-07-11 15:53:22</span>
            <span><i class="far fa-hourglass"></i> SLA截止：<strong style="color:#dc2626;">2026-07-12 15:53:22</strong></span>
            <span><i class="fas fa-user-cog"></i> 当前状态：<span style="background:#dbeafe;color:#1d4ed8;padding:0 12px;border-radius:12px;">处理中</span></span>
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
            <div class="log-item">
                <div class="avatar">张</div>
                <div class="log-content">
                    <div class="log-meta">
                        <span class="name">张伟</span>
                        <span>·</span>
                        <span>2026-07-11 17:20:33</span>
                        <span class="tag" style="background:#fef3c7;color:#b45309;">处理中</span>
                    </div>
                    <div class="log-text">开始诊断，初步判断为软件冲突，需进一步检查日志。</div>
                </div>
            </div>
            <div class="log-item">
                <div class="avatar">系</div>
                <div class="log-content">
                    <div class="log-meta">
                        <span class="name">系统管理员</span>
                        <span>·</span>
                        <span>2026-07-11 15:53:22</span>
                        <span class="tag" style="background:#dbeafe;color:#1d4ed8;">已提交</span>
                    </div>
                    <div class="log-text">创建工单，故障描述：设备坏了。</div>
                </div>
            </div>
        </div>
    </div>

    <!-- 底部 -->
    <div style="margin-top:28px;border-top:1px solid #eef2f6;padding-top:18px;display:flex;justify-content:space-between;flex-wrap:wrap;font-size:13px;color:#94a3b8;">
        <span><i class="far fa-clock"></i> 工单创建：2026-07-11 15:53:22</span>
        <span><i class="fas fa-rotate-right"></i> 最后更新：2026-07-11 17:20:33</span>
        <span><i class="fas fa-user"></i> 当前处理人：张伟</span>
    </div>

</div>

<script>
    // ---- 字符计数 ----
    const textarea = document.getElementById('opContent');
    const counter = document.getElementById('charCounter');
    textarea.addEventListener('input', function() {
        counter.textContent = this.value.length;
    });

    // ---- 保存工单信息（模拟） ----
    function saveTicket() {
        const data = {
            deviceName: document.getElementById('deviceName').value,
            assetNo: document.getElementById('assetNo').value,
            model: document.getElementById('model').value,
            location: document.getElementById('location').value,
            manufacturer: document.getElementById('manufacturer').value,
            region: document.getElementById('region').value,
            dept: document.getElementById('dept').value,
            ward: document.getElementById('ward').value,
            faultType: document.getElementById('faultType').value,
            faultLevel: document.getElementById('faultLevel').value,
            impactScope: document.getElementById('impactScope').value,
            repairMethod: document.getElementById('repairMethod').value,
            faultTime: document.getElementById('faultTime').value,
            faultDesc: document.getElementById('faultDesc').value,
            reporter: document.getElementById('reporter').value,
            phone: document.getElementById('phone').value,
            submitTime: document.getElementById('submitTime').value,
            slaDeadline: document.getElementById('slaDeadline').value,
        };
        console.log('保存的工单数据：', data);
        showToast('✅ 工单信息已保存 (模拟)', '#16a34a');
        // 实际项目请在此处调用API
    }

    // ---- 重置为示例数据 ----
    function resetTicket() {
        document.getElementById('deviceName').value = '监护仪';
        document.getElementById('assetNo').value = '12345';
        document.getElementById('model').value = 'ipm8';
        document.getElementById('location').value = '1床';
        document.getElementById('manufacturer').value = '迈瑞';
        document.getElementById('region').value = '';
        document.getElementById('dept').value = '';
        document.getElementById('ward').value = '';
        document.getElementById('faultType').value = '软件问题';
        document.getElementById('faultLevel').value = '紧急';
        document.getElementById('impactScope').value = '单机';
        document.getElementById('repairMethod').value = '院内维修';
        document.getElementById('faultTime').value = '2026-07-11T14:30';
        document.getElementById('faultDesc').value = '设备坏了，无法开机';
        document.getElementById('reporter').value = '系统管理员';
        document.getElementById('phone').value = '12345789';
        document.getElementById('submitTime').value = '2026-07-11T15:53';
        document.getElementById('slaDeadline').value = '2026-07-12T15:53';
        showToast('已重置为示例数据', '#64748b');
    }

    // ---- 提交操作 ----
    function submitOperation() {
        const content = document.getElementById('opContent').value.trim();
        if (!content) {
            showToast('请填写处理内容', '#dc2626');
            document.getElementById('opContent').focus();
            return;
        }
        const status = document.getElementById('opStatus').value;
        const engineer = document.getElementById('opEngineer').value.trim() || '未知';

        // 模拟提交成功
        showToast(`✅ 操作已提交 (${status})`, '#16a34a');
        console.log({ content, status, engineer });

        // 追加到历史记录
        appendLog(content, status, engineer);

        // 清空处理内容（可选）
        document.getElementById('opContent').value = '';
        counter.textContent = '0';
    }

    // ---- 追加日志 ----
    function appendLog(content, status, engineer) {
        const logContainer = document.getElementById('logList');
        const statusMap = {
            '维修完成': { bg: '#dcfce7', color: '#15803d', label: '已完成' },
            '待备件': { bg: '#fef3c7', color: '#b45309', label: '待备件' },
            '转外修': { bg: '#fce7f3', color: '#be185d', label: '转外修' },
            '暂无法修复': { bg: '#fee2e2', color: '#b91c1c', label: '暂无法修复' },
            '其他': { bg: '#f1f5f9', color: '#475569', label: '其他' },
        };
        const s = statusMap[status] || statusMap['其他'];
        const newItem = document.createElement('div');
        newItem.className = 'log-item';
        newItem.innerHTML = `
            <div class="avatar">${engineer.charAt(0)}</div>
            <div class="log-content">
                <div class="log-meta">
                    <span class="name">${engineer}</span>
                    <span>·</span>
                    <span>${new Date().toLocaleString('zh-CN')}</span>
                    <span class="tag" style="background:${s.bg};color:${s.color};">${s.label}</span>
                </div>
                <div class="log-text">${content}</div>
            </div>
        `;
        logContainer.prepend(newItem); // 新记录添加到最前面
        // 保持最多6条
        while (logContainer.children.length > 6) {
            logContainer.lastChild.remove();
        }
    }

    // ---- 重置操作表单 ----
    function resetOpForm() {
        document.getElementById('opContent').value = '';
        counter.textContent = '0';
        document.getElementById('opStatus').selectedIndex = 3; // 暂无法修复
        document.getElementById('opEngineer').value = '张伟';
        const fileInput = document.querySelector('.file-upload input[type="file"]');
        if (fileInput) fileInput.value = '';
        showToast('已重置操作表单', '#64748b');
    }

    // ---- Toast ----
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

    // 初始化计数器
    document.addEventListener('DOMContentLoaded', () => {
        counter.textContent = textarea.value.length;
    });
</script>

</body>
</html>
