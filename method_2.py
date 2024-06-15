import shutil
import os
# ------------
print("2")
#скрипт від софії
file = os.listdir('C:/Users/ACER/Desktop/НН ФТІ/Com. graf/Project/media_users/document_in/method2')[-1]

file_path = f"C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_in\method2\\{file}"
destination_path = f"C:\\Users\ACER\Desktop\НН ФТІ\Com. graf\Project\media_users\document_out\method2\\{file}"

shutil.copy(file_path, destination_path)