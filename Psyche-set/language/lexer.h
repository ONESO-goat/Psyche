#ifndef LEXER_H
#define LEXER_H

typedef enum {
    TOKEN_INT, TOKEN_STR, TOKEN_BOOL,
    TOKEN_IS, TOKEN_CHANGE,
    TOKEN_IF, TOKEN_BUT_IF, TOKEN_ELSE,
    TOKEN_LOOP_UNTIL, TOKEN_FOR,
    TOKEN_PRINT, TOKEN_ADD_ASSIGN,
    TOKEN_IDENTIFIER, TOKEN_NUMBER, 
    TOKEN_EOF, TOKEN_UNKNOWN
} TokenType;

typedef struct {
    TokenType type;
    char* value;
} Token;

// ADD THIS LINE BELOW:
Token next_token(const char** source);

#endif