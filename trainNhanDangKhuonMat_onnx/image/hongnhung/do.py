import os

def rename_to_lowercase(directory):
    # Lặp qua tất cả file trong thư mục
    for filename in os.listdir(directory):
        # Đường dẫn đầy đủ đến file
        old_file = os.path.join(directory, filename)
        
        # Chỉ xử lý file, không xử lý thư mục
        if os.path.isfile(old_file):
            # Chuyển tên file thành chữ thường
            new_filename = filename.lower()
            new_file = os.path.join(directory, new_filename)
            
            # Đổi tên file
            try:
                os.rename(old_file, new_file)
                print(f"Đã đổi tên: {filename} -> {new_filename}")
            except Exception as e:
                print(f"Lỗi khi đổi tên {filename}: {e}")

# Thay đổi đường dẫn thư mục tại đây
directory_path = "./"
rename_to_lowercase(directory_path)