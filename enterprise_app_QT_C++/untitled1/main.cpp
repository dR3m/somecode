#include "mainwindow.h"
#include <QApplication>
#include "employer.h"
#include "manager.h"
#include "sales.h"
#include "sql_db.h"

void fillDB(DataBase db){
    int id = 0;
    id = db.addWorker("Vova", QDate(2015, 12, 27), 15000, 0);
    db.setBoss(id, 3);
    id = db.addWorker("Petya", QDate(2016, 1, 27), 15000, 0);
    db.setBoss(id, 3);
    id = db.addWorker("Vasya", QDate(2017, 4, 27), 18000, 1);
    db.setBoss(id, 4);
    id = db.addWorker("Natasha", QDate(2018, 4, 27), 18000, 1);
    db.setBoss(id, 5);
    id = db.addWorker("Olya", QDate(2011, 5, 27), 20000, 2);
    db.setBoss(id, 6);
    id = db.addWorker("Katya", QDate(2011, 1, 27), 20000, 2);
    db.setBoss(id, 5);
    id = db.addWorker("Kolya", QDate(2014, 12, 27), 18000, 1);
    db.setBoss(id, 3);
    id = db.addWorker("Dana", QDate(2016, 10, 27), 15000, 0);
    db.setBoss(id, 7);
    id = db.addWorker("Tolya", QDate(2015, 12, 27), 15000, 0);
    db.setBoss(id, 6);
    id = db.addWorker("Dasha", QDate(2016, 1, 27), 15000, 0);
    db.setBoss(id, 6);
    id = db.addWorker("Pupkin", QDate(2017, 4, 27), 18000, 1);
    db.setBoss(id, 7);
    id = db.addWorker("Daniil", QDate(2018, 4, 27), 18000, 1);
    db.setBoss(id, 3);
    id = db.addWorker("Denis", QDate(2011, 5, 27), 20000, 2);
    db.setBoss(id, 11);
    id = db.addWorker("Danisa", QDate(2011, 1, 27), 20000, 2);
    db.setBoss(id, 13);
    id = db.addWorker("Anna", QDate(2014, 12, 27), 18000, 1);
    db.setBoss(id, 13);
    id = db.addWorker("Elsa", QDate(2016, 10, 27), 15000, 0);
    db.setBoss(id, 12);
}

void calcSalary(){
    DataBase db;
    db.connect();
    int sm = db.calculateAllStuffSalary(QDate(2018, 12, 27));
    printf("All stuff salary %d\n", sm);

    Employer *e = new Employer(1, db);
    e->calulate_salary(QDate(2018, 12, 27));

    Manager *m = new Manager(3, db);
    m->calculateSalary(QDate(2018, 12, 27));

    Sales *s = new Sales(5, db);
    s->calculateSalary(QDate(2018, 12, 27));
}

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
