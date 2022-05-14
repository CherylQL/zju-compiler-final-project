	.text
	.file	"<string>"
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	subq	$40, %rsp
.L0$pb:
	leaq	.L0$pb(%rip), %rax
	movabsq	$_GLOBAL_OFFSET_TABLE_-.L0$pb, %rdx
	addq	%rax, %rdx
	movabsq	$x@GOTOFF, %rax
	movl	$6, (%rdx,%rax)
	movabsq	$fmt2078927757@GOTOFF, %rcx
	addq	%rdx, %rcx
	movabsq	$printf@GOTOFF, %rax
	addq	%rdx, %rax
	movl	$6, %edx
	callq	*%rax
	addq	$40, %rsp
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main

	.globl	f
	.p2align	4, 0x90
	.type	f,@function
f:
	subq	$48, %rsp
	movabsq	$8589934593, %rax
	movq	%rax, 8(%rsp)
	movabsq	$17179869187, %rax
	movq	%rax, 16(%rsp)
	movabsq	$25769803781, %rax
	movq	%rax, 24(%rsp)
	movabsq	$34359738375, %rax
	movq	%rax, 32(%rsp)
	movabsq	$42949672969, %rax
	movq	%rax, 40(%rsp)
	movslq	%ecx, %rax
	movl	4(%rsp,%rax,4), %eax
	addq	$48, %rsp
	retq
.Lfunc_end1:
	.size	f, .Lfunc_end1-f

	.type	x,@object
	.bss
	.globl	x
	.p2align	2
x:
	.long	0
	.size	x, 4

	.type	fmt2078927757,@object
	.section	.rodata,"a",@progbits
fmt2078927757:
	.asciz	"SPL >> %d "
	.size	fmt2078927757, 11

	.section	".note.GNU-stack","",@progbits
