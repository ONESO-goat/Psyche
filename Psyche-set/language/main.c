// main.c - Entry point for Psyche's custom language interpreter


#include <stdio.h>
#include "lexer.h"

void parse_code(const char* code) {
    const char* ptr = code;
    
    Token t1 = next_token(&ptr); // Should be 'int'
    Token t2 = next_token(&ptr); // Should be 'x'
    Token t3 = next_token(&ptr); // Should be 'is'
    Token t4 = next_token(&ptr); // Should be '5'

    if (t1.type == TOKEN_INT && t3.type == TOKEN_IS) {
        // Here we actually call our memory function!
        store_variable(t2.value, atoi(t4.value));
    }
}


void execute_statement(const char** ptr) {
    Token t1 = next_token(ptr); // Get the first word (e.g., "x")

    if (t1.type == TOKEN_IDENTIFIER) {
        Token op = next_token(ptr); // Get the operator (e.g., "add*")
        Token val = next_token(ptr); // Get the number (e.g., "10")

        int index = find_variable(t1.value);
        if (index != -1) {
            if (op.type == TOKEN_ADD_ASSIGN) {
                symbol_table[index].value += atoi(val.value);
                printf("Anima: %s is now %d\n", t1.value, symbol_table[index].value);
            }
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: anima <filename>\n");
        return 1;
    }

    FILE* file = fopen(argv[1], "r");
    if (!file) {
        printf("Error: cannot open file '%s'\n", argv[1]);
        return 1;
    }

    // Find file size
    fseek(file, 0, SEEK_END);       // jump to end
    long size = ftell(file);        // how many bytes in?
    fseek(file, 0, SEEK_SET);       // jump back to start

    // Allocate a buffer and read it all
    char* source = malloc(size + 1);
    fread(source, 1, size, file);
    source[size] = '\0';            // null-terminate!
    fclose(file);

    parse_code(source);

    free(source);
    return 0;
}