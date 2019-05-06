#ifndef INTERFACE_H
#define INTERFACE_H

#include <QDialog>
#include <QSqlTableModel>
#include <QDataWidgetMapper>
#include <QMessageBox>

#include "sql_db.h"

namespace Ui {
class DialogAddDevice;
}
class Interface: public QDialog
{
    Q_OBJECT

public:
    explicit Interface(int row = -1, QWidget *parent = nullptr);
    ~Interface();

signals:
    void signalReady();

private slots:
    void on_buttonBox_accepted();
    void updateButtons(int row);

private:
    Ui::DialogAddDevice *ui;
    QSqlTableModel      *model;
    QDataWidgetMapper   *mapper;

private:
    void setupModel();
    void createUI();
    void accept();
};


#endif // INTERFACE_H
