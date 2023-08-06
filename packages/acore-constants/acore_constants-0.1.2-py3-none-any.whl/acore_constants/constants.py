# -*- coding: utf-8 -*-


class TagKey:
    """

    :param SERVER_ID: **重要** 这个 tag 用来标注 EC2 和 RDS 是属于哪个逻辑 Server.
        它的值需满足如下格式: ``{env_name}-{server_name}``, 例如 ``sbx-blue``.
    :param WOW_STATUS: 这个 tag 用来记录 WOW 服务器的在线状态, 如果不在线则显示
        "stopped", 如果在线, 则显示 "N players" 其中 N 是一个整数. 注意这个 value
        的格式也很重要, 他会被其他项目的代码解析.
    :param WOW_STATUS_MEASURE_TIME: 这个 tag 用来记录 WOW_STATUS 的测量时间. 值为
        ISO 格式的 datetime.
    """

    SERVER_ID = "wserver:server_id"
    WOW_STATUS = "wserver:wow_status"
    WOW_STATUS_MEASURE_TIME = "wserver:wow_status_measure_time"
