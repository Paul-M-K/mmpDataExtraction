import os

filesRename = ['demo_1.txt', 'demo_2.txt', 'demo_3.txt',]
folder = "C:\\Users\\pauru\\source\\GBA"

# Iterate
for file in os.listdir(folder):
	# Checking if the file is present in the list
	if file in filesRename:
		oldName = os.path.join(folder, file)
		n = os.path.splitext(file)[0]

		b = n + '_new' + '.txt'
		newName = os.path.join(folder, b)

		# Rename the file
		os.rename(oldName, newName)

res = os.listdir(folder)
print(res)