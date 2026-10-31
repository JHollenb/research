/* A freestanding Linux x86-64 C program: no libc or assembly source file. */
static const char message[] = "Hello, world!\n";

__attribute__((noreturn)) void _start(void)
{
    long written;
    __asm__ volatile (
        "syscall"
        : "=a" (written)
        : "0" (1L), "D" (1L), "S" (message), "d" (sizeof(message) - 1)
        : "rcx", "r11", "memory"
    );
    __asm__ volatile (
        "syscall"
        :
        : "a" (60L), "D" (0L)
        : "rcx", "r11", "memory"
    );
    __builtin_unreachable();
}
