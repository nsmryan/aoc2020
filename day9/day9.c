#include <stdint.h>
#include <stdio.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>


uint64_t solve(uint64_t *nums, uint32_t numsSize, uint32_t preamble_length);
uint64_t solve2(uint64_t *nums, uint32_t numsSize, uint64_t total);

int main(void) {
    FILE *file = fopen("day9.txt", "r");
    assert(file != NULL);

    fseek(file, 0, SEEK_END);
    int len = ftell(file);
    fseek(file, 0, SEEK_SET);

    char *data = (char*)calloc(len, 1);
    assert(data != NULL);

    fread(data, len, 1, file);

    uint32_t numlines = 0;
    for (uint32_t index = 0; index < len; index++) {
        if (data[index] == '\n') {
            numlines++;
        }
    }
    if (data[len - 1] != '\n') {
        numlines++;
    }

    uint64_t *nums = (uint64_t*)calloc(numlines, sizeof(uint64_t));

    uint32_t charindex = 0;
    for (uint32_t line_index = 0; line_index < numlines; line_index++) {
        uint32_t startindex = charindex;
        while ((charindex != len) && (data[charindex] != '\n')) {
            charindex++;
        }

        if (data[charindex] == '\n') {
            data[charindex] = '\0';
        }

        uint64_t num = strtol(&data[startindex], NULL, 10);
        nums[line_index] = num;

        charindex++;
    }

    uint32_t preamble_length = 25;
    uint64_t result = solve(nums, numlines, preamble_length);

    printf("%lld\n", result);

    uint64_t sum = solve2(nums, numlines, result);
    printf("%lld\n", sum);
}

uint64_t solve(uint64_t *nums, uint32_t numsSize, uint32_t preamble_length) {
    assert(preamble_length < numsSize);

    for (uint32_t index = preamble_length; index < numsSize; index++) {
        bool found = false;

        uint32_t offset = index - preamble_length;
        for (uint32_t first = 0; first < preamble_length && !found; first++) {
            for (uint32_t second = 0; second < preamble_length && !found; second++) {
                if (first == second) {
                    continue;
                }

                if ((nums[offset + first] + nums[offset + second]) == nums[index]) {
                    found = true;
                    printf("%d (%d, %d) | %lld + %lld == %lld\n", index, first, second, nums[first], nums[second], nums[index]);
                }
            }
        }

        if (!found) {
            return nums[index];
        }
    }

    return -1;
}

uint64_t solve2(uint64_t *nums, uint32_t numsSize, uint64_t total) {
    for (uint32_t bottom = 0; bottom < (numsSize - 1); bottom++) {
        uint64_t sum = nums[bottom];
        for (uint32_t top = bottom + 1; top < numsSize; top++) {
            sum += nums[top];

            if (sum == total) {
                uint64_t smallest = 0xFFFFFFFFFFFFFFFF;
                uint64_t largest = 0;
                for (uint32_t index = bottom; index < top; index++) {
                    if (nums[index] < smallest) {
                        smallest = nums[index];
                    }

                    if (nums[index] > largest) {
                        largest = nums[index];
                    }
                }

                return smallest + largest;
            }
        }
    }

    return -1;
}

