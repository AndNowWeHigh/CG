import shutil
import os
# ------------
print("1")
#скрипт від софії
file = os.listdir('C:/Users/ACER/Desktop/НН ФТІ/Com. graf/Project/media_users/document_in/method1')[-1]

file_path = f"C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method1\\{file}"
destination_path = f"C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_out\method1\\{file}"

shutil.copy(file_path, destination_path)

