#include <stdio.h>
#include <string.h>

#include "MyQlearningOperate.h"	// Q-learningに関する操作


/*=== インスタンスの生成 ===*/
MyQlearningOperate QLearning;
/*==========================*/


int main(){
	/*------------- コンストラクタの初期化 -------------*/
	QLearning = MyQlearningOperate(20, 10);	// 状態, 行動
	/*--------------------------------------------------*/

	QLearning.rewriteQtable("Qtable2.csv", 2, 6, 40);
		
return 0;
}
