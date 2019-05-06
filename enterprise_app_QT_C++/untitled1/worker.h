#ifndef WORKER_H
#define WORKER_H

#include <QDate>
#include "sql_db.h"
#include <iostream>

using namespace std;

class Worker
{
public:
    int id;
    string name;
    QDate start_date;
    int base_salary;

    Worker(int id, DataBase db){
        this -> id = id;
        this -> db = db;
        QSqlRecord q = db.getData(id);
        if(!q.isEmpty()){
            this -> name = q.value(1).toString().toStdString();
            this -> start_date = q.value(2).toDate();
            this -> base_salary = q.value(3).toInt();
        }
        else {
            printf("%s", "No such worker\n");
        }
    }

    virtual int calculateSalary(QDate some_date) {return 0;}
    virtual int countSlaves(QDate some_date) {return 0;}

    int experience(QDate some_date){
        return this -> start_date.daysTo(some_date)/365; //не учтён високосный год
    }

protected:
    DataBase db;
};

#endif // WORKER_H
