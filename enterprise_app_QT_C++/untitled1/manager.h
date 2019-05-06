#ifndef MANAGER_H
#define MANAGER_H

#include "worker.h"

class Manager: public Worker
{
public:
    Manager(int id, DataBase db):Worker(id, db){}
    int calculateSalary(QDate some_date);
    int countSlaves(QDate some_date);
};

#endif // MANAGER_H
