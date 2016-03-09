#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <direct.h>

#include "MyQlearningOperate.h"	// Q-learningに関する操作


/*=== インスタンスの生成 ===*/
MyQlearningOperate QLearning;
/*==========================*/

#define FolderName "Q学習実験"	// 保存フォルダ名
double vending_machine(int s, int a, int &sd);	// チーズ製造器のシミュレータ(状態, 行動, 次の状態)



int main(){
	int epsilon = 20;		// ε:行動を無作為に選ぶ確率[%]
	int EpisodeMax = 100;	// エピソードの繰り返し数
	int TrialMax = 10;		// 試行回数
	double reward = 0;		// 報酬
	int SuccessNum = 0;		// 成功数

	int QtableSaveFlag = 1;			// Q値のテーブルを保存するフラグ(1:する, 0:しない)
	int QtableSaveInterval = 10;	// 保存する間隔
	int TraceSaveFlag = 1;			// 適格度のテーブルを保存するフラグ(1:する, 0:しない)
	int TraceSaveInterval = 10;		// 保存する間隔
	int SuccessSaveFlag = 1;		// 成功率を保存するフラグ(1:する, 0:しない)
	int SuccessSaveInterval = 10;	// 保存する間隔

	int num_a = 2;			// 行動の数
	int num_s = 2;			// 状態の数
	int a = 0;				// 行動
	int s = 0;				// 状態
	int sd = 0;				// 行動の実行によって遷移する次の状態
	int ad = 0;				// 次の行動
	char FileNameBuffer[100];


	/*------------- コンストラクタの初期化 -------------*/
	QLearning = MyQlearningOperate(num_s , num_a);	// 状態の数, 行動の数
	/*--------------------------------------------------*/


	/*--- パラメータを設定 ---*/
	QLearning.alpha = 0.5;	// α:学習係数
	QLearning.gamma = 0.9;	// γ:減衰係数
	QLearning.lambda = 0.7;	// λ：トレースの減衰係数


	/*--- Q値のテーブルを作成・初期化 ---*/
	_mkdir(FolderName);						// フォルダ作成
	QLearning.makeQtable();					// 作成
	QLearning.initQtable();					// 初期化


	/*--- 適格度トレースのテーブルを作成・初期化 ---*/
	QLearning.makeTraceTable();					// 作成
	QLearning.initTraceTable();					// 初期化


	/*--- 学習 ---*/
	for(int i=1; i<=EpisodeMax; i++){	// エピソード

		// 各パラメータを初期化
		s = 0;
		a = 0;
		reward = 0;

		for(int j=1; j<=TrialMax; j++){	// 試行

			// 行動を実行
			reward = vending_machine(s, a, sd);


			// 行動をε-greedy法で選択
			ad = QLearning.softmax_roulette(sd);


			// Q値の更新
			QLearning.updateQtable_replacing_trace(s, sd, a, reward);


			// 状態の更新
			s = sd;
			a = ad;


			// 終了条件に合えば繰り返しを終了
			if(reward > 0)	break;

		}

		// 指定したタイミングでQ値を保存
		if( (QtableSaveFlag==1) && (i%QtableSaveInterval == 0) ){
			QLearning.saveQtable(FolderName, i);
		}


		// 指定したタイミングで適格度を保存
		if( (TraceSaveFlag==1) && (i%TraceSaveInterval == 0) ){
			QLearning.saveTraceTable(FolderName, i);
		}


		// 結果を表示
		printf("%d: ", i);
		if(reward > 0){
			printf("成功\n");
			SuccessNum++;
		}
		else	printf("失敗\n");


		// 成功率を出力
		if( (SuccessSaveFlag==1) && (i%SuccessSaveInterval == 0) ){
			QLearning.saveSuccess(FolderName, i, (double)SuccessNum/(double)SuccessSaveInterval*100);
			SuccessNum = 0;
		}

	}


	/*--- 成功率を表示 ---*/
//	printf("\n成功率 -> %.3lf[％]\n\n", (double)SuccessNum/(double)EpisodeMax*100);


	/*--- Q値のテーブルを表示 ---*/
	printf("--- Q値のテーブル ---\n");
	for(int i=0; i<num_s; i++){
		for(int j=0; j<num_a; j++){
			printf("状態 %d : 行動 %d -> %lf\n", i, j, QLearning.Qtable[i][j]);
		}
	}


	/*--- 学習結果を表示 ---*/
	printf("\n--- 学習結果 ---\n");
	s = 0;	// 状態初期化

	// 学習結果を使って試行
	for(int i=0; i<100; i++){

		// 状態について
		printf("現在の状態 -> ");
		if(s == 0)		printf("ランプ消灯\t");
		else if(s == 1)	printf("ランプ点灯\t");

		// 行動を取得
		a = QLearning.selectMaxAction(s);

		// 行動について
		printf("選択する行動 -> ");
		if(a == 0)		printf("ボタン1を押す\n");
		else if(a == 1)	printf("ボタン2を押す\n");

		// チーズが出たら表示
		if(vending_machine(s, a, sd) > 0){
			printf("\nチーズ出たよ！(終了)\n");
			break;
		}
		s = sd;
	}


	QLearning.freeQtable();	// Qテーブルを解放

getchar();
return 0;
}


/* チーズ製造器のシミュレータ */
double vending_machine(int s, int a, int &sd){
	double reward;	// 報酬

	// スイッチ1を押す
	if(a == 0){
		sd = !s;	// ランプのON,OFFを変更
		reward = 0;
	}

	// スイッチ2を押す
	else{
		if(s == 1){	// ランプONのとき
			sd = s;
			reward = 10;		
		}
		else{	// ランプOFFのとき
			sd = s;
			reward = 0;
		}	
	}
	
	return reward;
}
