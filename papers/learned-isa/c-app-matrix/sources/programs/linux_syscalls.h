/* Supplied Linux x86-64 OS boundary; all workload computation lives in C. */
#ifndef C_APPS_LINUX_SYSCALLS_H
#define C_APPS_LINUX_SYSCALLS_H

typedef unsigned long long u64;
typedef unsigned int u32;

static long write_stdout(const void *data, unsigned long size)
{
    long written;
    __asm__ volatile (
        "syscall"
        : "=a" (written)
        : "0" (1L), "D" (1L), "S" (data), "d" (size)
        : "rcx", "r11", "memory"
    );
    return written;
}

__attribute__((noreturn)) static void finish(int status)
{
    __asm__ volatile (
        "syscall"
        :
        : "a" (60L), "D" ((long)status)
        : "rcx", "r11", "memory"
    );
    __builtin_unreachable();
}

__attribute__((noreturn)) static void emit_result(u64 result)
{
    /* The frozen target is little-endian Linux x86-64. */
    long written = write_stdout(&result, sizeof(result));
    finish(written == (long)sizeof(result) ? 0 : 1);
}

#endif
