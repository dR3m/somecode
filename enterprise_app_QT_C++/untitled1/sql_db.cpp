#include "sql_db.h"
#include <iostream>
#include "sales.h"
#include "employer.h"
#include "manager.h"

QSqlDatabase DataBase::connect(){
    initDb();
    return this->db;
}

QSqlError DataBase::initDb()
{

    QSqlDatabase db = QSqlDatabase::addDatabase("QSQLITE");
    db.setDatabaseName("stuff.db");
    if (!db.open())
        return db.lastError();
    this -> db = db;
    cout << "DB connected" << endl;

    QStringList tables = db.tables();
    if (tables.contains("stuff", Qt::CaseInsensitive)
            && tables.contains("who_boss", Qt::CaseInsensitive)
            && tables.contains("positions", Qt::CaseInsensitive))
        return QSqlError();

    QSqlQuery q;
    if (!q.exec(QLatin1String("create table positions(type integer primary key, description varchar)")))
        return q.lastError();

    q.exec(QLatin1String("insert into positions(type, description) values(0, \"Employer\")"));
    q.exec(QLatin1String("insert into positions(type, description) values(1, \"Manager\")"));
    q.exec(QLatin1String("insert into positions(type, description) values(2, \"Sales\")"));

    if (!q.exec(QLatin1String("create table stuff(id integer primary key, name varchar, start_date date, base_rate integer, type integer, FOREIGN KEY(type) REFERENCES positions(type))")))
        return q.lastError();

    if (!q.exec(QLatin1String("create table who_boss(id integer, boss_id integer, FOREIGN KEY(id) REFERENCES stuff(id))")))
        return q.lastError();

    return QSqlError();
}

int DataBase::addWorker(const QString &name, QDate start_date, int base_rate, int type)
{
    QSqlQuery q;
    if (!q.prepare(QLatin1String("insert into stuff(name, start_date, base_rate, type) values(?, ?, ?, ?)"))){
        return false;
    }

    q.bindValue(0, name);
    q.bindValue(1, start_date);
    q.bindValue(2, base_rate);
    q.bindValue(3, type); //добавить проверку что position_type={0,1,2}
    if(!q.exec()){
        return -1;
    }
    cout << "Added" << endl;

    q.exec("SELECT COUNT(name) FROM stuff");
    q.first();
    return q.value(0).toInt();
}

bool DataBase::setBoss(int worker_id, int boss_id){
    if(worker_id == boss_id){ //это вызовет рекурсию при подсчёте зп
        printf("%s\n","нельзя стать начальником самому себе");
        return false;
    }

    QSqlQuery q;
    q.prepare(QLatin1String("select boss_id from who_boss where id=?"));
    q.bindValue(0, boss_id);
    q.exec();
    if(q.first() && q.value(0).toInt() == worker_id){ //это вызовет рекурсию при подсчёте зп
        printf("%s\n","нельзя стать начальником своего начальника");
        return false;
    }

    if (!q.prepare(QLatin1String("insert into who_boss(id, boss_id) values(?, ?)"))){
        return false;
    }

    q.bindValue(0, worker_id);
    q.bindValue(1, boss_id);
    if(!q.exec()){
        return false;
    }

    cout << "Boss assigned" << endl;
    return true;
}

bool DataBase::setPosition(int worker_id, int position_type){
    QSqlQuery q;
    if (!q.prepare(QLatin1String("update stuff set type=? where id=?"))){
        return false;
    }

    q.bindValue(0, position_type);
    q.bindValue(1, worker_id);
    if(!q.exec()){
        return false;
    }

    cout << "Position assigned" << endl;
    return true;
}

QSqlRecord DataBase::getData(int id){
    QSqlQuery q;
    if (q.prepare(QLatin1String("select * from stuff where id = ?"))){
        q.bindValue(0, id);
        q.exec();
        if (q.first()) {
            return q.record();
        }
    }
    QSqlRecord empty_res;
    return empty_res;
}

QSqlQuery DataBase::getSlaves(int worker_id){
    QSqlQuery q;
    if (q.prepare(QLatin1String("select stuff.id, stuff.type from stuff join who_boss on stuff.id=who_boss.id where who_boss.boss_id=?"))){
        q.bindValue(0, worker_id);
        q.exec();
    }
    return q;
}

QSqlQuery DataBase::getSlaves(int worker_id, int level){
    QSqlQuery q;
    if (q.prepare(QLatin1String("select stuff.id from stuff join who_boss on stuff.id=who_boss.id where who_boss.boss_id=? and stuff.type=?"))){
        q.bindValue(0, worker_id);
        q.bindValue(1, level);
        q.exec();
    }
    return q;
}

int DataBase::calculateAllStuffSalary(QDate some_date){
    int res = 0;
    QSqlQuery q = this->getAllStuff();
    while(q.next()){
        int w_id = q.value(0).toInt();
        int type = q.value(1).toInt();
        if(type == 0){
            Employer s(w_id, *this);
            res += s.calulate_salary(some_date);
        }
        if(type == 1){
            Manager s(w_id, *this);
            res += s.calculateSalary(some_date);
        }
        if(type == 2){
            Sales s(w_id, *this);
            res += s.calculateSalary(some_date);
        }
    }
    return res;
}

QSqlQuery DataBase::getAllStuff(){
    QSqlQuery q;
    q.exec("SELECT id, type from stuff");
    return q;
}

int DataBase::getBoss(int id){
    QSqlQuery q;
    q.prepare(QLatin1String("SELECT boss_id from who_boss where id=?"));
    q.bindValue(0, id);
    q.exec();
    q.first();
    return q.value(0).toInt();
}

