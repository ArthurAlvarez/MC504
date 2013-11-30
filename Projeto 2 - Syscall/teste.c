#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (void) {
	
	char newLine = (char)10;
	int pid = getpid();
	
	syscall(351, 5000, pid);
	
	printf("processo programado para parar em 5000 ms. %c", newLine);
	
	while(1) {
		
	}
	
	return 0;
}

