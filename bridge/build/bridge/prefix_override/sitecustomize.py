import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/manuelavillamizar/project_ws/src/bridge/install/bridge'
