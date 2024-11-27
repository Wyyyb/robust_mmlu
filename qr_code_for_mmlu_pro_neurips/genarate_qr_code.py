import qrcode


def create_qr_code(url, output_path='qrcode.png'):
    # 创建QR码对象
    qr = qrcode.QRCode(
        version=1,  # 二维码的尺寸大小(1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 错误纠正水平
        box_size=10,  # 每个格子的像素大小
        border=4  # 二维码边框宽度
    )

    # 添加数据
    qr.add_data(url)
    qr.make(fit=True)

    # 创建图像
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # 保存图像
    qr_image.save(output_path)


# 使用示例
url = "https://huggingface.co/spaces/TIGER-Lab/MMLU-Pro"
create_qr_code(url, "mmlu-pro_qr.png")


