import fitz  # 引入 PyMuPDF

def crop_pdf_top_bottom_left(input_pdf, output_pdf, bottom_crop_ratio, top_crop_ratio, left_crop_ratio):
    """
    从顶部、底部和左侧裁剪 PDF 文件。

    :param input_pdf: 输入的 PDF 文件路径
    :param output_pdf: 输出的 PDF 文件路径
    :param bottom_crop_ratio: 要从底部裁剪的比例（例如 0.1 表示裁剪底部的 10%）
    :param top_crop_ratio: 要从顶部裁剪的比例（例如 1/12 表示裁剪顶部的约 8.33%）
    :param left_crop_ratio: 要从左侧裁剪的比例（例如 0.1 表示裁剪左侧的 10%）
    """
    doc = fitz.open(input_pdf)  # 打开 PDF 文件
    for page in doc:
        rect = page.rect  # 获取当前页面的完整尺寸
        # 计算裁剪的尺寸
        crop_height_bottom = rect.height * bottom_crop_ratio
        crop_height_top = rect.height * top_crop_ratio
        crop_width_left = rect.width * left_crop_ratio
        # 创建新的裁剪框
        crop_rect = fitz.Rect(rect.x0 + crop_width_left, rect.y0 + crop_height_top, rect.x1, rect.y1 - crop_height_bottom)
        page.set_cropbox(crop_rect)  # 设置新的裁剪框
    doc.save(output_pdf)  # 保存裁剪后的 PDF
    doc.close()  # 关闭文档

# 使用示例
input_pdf_path = "subject_distribution.pdf"  # 输入文件名
output_pdf_path = "output_subject_distribution.pdf"  # 输出文件名
crop_pdf_top_bottom_left(input_pdf_path, output_pdf_path, 1/12, 1/15, 1/20)  # 同时裁剪底部的 10%、顶部的约 8.33% 和左侧的 10%

# 使用示例
input_pdf_path = "data_source_distribution.pdf"  # 输入文件名
output_pdf_path = "output_data_source_distribution.pdf"  # 输出文件名
crop_pdf_top_bottom_left(input_pdf_path, output_pdf_path, 1/12, 1/15, 1/20)  # 同时裁剪底部的 10%、顶部的约 8.33% 和左侧的 10%