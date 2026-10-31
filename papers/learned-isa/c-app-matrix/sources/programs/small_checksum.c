/* Twenty-four ordinary C updates of four volatile unsigned 64-bit cells. */
#include "linux_syscalls.h"

static volatile u64 a = 0x123456789abcdef0ULL;
static volatile u64 b = 0x0fedcba987654321ULL;
static volatile u64 c = 0x3141592653589793ULL;
static volatile u64 d = 0x2718281828459045ULL;

__attribute__((noreturn)) void _start(void)
{
    a += b;
    c ^= d;
    b += c;
    d ^= a;
    a *= 3ULL;
    b ^= d;
    c += a;
    d *= 5ULL;
    a ^= c;
    b -= a;
    c *= 7ULL;
    d += b;
    a += d;
    b *= 11ULL;
    c ^= b;
    d -= c;
    a *= 13ULL;
    b += d;
    c += a;
    d ^= b;
    a -= c;
    b ^= a;
    c += d;
    d *= 17ULL;
    emit_result(a ^ b ^ c ^ d);
}
