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
	movabsq	$fmt2012440923@GOTOFF, %rcx
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
	movl	$1, %eax
	movl	$1, %edx
	cmpl	%ecx, %edx
	jg	.LBB1_3
	.p2align	4, 0x90
.LBB1_2:
	imull	%edx, %eax
	incl	%edx
	cmpl	%ecx, %edx
	jle	.LBB1_2
.LBB1_3:
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

	.type	fmt2012440923,@object
	.section	.rodata,"a",@progbits
fmt2012440923:
	.asciz	"SPL >> %d "
	.size	fmt2012440923, 11

	.section	".note.GNU-stack","",@progbits
