#include <stdio.h>
#include <stdlib.h>

#define LengthA 100		// 入力データ1の最大入力数
#define LengthB 100		// 入力データ2の最大入力数


int main(){

	int i, j, k;

	int inputA[LengthA];	// 入力データ1
	int inputB[LengthB];	// 入力データ2

	int LenA;	// 入力データ1の長さ
	int LenB;	// 入力データ2の長さ

	int **Cost;	// 経路の長さ
	int **From;	// どこから来たか(0:斜め, 1:横, 2:縦)

	double Score;	// 類似度

	int Penalty = 10;
	int Yoko = 1;
	int Tate = 1;
	int Naname = 2;

	int Buffer1, Buffer2, Buffer3;

	FILE *FinA;
	FILE *FinB;



	/* ファイルを開いてデータを読み取る */
	if ( (FinA = fopen("Read Data1.csv", "r")) == NULL || (FinB = fopen("Read Data2.csv", "r")) == NULL){
		printf("(´･ω･`) FILE not open!\n");
		return -1;
	}
	for(i=0; i<LengthA; i++){	// データ1読み取り
		if(fscanf(FinA, "%d", &inputA[i]) == EOF) {
			LenA = i;
			break;
		}
	//	printf("%d,", inputA[i]);
	}
//	printf("\n");
	for(i=0; i<LengthB; i++){	// データ2読み取り
		if(fscanf(FinB, "%d", &inputB[i]) == EOF) {
			LenB = i;
			break;
		}
	//	printf("%d,", inputB[i]);
	}
//	printf("\n");


	/* CostとFromのメモリ確保 */
	Cost = (int **) malloc(sizeof(int *) * LenA);
	for(i=0; i<LenA; i++)	Cost[i] = (int *) malloc(sizeof(int) * LenB);

	From = (int **) malloc(sizeof(int *) * LenA);
	for(i=0; i<LenA; i++)	From[i] = (int *) malloc(sizeof(int) * LenB);

	if(Cost==NULL || From==NULL){
		printf("(´･ω･`) メモリ不足です\n");
		return -1;
	}


	/*--- 総当たりでDPマッチング ---*/

	/* [0][0]について */
	if(inputA[0] == inputB[0])	Cost[0][0] = Naname;
	else						Cost[0][0] = Naname * Penalty;
	From[0][0] = 0;	// 斜めから来た


	/* 横一列について */
	for(i=1; i<LenA; i++){
		if(inputA[i] == inputB[0])	Cost[i][0] = Cost[i-1][0] + Yoko;
		else						Cost[i][0] = Cost[i-1][0] + Yoko * Penalty;
		From[i][0] = 1;	// 横から来た
	}


	/* 縦一列について */
	for(j=1; j<LenB; j++){
		if(inputA[0] == inputB[j])	Cost[0][j] = Cost[0][j-1] + Tate;
		else						Cost[0][j] = Cost[0][j-1] + Tate * Penalty;
		From[0][j] = 2;	// 縦から来た
	}

	/* 真ん中の部分について */
	for(i=1; i<LenA; i++){
		for(j=1; j<LenB; j++){

			// コストの計算
			if(inputA[i] == inputB[j]){
				Buffer1 = Cost[i-1][j] + Yoko;
				Buffer2 = Cost[i-1][j-1] + Naname;
				Buffer3 = Cost[i][j-1] + Tate;
			}
			else{
				Buffer1 = Cost[i-1][j] + Yoko * Penalty;
				Buffer2 = Cost[i-1][j-1] + Naname * Penalty;
				Buffer3 = Cost[i][j-1] + Tate * Penalty;
			}

			// 最小距離を選び，通った経路を保存
			if( (Buffer1 < Buffer2) && (Buffer1 < Buffer3) ){
				Cost[i][j] = Buffer1;
				From[i][j] = 1;	// 横
			}
			else if(Buffer2 < Buffer3){
				Cost[i][j] = Buffer2;
				From[i][j] = 0;	// 斜め
			}
			else{
				Cost[i][j] = Buffer3;
				From[i][j] = 2;	// 縦
			}

		}
	}


	/* 類似度の計算 */
	Score = (double)Cost[LenA-1][LenB-1] / (double)(LenA + LenB);
	printf("類似度：%.2lf\n", Score);

	fclose(FinA);
	fclose(FinB);


getchar();
return 0;
}
