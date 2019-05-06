/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 4.8.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtGui/QApplication>
#include <QtGui/QButtonGroup>
#include <QtGui/QComboBox>
#include <QtGui/QHeaderView>
#include <QtGui/QLabel>
#include <QtGui/QLineEdit>
#include <QtGui/QListWidget>
#include <QtGui/QMainWindow>
#include <QtGui/QMenuBar>
#include <QtGui/QPushButton>
#include <QtGui/QStatusBar>
#include <QtGui/QTableView>
#include <QtGui/QTextBrowser>
#include <QtGui/QToolBar>
#include <QtGui/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QTableView *stuffList;
    QListWidget *listWidget;
    QLabel *label_2;
    QTextBrowser *textBrowser;
    QLabel *label_3;
    QComboBox *typeBox;
    QPushButton *addWorkerButton;
    QComboBox *bossBox;
    QLineEdit *nameField;
    QLineEdit *salaryField;
    QLabel *label_4;
    QLabel *label_5;
    QLabel *label_6;
    QLabel *label_7;
    QLabel *label_8;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QString::fromUtf8("MainWindow"));
        MainWindow->resize(942, 526);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QString::fromUtf8("centralWidget"));
        stuffList = new QTableView(centralWidget);
        stuffList->setObjectName(QString::fromUtf8("stuffList"));
        stuffList->setGeometry(QRect(10, 10, 581, 291));
        listWidget = new QListWidget(centralWidget);
        listWidget->setObjectName(QString::fromUtf8("listWidget"));
        listWidget->setGeometry(QRect(10, 330, 581, 91));
        label_2 = new QLabel(centralWidget);
        label_2->setObjectName(QString::fromUtf8("label_2"));
        label_2->setGeometry(QRect(10, 310, 151, 16));
        textBrowser = new QTextBrowser(centralWidget);
        textBrowser->setObjectName(QString::fromUtf8("textBrowser"));
        textBrowser->setGeometry(QRect(90, 430, 501, 31));
        label_3 = new QLabel(centralWidget);
        label_3->setObjectName(QString::fromUtf8("label_3"));
        label_3->setGeometry(QRect(10, 440, 151, 16));
        typeBox = new QComboBox(centralWidget);
        typeBox->setObjectName(QString::fromUtf8("typeBox"));
        typeBox->setGeometry(QRect(610, 120, 211, 31));
        addWorkerButton = new QPushButton(centralWidget);
        addWorkerButton->setObjectName(QString::fromUtf8("addWorkerButton"));
        addWorkerButton->setGeometry(QRect(610, 200, 211, 51));
        bossBox = new QComboBox(centralWidget);
        bossBox->setObjectName(QString::fromUtf8("bossBox"));
        bossBox->setGeometry(QRect(610, 160, 211, 31));
        nameField = new QLineEdit(centralWidget);
        nameField->setObjectName(QString::fromUtf8("nameField"));
        nameField->setGeometry(QRect(610, 40, 211, 31));
        salaryField = new QLineEdit(centralWidget);
        salaryField->setObjectName(QString::fromUtf8("salaryField"));
        salaryField->setGeometry(QRect(610, 80, 211, 31));
        label_4 = new QLabel(centralWidget);
        label_4->setObjectName(QString::fromUtf8("label_4"));
        label_4->setGeometry(QRect(830, 80, 111, 21));
        label_5 = new QLabel(centralWidget);
        label_5->setObjectName(QString::fromUtf8("label_5"));
        label_5->setGeometry(QRect(610, 10, 261, 21));
        QFont font;
        font.setPointSize(11);
        font.setBold(true);
        font.setWeight(75);
        label_5->setFont(font);
        label_6 = new QLabel(centralWidget);
        label_6->setObjectName(QString::fromUtf8("label_6"));
        label_6->setGeometry(QRect(830, 40, 101, 21));
        label_7 = new QLabel(centralWidget);
        label_7->setObjectName(QString::fromUtf8("label_7"));
        label_7->setGeometry(QRect(830, 120, 101, 21));
        label_8 = new QLabel(centralWidget);
        label_8->setObjectName(QString::fromUtf8("label_8"));
        label_8->setGeometry(QRect(830, 160, 101, 21));
        MainWindow->setCentralWidget(centralWidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName(QString::fromUtf8("menuBar"));
        menuBar->setGeometry(QRect(0, 0, 942, 19));
        MainWindow->setMenuBar(menuBar);
        mainToolBar = new QToolBar(MainWindow);
        mainToolBar->setObjectName(QString::fromUtf8("mainToolBar"));
        MainWindow->addToolBar(Qt::TopToolBarArea, mainToolBar);
        statusBar = new QStatusBar(MainWindow);
        statusBar->setObjectName(QString::fromUtf8("statusBar"));
        MainWindow->setStatusBar(statusBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MainWindow", 0, QApplication::UnicodeUTF8));
        label_2->setText(QApplication::translate("MainWindow", "\320\237\320\276\320\264\321\207\320\270\320\275\321\221\320\275\320\275\321\213\320\265", 0, QApplication::UnicodeUTF8));
        label_3->setText(QApplication::translate("MainWindow", "\320\235\320\260\321\207\320\260\320\273\321\214\320\275\320\270\320\272", 0, QApplication::UnicodeUTF8));
        typeBox->clear();
        typeBox->insertItems(0, QStringList()
         << QApplication::translate("MainWindow", "Employer", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("MainWindow", "Manager", 0, QApplication::UnicodeUTF8)
         << QApplication::translate("MainWindow", "Sales", 0, QApplication::UnicodeUTF8)
        );
        addWorkerButton->setText(QApplication::translate("MainWindow", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \321\201\320\276\321\202\321\200\321\203\320\264\320\275\320\270\320\272\320\260", 0, QApplication::UnicodeUTF8));
        label_4->setText(QApplication::translate("MainWindow", "\320\221\320\260\320\267\320\276\320\262\320\260\321\217 \321\201\321\202\320\260\320\262\320\272\320\260", 0, QApplication::UnicodeUTF8));
        label_5->setText(QApplication::translate("MainWindow", "\320\224\320\276\320\261\320\260\320\262\320\270\321\202\321\214 \320\275\320\276\320\262\320\276\320\263\320\276 \321\201\320\276\321\202\321\200\321\203\320\264\320\275\320\270\320\272\320\260", 0, QApplication::UnicodeUTF8));
        label_6->setText(QApplication::translate("MainWindow", "\320\230\320\274\321\217", 0, QApplication::UnicodeUTF8));
        label_7->setText(QApplication::translate("MainWindow", "\320\224\320\276\320\273\320\266\320\275\320\276\321\201\321\202\321\214", 0, QApplication::UnicodeUTF8));
        label_8->setText(QApplication::translate("MainWindow", "id \320\275\320\260\321\207\320\260\320\273\321\214\320\275\320\270\320\272\320\260", 0, QApplication::UnicodeUTF8));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
