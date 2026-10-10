@echo off
setlocal enabledelayedexpansion

REM 配置参数
set PIDs=2104 6680 5236 11560 11936 4516 17880
set duration=120      
set interval=1     

REM 初始化统计变量
set /a "sum_cpu=0, sum_mem=0, count=0"

REM 获取初始CPU时间
for %%p in (%PIDs%) do (
    for /f "tokens=1* delims==" %%A in ('wmic process where processid^="%%p" get KernelModeTime^,UserModeTime^,WorkingSetSize /value ^| findstr "=" 2^>nul') do (
        for /f "delims=" %%C in ("%%B") do set "old_%%p_%%A=%%C"
    )
)

:loop
REM 使用兼容性等待方案
where timeout >nul 2>nul
if %errorlevel% equ 0 (
    timeout /T %interval% /NOBREAK >nul
) else (
    set /a "ping_count=interval*10"
    ping -n !ping_count! 127.0.0.1 >nul
)

set total_cpu=0
set total_mem=0

REM 采集数据
for %%p in (%PIDs%) do (
    set "new_kernel=" & set "new_user=" & set "new_mem="
    
    REM 获取新时间
    for /f "tokens=1* delims==" %%A in ('wmic process where processid^="%%p" get KernelModeTime^,UserModeTime^,WorkingSetSize /value ^| findstr "=" 2^>nul') do (
        for /f "delims=" %%C in ("%%B") do set "new_%%A=%%C"
    )
    
    if defined new_KernelModeTime (
        REM 计算CPU使用率（避免中间结果溢出）
        set /a "old_time=old_%%p_KernelModeTime + old_%%p_UserModeTime"
        set /a "new_time=new_KernelModeTime + new_UserModeTime"
        set /a "delta_time=new_time - old_time"
        
        REM 调整计算顺序：先除法再乘法
        set /a "cpu=(delta_time / (interval * 100000))"
        set /a "total_cpu+=cpu"
        
        REM 更新旧时间
        set "old_%%p_KernelModeTime=!new_KernelModeTime!"
        set "old_%%p_UserModeTime=!new_UserModeTime!"
    )
    
    if defined new_WorkingSetSize (
        REM 内存直接以MB为单位累加
        set /a "total_mem+=new_WorkingSetSize / 1048576"
    )
)

REM 累计统计
set /a "sum_cpu+=total_cpu"
set /a "sum_mem+=total_mem"
set /a "count+=1"

REM 显示实时信息
set /a "elapsed=count*interval"
cls
echo [Progress] !elapsed!/%duration% s
echo [Interval] %interval% s
echo [PIDs] %PIDs%
echo --------------------------
echo CPU Usage: !total_cpu!%%
echo MEM Usage: !total_mem! MB
echo ===========================

REM 检查是否超时
if !elapsed! lss %duration% goto loop

REM 计算并显示报告
set /a "avg_cpu=sum_cpu/count"
set /a "avg_mem=sum_mem/count"

echo.
echo ======= Final Report =======
echo Duration: %duration% seconds
echo Samples: !count!
echo --------------------------
echo Average CPU: !avg_cpu!%%
echo Average MEM: !avg_mem! MB
echo ===========================
pause
endlocal