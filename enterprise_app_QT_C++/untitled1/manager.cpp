#include "manager.h"
#include "employer.h"

int Manager::calculateSalary(QDate some_date){
    int exp = experience(some_date); //стаж службы
    if(exp>=0){ //если стаж отрицательный, значит some_date раньше даты найма
        int res = this ->base_salary;
        double n, sum_n;

        for(int i=1; i<=exp; i++){
           n = this->base_salary*0.05;  //надбавка за один год
           sum_n = n*exp*0.4;  //40% от суммарной надбавки за стаж
           if(n > sum_n)
               res += sum_n;
           else
               res += n;
        }
        res += this->countSlaves(some_date);
        printf("Salary for id=%d : %d\n", this->id, res);
        return res;
    }
    return 0;
}

int Manager::countSlaves(QDate some_date){
    int res = 0;
    QSqlQuery q = this->db.getSlaves(this->id, 0);
    while(q.next()){
        int e_id = q.value(0).toInt();
        printf("manager id=%d, slave id=%d\n", this->id, e_id);
        Employer e(e_id, this->db);
        res += 0.005*e.calulate_salary(some_date); //0.5% от зп каждого подчинённого 0-типа
    }
    return res;
}
