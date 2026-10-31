/* Insertion sort and an order-sensitive digest of 32 unsigned integers. */
#include "linux_syscalls.h"

static volatile const u32 input[32] = {
    93U, 7U, 4294967295U, 41U, 0U, 18U, 73U, 7U,
    2048U, 511U, 31U, 99U, 2U, 65535U, 1009U, 17U,
    8U, 1U, 4096U, 63U, 127U, 255U, 1023U, 3U,
    8191U, 5U, 29U, 11U, 47U, 23U, 89U, 13U
};

static void sort(u32 *values, unsigned count)
{
    for (unsigned i = 1; i < count; ++i) {
        u32 key = values[i];
        unsigned j = i;
        while (j > 0 && values[j - 1] > key) {
            values[j] = values[j - 1];
            --j;
        }
        values[j] = key;
    }
}

static u64 digest(const u32 *values, unsigned count)
{
    u64 result = 1469598103934665603ULL;
    for (unsigned i = 0; i < count; ++i)
        result = (result ^ values[i]) * 1099511628211ULL;
    return result;
}

__attribute__((noreturn)) void _start(void)
{
    u32 values[32];
    for (unsigned i = 0; i < 32; ++i)
        values[i] = input[i];
    sort(values, 32);
    emit_result(digest(values, 32));
}
