#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QMessageBox>
#include <QApplication>
#include <QSqlTableModel>
#include <QTableView>
#include <QListWidget>
#include <QDate>

#include <stdlib.h>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    dbObj->connect();
    if(!dbObj->db.isOpen())
        return;

    model = new QSqlRelationalTableModel(this);
    model->setTable("stuff");
    model->setEditStrategy(QSqlTableModel::OnManualSubmit);

    typeIdx = model->fieldIndex("type");
    model->setRelation(typeIdx,QSqlRelation("positions", "type", "description"));
    model->select();

    model->setHeaderData(0, Qt::Horizontal, QObject::tr("ID"));
    model->setHeaderData(1, Qt::Horizontal, QObject::tr("Name"));
    model->setHeaderData(2, Qt::Horizontal, QObject::tr("Start date"));
    model->setHeaderData(3, Qt::Horizontal, QObject::tr("Base salary"));
    model->setHeaderData(4, Qt::Horizontal, QObject::tr("Position"));

    ui->stuffList->setModel(model);
    ui->stuffList->setItemDelegate(new QSqlRelationalDelegate(this));
    ui->stuffList->setSelectionBehavior(QAbstractItemView::SelectRows);

    getAllBosses();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::getAllBosses(){
    QSqlQuery q;
    q.exec("select id from stuff where type!=0");
    while (q.next()) {
        ui->bossBox->addItem(q.value(0).toString(), q.value(0));
    }
}

void MainWindow::on_stuffList_doubleClicked(const QModelIndex &index)
{
    QSqlQuery q = dbObj->getSlaves(index.row()+1);
    QSqlQuery q2(dbObj->db);
    ui->listWidget->clear();
    ui->textBrowser->clear();
    while(q.next()){
        q2.prepare(QLatin1String("select name from stuff where id=?"));
        q2.bindValue(0, q.value(0).toInt());
        q2.exec();
        q2.first();
        QString name = q2.value(0).toString();
        ui->listWidget->addItem(name);
    }

    q2.clear();
    q2.prepare(QLatin1String("select name from stuff where id=?"));
    q2.bindValue(0, dbObj->getBoss(index.row()+1));
    q2.exec();
    q2.first();
    ui->textBrowser->setText(q2.value(0).toString());
}

void MainWindow::on_addWorkerButton_released()
{
    QString name = ui->nameField->text();
    int base_salary = ui->salaryField->text().toInt();
    int type = ui->typeBox->currentIndex();

    if(!name.isEmpty() && base_salary>1000){
        int id = dbObj->addWorker(name, QDate::currentDate(),base_salary, type);
        dbObj->setBoss(id, ui->bossBox->currentText().toInt());
     }
    model->select();
    getAllBosses();
}
