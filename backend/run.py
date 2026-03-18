#!/usr/bin/env python3
# DramaPipeline Flask 应用启动入口
# @author fortune
# @date 2026-03-18 21:55:00

import os
from dotenv import load_dotenv

# 加载 .env（项目根目录）
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app import create_app

app = create_app()

if __name__ == '__main__':
    # 输出启动成功的 ASCII 艺术字提示
    print(" __ __ _ _ _ _ __ _ _____ _____ ")
    print(" \\ \\ / / | | | | | | | | | \\ | | | ____| |_ _| ")
    print(" \\ \\/ / | | | | | | | | | \\| | | |__ | | ")
    print(" \\ / | | _ | | | | | | | |\\ | | __| | | ")
    print(" / / | | | |_| | | |_| | | | \\ | | |___ | | ")
    print(" /_/ |_| \\_____/ \\_____/ |_| \\_| |_____| |_| ")
    print(" _____ _____ _____ _____ ___ _____ _____ _____ _ _ ")
    print(" / _ \\ / _ \\ |___ | / _ \\ |_ | | ___| / _ \\ / ___| | | | | ")
    print(" | | | | | | | | | / / | |_| | | | | |___ | |_| | | |___ | |_| | ")
    print(" | | | | | | | | | / / } _ { | | \\___ \\ \\___ | | _ \\ \\___ | ")
    print(" | |_| |_ | |_| |_ / / | |_| | | | ___| | ___| | | |_| | | | ")
    print(" \\_______| \\_______| /_/ \\_____/ |_| \\_____| |_____/ \\_____/ |_| ")
    print(" -----------===========(♥◠‿◠)ﾉﾞ DramaPipeline 启动成功 ლ(´ڡ`ლ)ﾞ ============----------- ")

    # 默认 5001，macOS 上 5000 常被 AirPlay 占用
    port = int(os.getenv('FLASK_PORT', '5001'))
    app.run(host='0.0.0.0', port=port, debug=True)
