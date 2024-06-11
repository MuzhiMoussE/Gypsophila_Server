import socket
import os
import subprocess
import threading
# 创建一个socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取主机名
host = '127.0.0.1'
# 设置端口
port = 9999
# 绑定到端口
server_socket.bind((host, port))

# 设置最大连接数，超过后排队
server_socket.listen(5)
cnt = 0

def send_files(output_dir):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((host, 9998))
    # 获取output_dir目录下的所有文件
    files = os.listdir(output_dir+'/sequence')
    # 对文件进行排序，确保按正确的顺序发送
    files.sort(key=lambda x: int(x[6:-4]))
    print("Sending files...")
    for file in files:
        # 只发送图片文件
        if file.endswith('.png'):
            # 打开文件
            with open(os.path.join(output_dir+'/sequence', file), 'rb') as f:
                # 读取文件内容
                data = f.read()
                
                # 发送文件内容
                _socket.sendall(data)
                print(f"Sending file: {file}") 
                # 发送一个分隔符，用于在客户端区分不同的文件
                #_socket.sendall(b'FILE_SEPARATOR')
    # 发送结束信号
    _socket.sendall(b'END')
    print("Files sent over...")
    _socket.close()


while True:
    print("等待新的连接...")
    # 建立客户端连接
    client_socket, addr = server_socket.accept()

    print("连接地址: %s" % str(addr))

    # 接收客户端发送的数据
    data = b""
    while True:
        part = client_socket.recv(1024)
        if part:
            data += part
        else:
            break
    #print("接收到的数据: %s" % data)
        
    # 检查数据是否完整
    #if data[:4] != b'\x89PNG' or data[-12:] != b'IEND\xAE\x42\x60\x82':
    #    print("---Incomplete data received. Skipping...---")
    #    continue
    
    print("Writing...")
    # 检查目录是否存在，不存在则创建
    if not os.path.exists('examples/receive'):
        os.makedirs('examples/receive')
    # 将数据写入到文件中
    with open(os.path.join('examples/receive/', str(cnt)+'.png'), 'wb') as f:
        f.write(data)

    print("Write over...")
    print("Start generating...")

    # 运行 image_to_animation.py 脚本
    output_dir = 'examples/send/output'+str(cnt)  # 你的输出文件夹
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    
    # 获取当前脚本的父目录
    parent_dir = os.path.dirname(os.path.abspath(__file__))

    # 构建image_to_animation.py脚本的路径
    script_path = os.path.join(parent_dir, 'image_to_animation.py')
    # 运行脚本
    subprocess.run(['python', script_path, 'examples/receive/'+str(cnt)+'.png', output_dir])
    print("Generate over...")    
    client_socket.close()
    print("---------------------------")
    print("Start sending...")

    # 创建一个新的线程来发送文件
    thread = threading.Thread(target=send_files, args=(output_dir,))
    # 启动新的线程
    thread.start()

    print("End signal sent...")
    print("Data sent...")
    # 关闭连接
    #client_socket.close()
    cnt += 1
