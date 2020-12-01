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

    uint32_t *expenses = (uint32_t*)calloc(num_lines, 1);
    uint32_t cursor = 0;
    char *line_ptr = contents;
    for (uint32_t line_index = 0; line_index < num_lines; line_index++) {
        int expense = 0;
        expense = strtol(line_ptr, &line_ptr, 10);
        // 0 does not occur as a valid value, and indicates a conversion error
        if (expense == 0) {
            break;
        }
        expenses[line_index] = expense;
        line_ptr += 2; // skip \n\r
    }

    for (int i = 0; i < num_lines; i++) {
        for (int j = i; j < num_lines; j++) {
            if ((expenses[i] + expenses[j]) == 2020) {
                printf("%d\n", expenses[i] * expenses[j]);
                exit(EXIT_SUCCESS);
            }
        }
    }
}
