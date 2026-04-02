#include <stdio.h>
#include "lexer.h"

void parse_code(const char* code) {
    const char* ptr = code;
    printf("--- Compiling Custom Language ---\n");

    while (1) {
        Token t = next_token(&ptr);
        if (t.type == TOKEN_EOF) break;

        switch(t.type) {
            case TOKEN_INT:      printf("[Type: Integer] "); break;
            case TOKEN_IDENTIFIER: printf("[Var: %s] ", t.value); break;
            case TOKEN_IS:       printf("[Op: Assign] "); break;
            case TOKEN_NUMBER:   printf("[Val: %s]\n", t.value); break;
            case TOKEN_BUT_IF:   printf("[Keyword: Elif]\n"); break;
            case TOKEN_ADD_ASSIGN: printf("[Op: +=]\n"); break;
            default:             printf("[Unknown] ");
        }
    }
}

int main() {
    // Example string from your prompt
    const char* my_program = "int x is 5 but if x add* 1";
    parse_code(my_program);
    return 0;
}