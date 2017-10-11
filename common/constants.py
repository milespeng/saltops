MINION_STATUS = (
    (0, '未启动'),
    (1, '运行中'),
    (2, '待接受'),
    (3, '已拒绝'),
    (4, '已禁止'),
)

IP_TYPE = (
    (100, '----'),
    (0, '内网'),
    (1, '外网'),
    (2, '管理网')
)

TOOL_RUN_TYPE = (
    (0, 'SaltState'),
    (1, 'Shell'),
    (2, 'PowerShell'),
    (3, 'Python'),
    (4, 'Salt命令'),
    (5, 'Windows批处理')
)
