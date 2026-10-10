def HBM_core_process(reread_config_name = None, must_auto_quit = False, msg_queue = None):
    """
    运行HBM核心流程
    RUN CORE HBM PROCESS

    @param reread_config_name: 是否重新解析config名
    @param must_auto_quit: 是否运行结束时自动退出
    @param msg_queue: log输出管道
    """
    # ============= Initialize =============
    from modules.configs.MyConfig import config
    if reread_config_name is not None:
        config.parse_user_config(reread_config_name)
    
    from modules.utils.log_utils import logging
    logging.set_log_queue(msg_queue)

    # ============= Import =============

    import os
    from modules.utils import subprocess_run, time, disconnect_this_device, sleep, check_connect, open_app, close_app, get_now_running_app, screenshot, click, check_app_running, subprocess, create_notificationer, EmulatorBlockError
    from modules.AllTask.myAllTask import my_AllTask

    def print_HBM_info():
        logging.info("+" + "HBM".center(88, "=") + "+")
        logging.info("||" + "你好".center(85, " ") + "||")
        logging.info("||" + "本工具不涉及逆向，破解，绕过权限，调用应用API等等侵犯行为".center(60, " ") + "||")
        logging.info("||" + "本项目仅限用于学术交流和研究目的，严禁任何形式的商业用途、非法传播及违法违规应用。".center(47, " ") + "||")
        logging.info("||" + "使用者应自觉遵守所在国家/地区的法律法规，若因违规使用导致法律纠纷或责任事故，".center(50," ") + "||")
        logging.info("||" + "相关后果由使用者自行承担，项目方保留追究其法律责任的权利。".center(59, " ") + "||")
        logging.info("||" + "".center(86, " ") + "||")
        logging.info("+" + "".center(88, "=") + "+")

    def print_HBM_config_info():
        from modules.utils.adb_utils import check_adb_binding
        check_adb_binding()
        adb_connect_string = f"{config.userconfigdict['ADB_SEIAL_NUMBER']}" if config.userconfigdict[
            'ADB_DIRECT_USE_SERIAL_NUMBER'] else f"{config.userconfigdict['TARGET_IP_PATH']}:{config.userconfigdict['TARGET_PORT']}"
        # 打印config信息
        logging.info(f"读取的配置文件: {config.nowuserconfigname}")
        logging.info(f"模拟器:{config.userconfigdict['TARGET_EMULATOR_PATH']}")
        logging.info(f"ADB连接: {adb_connect_string}")

    def print_HBM_finish():
        print_HBM_info()
        logging.info("\n程序运行结束")

    def HBM_release_adb_port(justDoIt=False):
        """
        释放adb端口，通常被一个后台进程占用
        """
        if config.userconfigdict["KILL_PORT_IF_EXIST"] or justDoIt:
            try:
                # 确保端口未被占用
                res = subprocess_run(["netstat", "-ano"], encoding="gbk").stdout
                for line in res.split("\n"):
                    if ":"+str(config.userconfigdict["TARGET_PORT"]) in line and "LISTENING" in line:
                        logging.info(line)
                        logging.info("端口被占用，正在释放")
                        pid=line.split()[-1]
                        subprocess_run(["taskkill", "/T", "/F", "/PID", pid], encoding="gbk")
                        logging.info("端口被占用，已释放")
                        config.sessiondict["PORT_IS_USED"] = True
                        break
            except Exception as e:
                logging.error("释放端口失败，请关闭模拟器后重试")
                logging.error(e)


    def _check_process_exist(pid):
        """
        检查进程是否存在
        """
        try:
            tasks = subprocess_run(["tasklist"], encoding="gbk").stdout
            tasklist = tasks.split("\n")
            for task in tasklist:
                wordlist = task.strip().split()
                if len(wordlist) > 1 and wordlist[1] == str(pid):
                    logging.info(" | ".join(wordlist))
                    return True
            return False
        except Exception as e:
            logging.error(e)
            return False


    def HBM_start_emulator():
        """
        启动模拟器
        """
        if config.userconfigdict["TARGET_EMULATOR_PATH"] and config.userconfigdict["TARGET_EMULATOR_PATH"] != "":
            try:
                # 以列表形式传命令行参数
                logging.info("启动模拟器")
                # 不能用shell，否则得到的是shell的pid
                emulator_process = subprocess_run(config.userconfigdict['TARGET_EMULATOR_PATH'], isasync=True)
                logging.info("模拟器pid: " + str(emulator_process.pid))
                time.sleep(30)
                # 检查pid是否存在
                if not _check_process_exist(emulator_process.pid):
                    logging.warn("模拟器启动进程已结束，可能是启动失败，或者是模拟器已经在运行")
                else:
                    # 存进session，这样最后根据需要按照这个pid杀掉模拟器
                    config.sessiondict["EMULATOR_PROCESS_PID"] = emulator_process.pid
            except Exception as e:
                logging.error("启动模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
                logging.error(e)
        else:
            logging.info("未配置模拟器路径，跳过启动模拟器")


    def HBM_check_adb_connect():
        """
        检查adb连接
        """
        # 检查adb连接
        disconnect_this_device()
        for i in range(1, 10):
            sleep(i)
            if check_connect():
                logging.info("adb连接成功")
                return True
            else:
                logging.info("未检测到设备连接, 重试...")
        if config.sessiondict["PORT_IS_USED"]:
            # 连接失败，并且出现端口被占用的情况，现在模拟器的用户可见进程的端口估计是配置文件里的后一个端口
            # 提醒用户启动HBM时，不要启动模拟器
            raise Exception("检测到启动HBM前 端口已被占用，但HBM无法连接至该端口。上次模拟器可能未被正常关闭，请在启动HBM前关闭模拟器")
        raise Exception("adb连接失败, 请检查配置里的adb端口")



    def HBM_open_target_app():
        """
        打开游戏
        """
        if check_app_running(config.userconfigdict['ACTIVITY_PATH']):
            logging.info("检测到游戏已经在运行")
            return True
        for i in range(40):
            logging.info(f"打开游戏{i}/30")
            open_app(config.userconfigdict['ACTIVITY_PATH'])
            sleep(5)
            if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
                logging.error("未检测到游戏打开，请检查设置")
            else:
                return True
        raise Exception("未检测到游戏打开，请检查设置 以及 如果使用的是MuMu模拟器，请关闭后台保活")

    def HBM_close_target_app():
        """
        关闭游戏
        """
        if (config.userconfigdict["CLOSE_GAME_FINISH"]):
            if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
                logging.info("检测到游戏已关闭")
                return True
            for i in range(5):
                logging.info(f"关闭游戏{i}/5")
                close_app(config.userconfigdict['ACTIVITY_PATH'])
                sleep(3)
                if not check_app_running(config.userconfigdict['ACTIVITY_PATH']):
                    logging.info("游戏已关闭")
                    return True
                    
    def HBM_run_pre_command():
        if len(config.userconfigdict["PRE_COMMAND"]) > 0:
            logging.info("运行前置命令")
            sleep(1.5)
            subprocess.Popen(config.userconfigdict["PRE_COMMAND"], shell=True)

    def HBM_run_post_command():
        if len(config.userconfigdict["POST_COMMAND"]) > 0:
            logging.info("运行后置命令")
            sleep(1.5)
            subprocess.Popen(config.userconfigdict["POST_COMMAND"], shell=True)

    def HBM_kill_emulator(must_do = False):
        """
        杀掉模拟器进程
        """
        if (config.userconfigdict["TARGET_EMULATOR_PATH"] and (config.userconfigdict["CLOSE_EMULATOR_FINISH"] or must_do)):
            try:
                if not config.sessiondict["EMULATOR_PROCESS_PID"]:
                    logging.error("未能获取到模拟器进程，跳过关闭模拟器")
                    return
                # 提取出模拟器的exe名字
                full_path = config.userconfigdict['TARGET_EMULATOR_PATH']
                emulator_exe = os.path.basename(full_path).split(".exe")[0] + ".exe"
                subprocess_run(["taskkill", "/T", "/F", "/PID", str(config.sessiondict["EMULATOR_PROCESS_PID"])],
                            encoding="gbk")
                # 杀掉模拟器可见窗口进程后，可能残留后台进程，这里根据adb端口再杀一次
                HBM_release_adb_port(justDoIt=True)
            except Exception as e:
                logging.error("关闭模拟器失败, 可能是没有以管理员模式运行 或 配置的模拟器路径有误")
                logging.error(e)
        else:
            logging.info("跳过关闭模拟器")


    def HBM_send_email():
        """
        发送邮件
        """
        logging.info("尝试发送通知")
        try:
            # 构造通知对象
            notificationer = create_notificationer()
            # 构造邮件内容
            content = []
            content.append("HBM任务结束")
            content.append("配置文件名称: " + config.nowuserconfigname)
            content.append("任务开始时间: " + config.sessiondict["HBM_START_TIME"])
            content.append("开始时资源: " + str(config.sessiondict["BEFORE_HBM_SOURCES"]))
            content.append("任务结束时间: " + time.strftime("%Y-%m-%d %H:%M:%S"))
            content.append("结束时资源: " + str(config.sessiondict["AFTER_HBM_SOURCES"]))
            # 任务内容
            content.append("执行的任务内容:")
            tasks_str = ""
            for ind, task in enumerate(config.userconfigdict["TASK_ORDER"]):
                if config.userconfigdict["TASK_ACTIVATE"][ind]:
                    tasks_str += f" -> {task}"
            content.append(tasks_str)
            # 其他消息
            content.append("其他消息:")
            info_str = ""
            # INFO_DICT 里的信息
            for key, value in config.sessiondict["INFO_DICT"].items():
                info_str += f"{value}\n"
            content.append(info_str)
            # 发送
            fullcontent = "\r\n".join(content)
            notificationer.send(fullcontent, title="HBM结束")
            logging.info("通知发送结束")
        except Exception as e:
            logging.error("发送通知失败")
            logging.error(e)

    def HBM_auto_quit(forcewait = False, key_map_func = None):
        """ 结束运行，如果用户没有勾选自动关闭模拟器与HBM，等待用户按回车键 """
        # 用于GUI识别是否结束的关键字
        logging.info("GUI_HBM_TASK_END")
        # 默认值空字典
        if key_map_func is None:
            key_map_func = dict()
        if must_auto_quit:
            return
        if forcewait or not config.userconfigdict["CLOSE_HBM_FINISH"]:
            user_input = input(f"Press Enter to exit/回车退出, "+str([f"[{k}]{key_map_func[k]['desc']}" for k in key_map_func]) + ": ")
            for k in key_map_func:
                if user_input.upper() == k.upper():
                    key_map_func[k]["func"]()
                    break
        else:
            logging.info("10秒后自动关闭")
            sleep(10)
            
    def HBM_rm_pic():
        """运行结束后，删除截图文件，内含try-except"""
        try:
            # 运行结束后如果截图文件存在，删除截图文件
            if os.path.exists(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}"):
                os.remove(f"./{config.userconfigdict.get('SCREENSHOT_NAME')}")
        except Exception as e:
            logging.error("删除截图文件失败")

    def HBM_send_err_mail(e):
        """ 发送错误通知邮件 """
        if config.userconfigdict["ENABLE_MAIL_NOTI"]:
            logging.info("发送错误通知邮件")
            try:
                # 构造通知对象
                notificationer = create_notificationer()
                # 构造邮件内容
                content = []
                content.append("HBM任务错误")
                content.append("配置文件名称: " + config.nowuserconfigname)
                content.append("错误信息: " + str(e))
                logging.info(notificationer.send("\n".join(content), title="HBM任务失败"))
                logging.info("邮件发送结束")
            except Exception as eagain:
                logging.error("发送邮件失败")
                logging.error(eagain)

    def HBM_main(run_precommand = True):
        """
        执行HBM主程序, 在此之前config应该已经被单独import然后解析为用户指定的配置文件->随后再导入my_AllTask以及其他依赖config的模块
        """
        try:
            # 同级别的except只能捕获同级别的try里的错误
            try:
                config.sessiondict["HBM_START_TIME"] = time.strftime("%Y-%m-%d %H:%M:%S")
                print_HBM_info()
                print_HBM_config_info()
                if run_precommand:
                    HBM_run_pre_command()
                HBM_release_adb_port()
                HBM_start_emulator()
                HBM_check_adb_connect()
                HBM_open_target_app()
                
                # 运行任务
                logging.info("运行任务")
                my_AllTask.run()
                logging.info("所有任务结束")
                HBM_close_target_app()
                HBM_kill_emulator()
                HBM_send_email()
                print_HBM_finish()
                HBM_rm_pic()
                HBM_run_post_command()
                
                print_HBM_config_info()
                HBM_auto_quit()

            except EmulatorBlockError as ebe:
                logging.info("模拟器卡顿，重启模拟器")
                if config.sessiondict["EMULATOR_PROCESS_PID"] is None:
                    raise Exception("无模拟器pid，无法重启模拟器，请确保模拟器由HBM启动")
                # sessionstorage里重启次数加1
                store_restart_times = config.sessiondict["RESTART_EMULATOR_TIMES"] + 1
                HBM_kill_emulator(must_do=True)
                time.sleep(30)
                # 重新加载其他config值，覆盖模拟器重启次数到sessiondict
                config.parse_user_config(config.nowuserconfigname)
                config.sessiondict["RESTART_EMULATOR_TIMES"] = store_restart_times
                # 防止重复调用precommand
                HBM_main(run_precommand=False)

        # 最外层的except捕获正常运行过程中的错误 以及 模拟器重启次数达到最大值的错误
        except Exception as e:
            logging.error(f"运行出错: {e}")
            # 打印完整的错误信息
            import traceback
            # 打印错误信息, 保存日志信息到文件
            detailed_trackback_str = traceback.format_exc()
            logging.error(detailed_trackback_str)
            logging.save_custom_log_file()
            # 发送错误邮件
            HBM_send_err_mail(e)
            print_HBM_finish()
            
            print_HBM_config_info()
            HBM_auto_quit(forcewait=True, key_map_func={
                "R": {
                    "desc":"estart", # [R]estart
                    "func":lambda: [config.parse_user_config(config.nowuserconfigname), HBM_main()]
                      }
            })


    # Run
    HBM_main()


def HBM_single_func_process(reread_config_name = None, msg_queue = None, to_run_func_config_name = None):
    """
    快捷执行某一个函数的wrapped方法
    """
    if to_run_func_config_name is None:
        raise Exception("to_run_func_config_name is None")
    
    # ============= Initialize =============
    from modules.configs.MyConfig import config
    if reread_config_name is not None:
        config.parse_user_config(reread_config_name)
    
    from modules.utils.log_utils import logging
    logging.set_log_queue(msg_queue)

    # ============= Import =============

    from modules.utils import check_connect
    from modules.AllTask.myAllTask import task_instances_map

    if to_run_func_config_name not in task_instances_map.taskmap:
        raise Exception(f"to_run_func_config_name: {to_run_func_config_name} not in task_instances_map.taskmap")
    
    # 执行
    try:
        print("to_run_func_config_name: ", to_run_func_config_name)
        task_ins = task_instances_map.taskmap[to_run_func_config_name]
        module_func = task_ins.task_module
        params_func = task_ins.task_params
        check_connect()
        module_func(**params_func).run()
    except Exception as e:
        logging.error(f"运行出错: {e}")
        # 打印完整的错误信息
        import traceback
        # 打印错误信息
        detailed_trackback_str = traceback.format_exc()
        logging.error(detailed_trackback_str)