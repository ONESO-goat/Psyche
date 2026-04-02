#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "lexer.h"

Token next_token(const char** source) {
    while (isspace(**source)) (*source)++; // Skip whitespace

    if (**source == '\0') return (Token){TOKEN_EOF, NULL};

    // Handle multi-character operators/keywords
    if (strncmp(*source, "but if", 6) == 0) {
        *source += 6;
        return (Token){TOKEN_BUT_IF, "but if"};
    }
    if (strncmp(*source, "add*", 4) == 0) {
        *source += 4;
        return (Token){TOKEN_ADD_ASSIGN, "add*"};
    }
    if (strncmp(*source, "is", 2) == 0 && isspace((*source)[2])) {
        *source += 2;
        return (Token){TOKEN_IS, "is"};
    }

    // Handle Identifiers and Keywords
    if (isalpha(**source)) {
        char buffer[128];
        int i = 0;
        while (isalnum(**source) || **source == '_') {
            buffer[i++] = *(*source)++;
        }
        buffer[i] = '\0';

        if (strcmp(buffer, "int") == 0) return (Token){TOKEN_INT, "int"};
        if (strcmp(buffer, "print") == 0) return (Token){TOKEN_PRINT, "print"};
        if (strcmp(buffer, "change") == 0) return (Token){TOKEN_CHANGE, "change"};
        
        return (Token){TOKEN_IDENTIFIER, strdup(buffer)};
    }

    // Handle Numbers
    if (isdigit(**source)) {
        char buffer[64];
        int i = 0;
        while (isdigit(**source)) buffer[i++] = *(*source)++;
        buffer[i] = '\0';
        return (Token){TOKEN_NUMBER, strdup(buffer)};
    }

    (*source)++;
    return (Token){TOKEN_UNKNOWN, NULL};
}