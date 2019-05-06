#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDataWidgetMapper>
#include <QtSql>
#include "sql_db.h"

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_stuffList_doubleClicked(const QModelIndex &index);
    void on_addWorkerButton_released();

private:
    Ui::MainWindow *ui;
    QSqlRelationalTableModel *model;
    QDataWidgetMapper *mapper;
    int typeIdx;
    DataBase *dbObj = new DataBase();

    void getAllBosses();
};

#endif // MAINWINDOW_H
