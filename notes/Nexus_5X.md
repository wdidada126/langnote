Nexus 5X 进入bootloader和recovery的方法
进bootloader 电源键+音量减键

fastboot flash recovery twrp-3.2.1-0-bullhead.img

adb shell settings put secure user_setup_complete 1

adb push addonsu-15.1-arm64-signed.zip /sdcatd

adb push addonsu-remove-15.1-arm64-signed.zip /sdcatd