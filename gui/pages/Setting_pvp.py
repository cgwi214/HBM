from nicegui import ui


def set_pvp(config):
    with ui.row():
        ui.link_target("PVP_TASK")
        ui.label("决斗场").style('font-size: x-large')

    with ui.card():
        ui.label("请输入战斗次数").classes("text-weight-bold")

        # 总战斗次数输入框
        max_times = ui.number(
            label="总战斗回合次数",
            min=0,
            precision=0,
            step=8,
            format="%.0f",  # 强制显示为整数
            validation={
                '请输入整数': lambda value: isinstance(value, int) or (isinstance(value, float) and value.is_integer())
            }
        ).style("width: 180px").classes("q-mb-sm")
        max_times.bind_value(config.userconfigdict, "PVP_MAX_TIMES", forward=lambda x: int(x))

        # 胜利次数输入框
        victory_times = ui.number(
            label="胜利次数",
            min=0,
            precision=0,
            step=2,
            format="%.0f",
            validation={
                '请输入整数': lambda value: isinstance(value, int) or (isinstance(value, float) and value.is_integer())
            }
        ).style("width: 180px")
        victory_times.bind_value(config.userconfigdict, "PVP_VICTORY_TIMES", forward=lambda x: int(x))

        # 动态更新胜利次数最大值
        def update_victory_max():
            new_max = int(max_times.value)  # 强制转换为整数
            victory_times.min = 0
            victory_times.max = new_max
            if victory_times.value > new_max:
                victory_times.value = new_max
            victory_times.update()

        # 输入值强制整数化
        def force_integer(event):
            try:
                event.value = int(float(event.value))
            except:
                event.value = event.sender.value

        max_times.on('change', lambda e: [force_integer(e), update_victory_max()])
        victory_times.on('change', force_integer)

        # 初始化校验
        update_victory_max()