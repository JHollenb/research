#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static double now(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

static void save_pipe(int fd, const char *path) {
    int out = open(path, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    char buffer[4096];
    ssize_t n;
    while ((n = read(fd, buffer, sizeof buffer)) > 0) {
        ssize_t done = 0;
        while (done < n) {
            ssize_t wrote = write(out, buffer + done, n - done);
            if (wrote <= 0) _exit(4);
            done += wrote;
        }
    }
    close(out);
    close(fd);
}

int main(int argc, char **argv) {
    if (argc != 4) return 2;
    int output[2], errors[2];
    if (pipe(output) || pipe(errors)) return 3;
    struct rusage usage;
    int status;
    double start = now();
    pid_t child = fork();
    if (child < 0) return 3;
    if (!child) {
        dup2(output[1], STDOUT_FILENO);
        dup2(errors[1], STDERR_FILENO);
        close(output[0]); close(output[1]); close(errors[0]); close(errors[1]);
        execl(argv[1], argv[1], (char *)NULL);
        _exit(127);
    }
    close(output[1]); close(errors[1]);
    if (wait4(child, &status, 0, &usage) < 0) return 3;
    double wall = now() - start;
    save_pipe(output[0], argv[2]);
    save_pipe(errors[0], argv[3]);
    double cpu = usage.ru_utime.tv_sec + usage.ru_utime.tv_usec * 1e-6
               + usage.ru_stime.tv_sec + usage.ru_stime.tv_usec * 1e-6;
    printf("{\"wall_s\":%.12f,\"cpu_s\":%.12f,\"maxrss_kib\":%ld,\"exit_code\":%d,\"signal\":%d}\n",
           wall, cpu, usage.ru_maxrss,
           WIFEXITED(status) ? WEXITSTATUS(status) : -1,
           WIFSIGNALED(status) ? WTERMSIG(status) : 0);
    return 0;
}
