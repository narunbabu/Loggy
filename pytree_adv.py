import sys

# from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QTreeWidget,QTreeWidgetItem,QApplication)

def main(): 
    treeview_dict={
        'MD':{
            'LWD':{
                'a':['file4','200-500','43','gr mfs'],
                'b':['file5','300-450','54','gr mfs']
            },
            'WireLine':{
                'c':['file6','450-670','2','gr mfs']
            }

        },
        'TVD':{
            'LWD':{
                'a1':['file1','123-789','45','gr mfs'],
                'b1':['file2','234-456','23','gr mfs']
            },
            'WireLine':{
                'c1':['file3','124-789','12','gr mfs']
            }

        }
        
    }
    app     = QApplication (sys.argv)


    tree    = QTreeWidget ()
    item    = QTreeWidgetItem()

    tree.headerItem().setText(0, "File name")
    tree.headerItem().setText(1, "Depth Range")
    tree.headerItem().setText(2, "No of Logs")
    tree.headerItem().setText(3, "Log Names")

    for key in treeview_dict:
        parent = QTreeWidgetItem(tree)
        parent.setText(0, key)
        # parent.setFlags(parent.flags() | Qt.ItemIsTristate )
        parent.setFlags(parent.flags())
        
        for subkey in treeview_dict[key]:
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags()  )
            # child.setFlags(child.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            child.setText(0, subkey)
            # child.setCheckState(0, Qt.Unchecked)
            for thirdkey in treeview_dict[key][subkey]:
                subchild = QTreeWidgetItem(child)
                subchild.setFlags(child.flags()  | Qt.ItemIsUserCheckable)
                subchild.setText(0, thirdkey)
                subchild.setCheckState(0, Qt.Unchecked)

                #create the checkbox
                finaldict=treeview_dict[key][subkey][thirdkey]
                # for fourthkey in finaldict:
                for i,descr in enumerate(finaldict):
                    # if i < 3:
                    subchild.setText(i, descr)
                        # subchild.setCheckState(i, Qt.Unchecked)
                    # if i == 3:
                    #     subchild.setText(i, "Any Notes?")
                    #     subchild.setFlags(subchild.flags() | Qt.ItemIsEditable)

    tree.show() 
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()