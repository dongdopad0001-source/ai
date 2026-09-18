from streamlit.web import cli as stcli
import sys
    # 현재 실행 중인 파일의 경로를 자동으로 입력합니다.
sys.argv = ["streamlit", "run", "main.py"]
sys.exit(stcli.main())