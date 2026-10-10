def main():
    # Use freeze_support to avoid running GUI again: https://blog.csdn.net/fly_leopard/article/details/121610641
    import multiprocessing
    multiprocessing.freeze_support()
    if not multiprocessing.get_start_method(allow_none=True):
        from gui.components.exec_arg_parse import parse_args
        from nicegui import ui, app
        
        print("GUI is running...")
        args = parse_args()
        ui.run(title=f"HBM", language="zh-cn",
            reload=False, host=args.host, port=args.port, show=args.show,favicon="DATA\\icons\\hb.ico")

if __name__ in {"__main__", "__mp_main__"}:
    main()
