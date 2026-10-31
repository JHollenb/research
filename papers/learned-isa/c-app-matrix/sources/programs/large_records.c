/* Parse 80 built-in text records and aggregate eight hashed name buckets. */
#include "linux_syscalls.h"

static volatile const char input[] =
    "birch,1,50\n"
    "elm,8,187\n"
    "hazelnut,15,324\n"
    "cedar,22,461\n"
    "fir,6,598\n"
    "amber,13,735\n"
    "delta,20,872\n"
    "granite,4,1009\n"
    "birch,11,1146\n"
    "elm,18,1283\n"
    "hazelnut,2,1420\n"
    "cedar,9,1557\n"
    "fir,16,1694\n"
    "amber,23,1831\n"
    "delta,7,1968\n"
    "granite,14,105\n"
    "birch,21,242\n"
    "elm,5,379\n"
    "hazelnut,12,516\n"
    "cedar,19,653\n"
    "fir,3,790\n"
    "amber,10,927\n"
    "delta,17,1064\n"
    "granite,1,1201\n"
    "birch,8,1338\n"
    "elm,15,1475\n"
    "hazelnut,22,1612\n"
    "cedar,6,1749\n"
    "fir,13,1886\n"
    "amber,20,2023\n"
    "delta,4,160\n"
    "granite,11,297\n"
    "birch,18,434\n"
    "elm,2,571\n"
    "hazelnut,9,708\n"
    "cedar,16,845\n"
    "fir,23,982\n"
    "amber,7,1119\n"
    "delta,14,1256\n"
    "granite,21,1393\n"
    "birch,5,1530\n"
    "elm,12,1667\n"
    "hazelnut,19,1804\n"
    "cedar,3,1941\n"
    "fir,10,78\n"
    "amber,17,215\n"
    "delta,1,352\n"
    "granite,8,489\n"
    "birch,15,626\n"
    "elm,22,763\n"
    "hazelnut,6,900\n"
    "cedar,13,1037\n"
    "fir,20,1174\n"
    "amber,4,1311\n"
    "delta,11,1448\n"
    "granite,18,1585\n"
    "birch,2,1722\n"
    "elm,9,1859\n"
    "hazelnut,16,1996\n"
    "cedar,23,133\n"
    "fir,7,270\n"
    "amber,14,407\n"
    "delta,21,544\n"
    "granite,5,681\n"
    "birch,12,818\n"
    "elm,19,955\n"
    "hazelnut,3,1092\n"
    "cedar,10,1229\n"
    "fir,17,1366\n"
    "amber,1,1503\n"
    "delta,8,1640\n"
    "granite,15,1777\n"
    "birch,22,1914\n"
    "elm,6,51\n"
    "hazelnut,13,188\n"
    "cedar,20,325\n"
    "fir,4,462\n"
    "amber,11,599\n"
    "delta,18,736\n"
    "granite,2,873\n";

static u64 quantities[8];
static u64 revenues[8];
static u64 counts[8];

static u32 parse_unsigned(const volatile char **cursor)
{
    u32 value = 0;
    while (**cursor >= '0' && **cursor <= '9') {
        value = value * 10U + (u32)(**cursor - '0');
        ++*cursor;
    }
    return value;
}

static void aggregate(void)
{
    const volatile char *cursor = input;
    while (*cursor != '\0') {
        unsigned bucket = 0;
        while (*cursor != ',') {
            bucket = (bucket * 33U + (unsigned char)*cursor) & 7U;
            ++cursor;
        }
        ++cursor;
        u32 quantity = parse_unsigned(&cursor);
        ++cursor; /* comma in the valid built-in fixture */
        u32 price = parse_unsigned(&cursor);
        ++cursor; /* newline in the valid built-in fixture */
        quantities[bucket] += quantity;
        revenues[bucket] += (u64)quantity * price;
        counts[bucket] += 1ULL;
    }
}

static u64 digest(void)
{
    u64 result = 1469598103934665603ULL;
    for (unsigned bucket = 0; bucket < 8; ++bucket) {
        result = (result ^ quantities[bucket]) * 1099511628211ULL;
        result = (result ^ revenues[bucket]) * 1099511628211ULL;
        result = (result ^ counts[bucket]) * 1099511628211ULL;
    }
    return result;
}

__attribute__((noreturn)) void _start(void)
{
    aggregate();
    emit_result(digest());
}
