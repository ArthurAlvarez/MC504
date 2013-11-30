#include <linux/unistd.h>
#include <linux/linkage.h>
#include <linux/syscalls.h>	
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/timer.h>

MODULE_LICENSE("GPL");

static struct timer_list my_timer;
unsigned int tempoInicial;
int waitedPid;

void my_timer_callback (unsigned long data) {
	unsigned int tempoTotal;
	
	if (CONFIG_MMU) {
		sys_kill(waitedPid,SIGSTOP);
		tempoTotal = jiffies_to_msecs(jiffies);
		printk("Processo terminado apos %u ms.\n", tempoTotal - tempoInicial);
    }
    else printk("Processo nao terminado.\n");
}


int seta_timer (const unsigned int tempo) {
	int ret;
	
	printk("Timer module installing\n");
	
	setup_timer(&my_timer, my_timer_callback, 0);
	
	tempoInicial = jiffies_to_msecs(jiffies);
	ret = mod_timer(&my_timer, jiffies + msecs_to_jiffies(tempo));
	if (ret) printk("Error in mod_timer\n");
	
	return 0;
}

void cleanup_module (void) {
	int ret;
	
	ret = del_timer(&my_timer);
	if (ret) printk("The timer is still in use...\n");
	
	printk("Timer module uninstalling\n");

	return;
}

asmlinkage long sys_timed_stop (const unsigned int n, int pid) {
	waitedPid = pid;
	return seta_timer(n);
}

