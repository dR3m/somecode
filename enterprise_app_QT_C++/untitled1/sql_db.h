#ifndef SQL_DB_H
#define SQL_DB_H

#include <iostream>
#include <QtSql>
using namespace std;
class DataBase
{
public:
    QSqlDatabase db;

    DataBase(){}
    int addWorker(const QString &name, QDate start_date, int base_rate, int type);
    bool setBoss(int worker_id,  int boss_id);
    bool setPosition(int worker_id,  int position_type);
    QSqlDatabase connect();
    QSqlQuery getSlaves(int worker_id);
    QSqlQuery getSlaves(int worker_id, int level);
    QSqlQuery getAllStuff();
    QSqlRecord getData(int id);
    int calculateAllStuffSalary(QDate some_date);
    int getBoss(int id);

private:
    QSqlError initDb();
};




#endif // SQL_DB_H
