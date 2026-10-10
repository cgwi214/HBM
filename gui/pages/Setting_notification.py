from nicegui import ui
from modules.utils import encrypt_data, decrypt_data

def set_notification(config, shared_softwareconfig):
    with ui.row():
        ui.link_target("NOTIFICATION")
        ui.label("通知设置").style('font-size: x-large')
    
    with ui.row():
        # 邮件
        with ui.card():
            ui.checkbox("是否启用邮件通知，默认为QQ邮箱").bind_value(config.userconfigdict, 'ENABLE_MAIL_NOTI')
            ui.input("邮件账号/QQ号").bind_value(config.userconfigdict, "MAIL_USER").style("width: 300px")
            ui.input("SMTP授权码", password=True, password_toggle_button=True).bind_value(
                config.userconfigdict, 
                "MAIL_PASS", 
                forward= lambda x: encrypt_data(x, shared_softwareconfig.softwareconfigdict["ENCRYPT_KEY"]),
                backward= lambda x: decrypt_data(x, shared_softwareconfig.softwareconfigdict["ENCRYPT_KEY"])
                ).style("width: 300px")
            
            # 高级模式让用户自己选择邮件发送服务器
            ui.checkbox("自定义邮件发送服务器").bind_value(config.userconfigdict, "ADVANCED_EMAIL")
            
            with ui.row().bind_visibility_from(config.userconfigdict, "ADVANCED_EMAIL"):
                # 发件人
                ui.input("发件人邮箱").bind_value(config.userconfigdict, "SENDER_EMAIL").style("width: 300px")
                # 收件人
                ui.input("收件人邮箱").bind_value(config.userconfigdict, "RECEIVER_EMAIL").style("width: 300px")
                # 邮件服务器
                ui.input("SMTP服务器").bind_value(config.userconfigdict, "MAIL_HOST").style("width: 300px")

            ui.label("如何获取授权码")
            ui.html('<iframe src="//player.bilibili.com/player.html?aid=583874363&bvid=BV16z4y1D74s&cid=211611094&p=1&autoplay=0" width="720px" height="480px" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>')
        
        with ui.card():
            ui.checkbox("是否启用API通知(PushPlus)").bind_value(config.userconfigdict, "ENABLE_HTTP_NOTI")
            ui.input("API通知Token",
                     password=True,
                     password_toggle_button=True
                     ).bind_value(config.userconfigdict, "TARGET_HTTP_TOKEN").style("width: 300px")
                
            # 目标url
            ui.input("API通知URL(get请求)").bind_value(config.userconfigdict, "TARGET_HTTP_URL").style("width: 500px").value = "http://www.pushplus.plus/send?token=[token]&title=[title]&content=[content]&template=txt"

            # 官网
            ui.link("PushPlus", "http://www.pushplus.plus/", new_tab=True)
