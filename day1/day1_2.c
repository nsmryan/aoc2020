#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>


int main(void) {
    char *file_name = "day1.txt";
    FILE *file = fopen(file_name, "r");
    assert(NULL != file);

    int result;
    result = fseek(file, 0, SEEK_END);
    assert(result >= 0);

    int len = ftell(file);
    result = fseek(file, 0, SEEK_SET);
    assert(result >= 0);

    char *contents = (char*)malloc(len + 1);
    result = fread(contents, len, 1, file);
    assert(result >= 0);

    uint32_t num_lines = 0;
    for (uint32_t index = 0; index < len; index++) {
        if (contents[index] == '\n') {
            num_lines++;
        }
    }

    uint64_t *expenses = (uint64_t*)calloc(num_lines, 1);
    uint32_t cursor = 0;
    char *line_ptr = contents;
    for (uint32_t line_index = 0; line_index < num_lines; line_index++) {
        uint64_t expense = 0;
        expense = strtol(line_ptr, &line_ptr, 10);
        // 0 does not occur as a valid value, and indicates a conversion error
        if (expense == 0) {
            num_lines = line_index;
            break;
        }
        expenses[line_index] = expense;
        line_ptr += 2; // skip \n\r
    }

    printf("num_lines = %d\n", num_lines);
    for (int i = 0; i < num_lines; i++) {
        for (int j = i; j < num_lines; j++) {
            for (int k = j; k < num_lines; k++) {
                uint64_t sum = expenses[i] + expenses[j] + expenses[k];
                if (sum == 2020ULL) {
                    uint64_t prod = expenses[i] * expenses[j] * expenses[k];
                    exit(EXIT_SUCCESS);
                }
            }
        }
    }
}
