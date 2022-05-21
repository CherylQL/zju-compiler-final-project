	.text
	.file	"<string>"
	.globl	main
	.p2align	4, 0x90
	.type	main,@function
main:
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rsi
	pushq	%rdi
	pushq	%rbp
	pushq	%rbx
	subq	$440, %rsp
.L0$pb:
	leaq	.L0$pb(%rip), %rax
	movabsq	$_GLOBAL_OFFSET_TABLE_-.L0$pb, %r15
	addq	%rax, %r15
	movabsq	$sca1861328492@GOTOFF, %rcx
	addq	%r15, %rcx
	movabsq	$n@GOTOFF, %r14
	leaq	(%r15,%r14), %rdx
	movabsq	$scanf@GOTOFF, %r12
	addq	%r15, %r12
	callq	*%r12
	movl	(%r15,%r14), %ebp
	movl	$1, %ebx
	movabsq	$sca1372460022@GOTOFF, %rsi
	addq	%r15, %rsi
	movabsq	$x@GOTOFF, %r13
	leaq	(%r15,%r13), %rdi
	cmpl	%ebp, %ebx
	jg	.LBB0_3
	.p2align	4, 0x90
.LBB0_2:
	movq	%rsi, %rcx
	movq	%rdi, %rdx
	callq	*%r12
	movl	(%r15,%r13), %eax
	movslq	%ebx, %rcx
	movl	%eax, 36(%rsp,%rcx,4)
	incl	%ebx
	cmpl	%ebp, %ebx
	jle	.LBB0_2
.LBB0_3:
	movl	(%r15,%r14), %edi
	movl	$1, %ebx
	movabsq	$fmt578616253@GOTOFF, %rsi
	addq	%r15, %rsi
	movabsq	$printf@GOTOFF, %rbp
	addq	%r15, %rbp
	cmpl	%edi, %ebx
	jg	.LBB0_6
	.p2align	4, 0x90
.LBB0_5:
	movslq	%ebx, %rax
	movl	36(%rsp,%rax,4), %edx
	movq	%rsi, %rcx
	callq	*%rbp
	incl	%ebx
	cmpl	%edi, %ebx
	jle	.LBB0_5
.LBB0_6:
	addq	$440, %rsp
	popq	%rbx
	popq	%rbp
	popq	%rdi
	popq	%rsi
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	retq
.Lfunc_end0:
	.size	main, .Lfunc_end0-main

	.globl	qsort
	.p2align	4, 0x90
	.type	qsort,@function
qsort:
	retq
.Lfunc_end1:
	.size	qsort, .Lfunc_end1-qsort

	.type	n,@object
	.bss
	.globl	n
	.p2align	2
n:
	.long	0
	.size	n, 4

	.type	i,@object
	.globl	i
	.p2align	2
i:
	.long	0
	.size	i, 4

	.type	x,@object
	.globl	x
	.p2align	2
x:
	.long	0
	.size	x, 4

	.type	sca1861328492,@object
	.section	.rodata,"a",@progbits
sca1861328492:
	.asciz	"%d"
	.size	sca1861328492, 3

	.type	sca1372460022,@object
sca1372460022:
	.asciz	"%d"
	.size	sca1372460022, 3

	.type	fmt578616253,@object
fmt578616253:
	.asciz	"SPL >> %d "
	.size	fmt578616253, 11

	.section	".note.GNU-stack","",@progbits
