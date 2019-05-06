#ifndef EMPLOYER_H
#define EMPLOYER_H

#include "worker.h"
#include <QDate>

class Employer: public Worker
{
public:
    Employer(int id,DataBase db):Worker(id, db){}
    int calulate_salary(QDate some_date);
    int countSlaves() {return 0;}
};

#endif // EMPLOYER_H
