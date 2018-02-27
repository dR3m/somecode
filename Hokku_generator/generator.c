#include <stdio.h>
#include <stdlib.h>
char secret[44];

char* read_command(){
	FILE* f;
	f = fopen(".secret2.txt", "r"); 
	fread(secret,1, 44 , f);
	fclose(f);	
	return &secret;
}

void level3(char inp[]){
	char* a = 3405691582;//0xcafebabe;//истина между строк
	char* ptrsecret = read_command();
	char* b = 4207869677;//0xfacefeed;
	char c[79];

	printf("Введи ещё что-нибудь: \n");
	scanf("%s", c);
	printf(inp);
	system(b);
}

void level2(){
	char inp[64];
	int cant_touch_this = 0;
	printf("Введи что-нибудь: ");
	scanf("%s", &inp);
	if (cant_touch_this != 0){
//	if (cant_touch_this == 31337){
		system("cat open_me/lvl2"); //выведет хокку
	}
	else{		
		printf("Вижу ты не достоин\n");
		printf("%x\n", cant_touch_this);
	}
}

void level1(){
	int key;
	printf("Введи секрет: ");
	scanf("%d", &key);
	FILE* f;
	int check;

	if (f = fopen(".secret1.txt", "r")){
		fscanf(f, "%d", &check);
		fclose(f);	
	}

	check ^= 0xdeadbeef;
	if (check && key == 1){
		system("cat open_me/lvl1"); //выведет хокку
	}
	else{
		printf("Вижу ты не достоин\n"); //lose
	}
}

int main(int argc, char *argv[]){
	system("clear");
	system("cat .design");

	int task; 
	printf("Выбери свой путь:\n");
	printf("0 - Хочу домой :(\n1 - Изи бризи\n2 - Плыть по течению\n3 - Путь Хокаге\n");
	scanf("%d", &task);

	switch(task){
		case 0: break;
		case 1: 
			level1();
			break;
		case 2: 
			level2();
			break;
		case 3:
			level3(argv[1]);
			break;
		default: break;
	}
	return 0;
}
