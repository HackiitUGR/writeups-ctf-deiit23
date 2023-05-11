// gcc touch.c -no-pie
#include <stdio.h>
#include <stdlib.h>

// Cómo llego aquí..?
__attribute__ ((force_align_arg_pointer)) // ignore this
void win() {
	printf("Enhorabuena! Aquí tienes tu flag: \n");
	system("cat flag3.txt");
}

unsigned long untouchable2 = 0x31337;

int main() {
	// Ignore me
	setbuf(stdout, NULL);

	unsigned long untouchable1 = 0x31337;
	unsigned long p[] = {1,2,3};
	printf("Código secreto de ayuda para flag2: %p\n", p);

	unsigned long index = 0, value = 0;
	printf("Introduce un índice: ");
	scanf("%lu", &index);
	printf("Introduce un valor: ");
	scanf("%lu", &value);

	p[index] = value;

	if (untouchable1 == 0xcacabaca) {
		system("cat flag1.txt");
	} else if (untouchable2 == 0x123456) {
		system("cat flag2.txt");
	} else {
		printf("Nope! Valores: %lx %lx\n", untouchable1, untouchable2);
	}
}