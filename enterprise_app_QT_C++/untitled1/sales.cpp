#include "sales.h"
#include "employer.h"
#include "manager.h"

int Sales::calculateSalary(QDate some_date){
    int exp = experience(some_date); //стаж службы
    if(exp>=0){ //если стаж отрицательный, значит some_date раньше даты найма
        int res = this ->base_salary;
        double n, sum_n;

        for(int i=1; i<=exp; i++){
           n = this->base_salary*0.01;  //надбавка за один год
           sum_n = n*exp*0.35;  //35% от суммарной надбавки за стаж
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

int Sales::countSlaves(QDate some_date){
    int res = 0;
    QSqlQuery q = this->db.getSlaves(this->id);
    while(q.next()){
        int s_id = q.value(0).toInt();
        int type = q.value(1).toInt();
        printf("sales id=%d, slave id=%d, s_type=%d\n", this->id, s_id, type);
        if(type == 0){
            Employer s(s_id, this->db);
            res += 0.005*s.calulate_salary(some_date);
        }
        if(type == 1){
            Manager s(s_id, this->db);
            res += 0.005*s.calculateSalary(some_date);
        }
        if(type == 2){
            Sales s(s_id, this->db);
            res += 0.003*s.calculateSalary(some_date);  //0.3% от зп каждого подчинённого
        }
    }
    return res;
}
