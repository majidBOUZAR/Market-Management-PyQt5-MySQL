from PyQt5.QtWidgets import QComboBox, QApplication

app = QApplication([])
comboBox = QComboBox()
comboBox.addItem("Item 1")
comboBox.addItem("Item 2")
comboBox.addItem("Item 1")
comboBox.addItem("Item 3")
comboBox.addItem("Item 2")

unique_items = []
for i in range(comboBox.count()):
    item = comboBox.itemText(i)
    if item not in unique_items:
        unique_items.append(item)
    else:
        comboBox.removeItem(i)

print("All unique items:", unique_items)

app.exec_()
