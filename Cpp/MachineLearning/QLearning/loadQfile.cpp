#include <stdio.h>

#define s_num 20	// 状態の数
#define a_num 10	// 行動の数

double searchQtable(int search_s, int search_a);	// 検索する状態, 検索する行動

int main(){

	
	printf("Qtable : %lf\n", searchQtable(19, 9));

	getchar(); 

return 0;
}


double searchQtable(int search_s, int search_a){	// 検索する状態, 検索する行動
	FILE *fp;
	char GarbageStr[100];	// いらない部分
	double GarbageDouble;	// いらない部分
	int GarbageInt;			// いらない部分
	double Qtable = 0;		// Q値


	// ファイルを開く
	if ( (fp = fopen("Qtable.csv", "r")) == NULL ){
		printf("(´･ω･`) FILE not open!\n");
		return -1;
	}

	// 1行目を吐き出す
	fscanf(fp, "%s", GarbageStr);

	// 必要な行の手前まで吐き出す
	for(int i=0; i<search_s; i++){
		fscanf(fp, "%d,", &GarbageInt);
		for(int j=0; j<a_num; j++)	fscanf(fp, "%lf,", &GarbageDouble);
	}

	// 必要な列の手前まで吐き出す
	fscanf(fp, "%d,", &GarbageInt);
	for(int j=0; j<search_a; j++)	fscanf(fp, "%lf,", &GarbageDouble);

	// 必要なQ値を読み取る
	fscanf(fp, "%lf,", &Qtable);

	fclose(fp);	// ファイルを閉じる


	return Qtable;
}
