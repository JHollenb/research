// Dynamic opcode-mix tracer: single-steps a Linux x86-64 program on the real CPU and counts executed
// instructions per RIP, keeping the 16 bytes at each distinct RIP for offline decoding. Usage:
//   trace_opmix <out-file> <max-steps> <program> [args...]
// Output: "steps <n> status <exit|signal|limit> <code>" then one "<rip-hex> <count> <16-byte-hex>" line per RIP.
// Assumes code at a given RIP does not change while it runs (true for static and relocated dynamic text).
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>

#define SLOTS (1u << 22)
typedef struct { uint64_t rip, count; unsigned char bytes[16]; } Slot;

int main(int argc, char **argv) {
    if (argc < 4) return 2;
    long max_steps = strtol(argv[2], 0, 10);
    Slot *table = calloc(SLOTS, sizeof(Slot));
    if (!table) return 3;
    pid_t child = fork();
    if (child < 0) return 3;
    if (!child) {
        int devnull = open("/dev/null", O_WRONLY);
        if (devnull >= 0) { dup2(devnull, 1); dup2(devnull, 2); }
        if (ptrace(PTRACE_TRACEME, 0, 0, 0) < 0) _exit(126);
        execv(argv[3], argv + 3);
        _exit(127);
    }
    int status = 0, code = 0;
    const char *how = "limit";
    long steps = 0, distinct = 0;
    if (waitpid(child, &status, 0) < 0) return 4;
    for (; steps < max_steps; ++steps) {
        if (!WIFSTOPPED(status) || WSTOPSIG(status) != SIGTRAP) { how = "unexpected-stop"; code = WIFSTOPPED(status) ? WSTOPSIG(status) : -1; break; }
        struct user_regs_struct r;
        if (ptrace(PTRACE_GETREGS, child, 0, &r) < 0) { how = "getregs"; break; }
        uint64_t h = (r.rip * 0x9E3779B97F4A7C15ull) >> 42;
        while (table[h].count && table[h].rip != r.rip) h = (h + 1) & (SLOTS - 1);
        if (!table[h].count) {
            if (++distinct > (long)(SLOTS / 2)) { how = "table-full"; break; }
            table[h].rip = r.rip;
            for (int w = 0; w < 2; ++w) {
                errno = 0;
                long word = ptrace(PTRACE_PEEKTEXT, child, (void *)(r.rip + 8 * w), 0);
                memcpy(table[h].bytes + 8 * w, &word, 8);
            }
        }
        table[h].count++;
        if (ptrace(PTRACE_SINGLESTEP, child, 0, 0) < 0) { how = "singlestep"; break; }
        if (waitpid(child, &status, 0) < 0) { how = "waitpid"; break; }
        if (WIFEXITED(status)) { how = "exit"; code = WEXITSTATUS(status); ++steps; break; }
        if (WIFSIGNALED(status)) { how = "signal"; code = WTERMSIG(status); ++steps; break; }
    }
    if (strcmp(how, "exit") && strcmp(how, "signal")) { kill(child, SIGKILL); waitpid(child, &status, 0); }
    FILE *out = fopen(argv[1], "w");
    if (!out) return 5;
    fprintf(out, "steps %ld status %s %d\n", steps, how, code);
    for (uint64_t i = 0; i < SLOTS; ++i) {
        if (!table[i].count) continue;
        fprintf(out, "%llx %llu ", (unsigned long long)table[i].rip, (unsigned long long)table[i].count);
        for (int b = 0; b < 16; ++b) fprintf(out, "%02x", table[i].bytes[b]);
        fputc('\n', out);
    }
    fclose(out);
    return 0;
}
