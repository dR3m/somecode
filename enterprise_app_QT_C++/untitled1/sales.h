#ifndef SALES_H
#define SALES_H

#include "worker.h"

class Sales: public Worker
{
public:
    Sales(int id, DataBase db):Worker(id, db){}
    int calculateSalary(QDate some_date);
    int countSlaves(QDate some_date);
};

#endif // SALES_H
