// semantics.c

#include <string.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[50];
    int value;
} Variable;

Variable symbol_table[100];
int var_count = 0;

// Find a variable's index in the table by its name
int find_variable(char* name) {
    for (int i = 0; i < var_count; i++) {
        if (strcmp(symbol_table[i].name, name) == 0) {
            return i;
        }
    }
    return -1; // Not found
}

// The 'change' command logic
void update_variable(char* name, int new_value) {
    int index = find_variable(name);
    if (index != -1) {
        symbol_table[index].value = new_value;
        printf("Anima: Updated %s to %d\n", name, new_value);
    } else {
        printf("Anima Error: Variable '%s' doesnt exist.\n", name);
    }
}

void store_variable(char* name, int value) {
        int idx = find_variable(name);
        if (idx != -1) {
            symbol_table[idx].value = value;
        } else {
            strncpy(symbol_table[var_count].name, name, 49);
            symbol_table[var_count].value = value;
            var_count++;
        }
    }