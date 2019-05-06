#include "employer.h"
#include "sql_db.h"
#include <iostream>
using namespace std;

int Employer::calulate_salary(QDate some_date){
    int exp = experience(some_date); //стаж службы
    if(exp>=0){ //если стаж отрицательный, значит some_date раньше даты найма
        int res = this ->base_salary;
        double n, sum_n;

        for(int i=1; i<=exp; i++){
           n = this->base_salary*0.03;  //надбавка за один год
           sum_n = n*exp*0.3;  //30% от суммарной надбавки за стаж
           if(n > sum_n)
               res += sum_n;
           else
               res += n;
        }
        printf("Salary for id=%d : %d\n", this->id, res);
        return res;
    }
    return 0;
}
