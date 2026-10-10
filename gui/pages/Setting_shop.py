from nicegui import ui
from DATA.assets.ItemName import ITEM_MAP

# 商品位置映射表 (列, 行): 商品名称


def get_item_name(col, row):
    """根据列行获取商品名称"""
    return ITEM_MAP.get((col, row), f"未知商品({col},{row})")
def set_shop(config):
    # ============= 特权商店 =============
    with ui.row().classes('w-full'):
        ui.link_target("SHOP_VIP")
        ui.label("特权商店").style('font-size: x-large')

        with ui.row().classes('w-full'):
            ui.checkbox("特权商店领金币").bind_value(config.userconfigdict, 'SHOP_VIP_FREE')

        with ui.row().classes('w-full items-center gap-4'):
            ui.label("特权忍者").classes('min-w-[80px]').style('font-size: large')
            vip_switch = ui.switch("购买开关").bind_value(config.userconfigdict, "SHOP_VIP_SWITCH")

            with ui.column().bind_visibility_from(vip_switch, 'value').style('width: 100%;'):
                with ui.row().classes('items-center gap-2'):
                    ap_check = ui.checkbox("秽土长门碎片").bind_value(config.userconfigdict, 'SHOP_VIP_AP')
                    # 购买次数输入框
                    ui.number('数量',
                              min=1,
                              max=3,
                              format='%.0f',
                              step=1
                              ).bind_value(config.userconfigdict, 'AP_TICKET_BUY_TIMES', forward=lambda x: int(x)
                                           ).bind_visibility_from(ap_check, 'value')

    # ============= 组织商店 =============
    with ui.row():
        ui.link_target("SHOP_ORGAN")
        ui.label("组织商店").style('font-size: x-large')
        # 开关
        organ_switch = ui.switch("组织商店购买开关").bind_value(config.userconfigdict, "SHOP_ORGAN_SWITCH")


    # 购买配置区域
    with ui.column().bind_visibility_from(organ_switch, 'value').style('width: 100%;'):
        with ui.row():
            # 购买所有
            ui.checkbox("组织商店购买所有").bind_value(config.userconfigdict, "SHOP_ORGAN_BUYALL").style("color: red")

        # 初始化配置结构
        if not config.userconfigdict["SHOP_ORGAN"]:
            config.userconfigdict["SHOP_ORGAN"] = [
                {'enabled': False, 'col': col, 'row': row}
                for (col, row) in sorted(ITEM_MAP.keys())
            ]

            # 可折叠配置项
        with ui.expansion('配置单个商品', icon='arrow_right').classes('w-full').props('default-opened=false'):
            for idx, (col, row) in enumerate(sorted(ITEM_MAP.keys())):
                item_name = ITEM_MAP[(col, row)]
                with ui.row().classes('items-center gap-4 w-full'):
                    # 启用开关
                    ui.checkbox(f'购买{item_name}').bind_value(
                        config.userconfigdict["SHOP_ORGAN"][idx], 'enabled'
                    ).classes('min-w-[200px]')

                    # # 列行配置
                    # with ui.column().bind_visibility_from(
                    #         config.userconfigdict["SHOP_ORGAN"][idx], 'enabled'
                    # ):
                    #     ui.number('列',
                    #               min=1,
                    #               max=7,
                    #               format='%.0f',
                    #               on_change=lambda e, idx=idx: e.value and config.userconfigdict["SHOP_ORGAN"][
                    #                   idx].update(col=int(e.value))
                    #               ).bind_value(config.userconfigdict["SHOP_ORGAN"][idx], 'col')
                    #
                    #     ui.number('行',
                    #               min=1,
                    #               max=2,
                    #               format='%.0f',
                    #               on_change=lambda e, idx=idx: e.value and config.userconfigdict["SHOP_ORGAN"][
                    #                   idx].update(row=int(e.value))
                    #               ).bind_value(config.userconfigdict["SHOP_ORGAN"][idx], 'row')





