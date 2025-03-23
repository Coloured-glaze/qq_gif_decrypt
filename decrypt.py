
import argparse, os

def decrypt_gif_header(encrypted_header):
    decrypted_header = ''
    for i in range(0, len(encrypted_header), 4):
        # 将16进制字符串转换为数字
        hex_value = int(encrypted_header[i:i+4], 16)
        # 偶数则+1，奇数则-1
        if hex_value % 2 == 0:
            hex_value += 1
        else:
            hex_value -= 1
        # 将数字转换回16进制字符串，并添加到解密头部
        decrypted_header += '{:04x}'.format(hex_value)
    return decrypted_header

def decrypt_gif_file(input_file_path, output_folder, output_file_name):
    with open(input_file_path, 'rb') as encrypted_gif:
        # 读取加密的GIF文件内容
        encrypted_content = encrypted_gif.read()
        # 找到GIF文件头结束的位置（通常是GIF89a之后）
        # header_end_index = encrypted_content.find(b'GHF99`') + 10
        header_end_index = 20 # 头 
        # 解密文件头
        decrypted_header = decrypt_gif_header(encrypted_content[:header_end_index].hex())
        # 将解密的文件头和原始文件的其余部分合并
        decrypted_content = bytes.fromhex(decrypted_header) + encrypted_content[header_end_index:] + bytes(00) + bytes(00) # 填充数据空白
        # 保存解密后的GIF文件
        with open(os.path.join(output_folder, output_file_name), 'wb') as decrypted_gif:
            decrypted_gif.write(decrypted_content)

# 使用示例
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', type=str, default="", help="目标文件夹")
    param, _ = parser.parse_known_args()

    if len(_): 
        print(f"unknown args: {_}")
    if not os.path.exists(param.folder):
        print(f"folder not exists: {param.folder}"); exit(1)

    output_folder = os.path.join(param.folder, "output"); 
    os.makedirs(output_folder, exist_ok=True)

    for file in os.listdir(param.folder):
        file_path = os.path.join(param.folder, file)
        if os.path.isfile(file_path):  # 仅处理文件（排除子目录）
            decrypt_gif_file(file_path, output_folder, file + '.gif')
            print(f'{file_path} -> {os.path.join(output_folder, file)}.gif')
    print()
